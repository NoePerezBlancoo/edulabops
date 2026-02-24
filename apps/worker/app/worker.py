import os
import json
import shutil
import subprocess
import tempfile
from celery import Celery
from sqlalchemy import create_engine, text

DATABASE_URL = os.getenv("DATABASE_URL")
REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379/0")

celery_app = Celery("edulabops_worker", broker=REDIS_URL, backend=REDIS_URL)
engine = create_engine(DATABASE_URL, pool_pre_ping=True)

def _run(cmd, cwd=None, timeout=600):
    p = subprocess.run(cmd, cwd=cwd, text=True, capture_output=True, timeout=timeout)
    return p.returncode, p.stdout, p.stderr

@celery_app.task(name="edulabops.grade_submission")
def grade_submission(submission_id: int):
    with engine.begin() as conn:
        row = conn.execute(
            text("SELECT id, repo_url, status, assignment_id FROM submissions WHERE id=:id"),
            {"id": submission_id},
        ).mappings().first()
        if not row:
            return {"id": submission_id, "error": "not_found"}

        conn.execute(text("UPDATE submissions SET status='running' WHERE id=:id"), {"id": submission_id})

        a = conn.execute(
            text("SELECT grader_image FROM assignments WHERE id=:id"),
            {"id": row["assignment_id"]},
        ).mappings().first()

        grader_image = (a["grader_image"] if a and a.get("grader_image") else "python:3.12-slim")

    workdir = tempfile.mkdtemp(prefix=f"sub_{submission_id}_")
    repo_dir = os.path.join(workdir, "repo")

    score = 0
    feedback = ""

    try:
        rc, out, err = _run(["git", "clone", "--depth", "1", row["repo_url"], repo_dir], timeout=300)
        if rc != 0:
            feedback = "GIT_CLONE_FAILED\n" + (err or out)
            with engine.begin() as conn:
                conn.execute(
                    text("UPDATE submissions SET status='failed', score=0, feedback=:fb WHERE id=:id"),
                    {"id": submission_id, "fb": feedback[:20000]},
                )
            return {"id": submission_id, "status": "failed"}

        _run(["docker", "pull", grader_image], timeout=600)

        test_cmd = "set -e; cd /work; if [ -f requirements.txt ]; then pip install -r requirements.txt; fi; if command -v pytest >/dev/null 2>&1; then pytest -q; else python -m pytest -q; fi"
        rc, out, err = _run(
            ["docker", "run", "--rm", "-v", f"{repo_dir}:/work", "-w", "/work", grader_image, "bash", "-lc", test_cmd],
            timeout=900,
        )

        combined = (out or "") + ("\n" + err if err else "")
        combined = combined.strip()

        if rc == 0:
            score = 100
            feedback = "TESTS_OK\n" + (combined if combined else "pytest ok")
            status = "done"
        else:
            score = 0
            feedback = "TESTS_FAILED\n" + (combined if combined else "pytest failed")
            status = "failed"

        with engine.begin() as conn:
            conn.execute(
                text("UPDATE submissions SET status=:st, score=:sc, feedback=:fb WHERE id=:id"),
                {"id": submission_id, "st": status, "sc": score, "fb": feedback[:20000]},
            )

        return {"id": submission_id, "status": status, "score": score}

    except Exception as e:
        feedback = "GRADER_EXCEPTION\n" + str(e)
        with engine.begin() as conn:
            conn.execute(
                text("UPDATE submissions SET status='failed', score=0, feedback=:fb WHERE id=:id"),
                {"id": submission_id, "fb": feedback[:20000]},
            )
        return {"id": submission_id, "status": "failed"}

    finally:
        shutil.rmtree(workdir, ignore_errors=True)