function iwrb { param([Parameter(ValueFromRemainingArguments=$true)]$Args) Invoke-WebRequest -UseBasicParsing @Args }

(iwrb http://localhost:8000/health).Content
(iwrb http://localhost:8000/openapi.json).Content.Length
powershell -ExecutionPolicy Bypass -File .\scripts\demo.ps1