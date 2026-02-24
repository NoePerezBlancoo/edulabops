function Invoke-HttpJson {
  param(
    [Parameter(Mandatory=$true)][string]$Url,
    [ValidateSet("GET","POST")][string]$Method = "GET",
    [hashtable]$Headers = $null,
    [object]$Body = $null
  )

  $params = @{
    UseBasicParsing = $true
    Uri            = $Url
    Method         = $Method
  }

  if ($Headers) { $params.Headers = $Headers }

  if ($null -ne $Body) {
    $params.ContentType = "application/json"
    $params.Body = ($Body | ConvertTo-Json -Depth 10)
  }

  try {
    $resp = Invoke-WebRequest @params
    if ($resp.Content) { return ($resp.Content | ConvertFrom-Json) }
    return $null
  } catch {
    $we = $_.Exception
    if ($we.Response -and $we.Response.GetResponseStream) {
      $sr = New-Object System.IO.StreamReader($we.Response.GetResponseStream())
      $raw = $sr.ReadToEnd()
      if ($raw) { return ($raw | ConvertFrom-Json) }
    }
    return @{ detail = "request_failed" }
  }
}

function Get-Token {
  param(
    [string]$Base,
    [string]$Email,
    [string]$Password,
    [string]$Role
  )

  $reg = Invoke-HttpJson -Method POST -Url "$Base/auth/register" -Body @{email=$Email;password=$Password;role=$Role}
  if ($reg.access_token) { return $reg.access_token }

  $log = Invoke-HttpJson -Method POST -Url "$Base/auth/login" -Body @{email=$Email;password=$Password}
  if ($log.access_token) { return $log.access_token }

  throw "No token for $Email"
}

$base = "http://localhost:8000"

$tokenTeacher = Get-Token -Base $base -Email "teacher@demo.com" -Password "123456" -Role "teacher"
$course = Invoke-HttpJson -Method POST -Url "$base/courses" -Headers @{Authorization="Bearer $tokenTeacher"} -Body @{name="DAW DevOps"}
$assignment = Invoke-HttpJson -Method POST -Url "$base/assignments" -Headers @{Authorization="Bearer $tokenTeacher"} -Body @{course_id=$course.id;title="Entrega 1";description="MVP";grader_image="python:3.12-slim"}

$tokenStudent = Get-Token -Base $base -Email "student@demo.com" -Password "123456" -Role "student"
$submission = Invoke-HttpJson -Method POST -Url "$base/submissions" -Headers @{Authorization="Bearer $tokenStudent"} -Body @{assignment_id=$assignment.id;repo_url="https://example.com/repo.git"}

Start-Sleep -Seconds 2
$result = Invoke-HttpJson -Method GET -Url "$base/submissions/$($submission.id)" -Headers @{Authorization="Bearer $tokenStudent"}
$result