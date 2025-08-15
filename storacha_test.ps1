# storacha_test.ps1

# 0) Optional: activate venv
# & .\.venv\Scripts\Activate.ps1

# 1) Confirm CLI
if (-not (Get-Command storacha -ErrorAction SilentlyContinue)) { throw "storacha CLI not found. npm i -g @storacha/cli" }

# 2) Your Space DID
$spaceDid = "did:key:z6MkkYs8Hoo6cXHbfjH7mQPKzVz7D6hz4nBjCyNRxmCcqsCA"
Write-Host $spaceDid

# 3) 24h expiration (UNIX seconds)
$exp = [int][double]((Get-Date).ToUniversalTime().AddHours(24) - (Get-Date "1970-01-01Z")).TotalSeconds
Write-Host "Expiration (exp): $exp"

# 4) Single-line token generation (avoid backtick issues)
$tokens = storacha bridge generate-tokens $spaceDid --can "store/add" --can "upload/add" --can "upload/list" --expiration $exp

# 5) Tight parsing (stop at base64url chars only)
$secret = [regex]::Match($tokens, "X-Auth-Secret header:\s*([A-Za-z0-9\-_]+)", "Singleline").Groups[1].Value.Trim()
$auth   = [regex]::Match($tokens, "Authorization header:\s*([A-Za-z0-9\-_\.]+)", "Singleline").Groups[1].Value.Trim()

if (-not $secret -or -not $auth) {
  Write-Error "Could not parse headers from CLI output"; $tokens | Out-Host; throw "Token parse failed"
}
if ($secret -notmatch '^[A-Za-z0-9\-_]+$') { throw "STORACHA_SECRET contains non-base64url characters." }
if ($auth   -notmatch '^[A-Za-z0-9\-_\.]+$') { throw "STORACHA_AUTH contains invalid characters." }

# 6) Export env for this PowerShell session
$env:STORACHA_ENABLED    = "True"
$env:STORACHA_BRIDGE_URL = "https://up.storacha.network/bridge"
$env:STORACHA_SPACE_DID  = $spaceDid
$env:STORACHA_SECRET     = $secret
$env:STORACHA_AUTH       = $auth

# 7) Minimal leak-safe print
Write-Host ("STORACHA_SECRET: {0}… (len={1}) …{2}" -f $secret.Substring(0,6), $secret.Length, $secret.Substring($secret.Length-4))
Write-Host ("STORACHA_AUTH  : {0}… (len={1}) …{2}" -f $auth.Substring(0,6),   $auth.Length,   $auth.Substring($auth.Length-4))
Write-Host "PWD: $((Get-Location).Path)"

# 8) Run Django command from project ROOT
python manage.py storacha_list