# 脚本
## Windows / Powershell

```powershell
# 常量

$TOKEN = <GITHUB TOKEN>
$OWNER = <GITHUB ACCOUNT>
$REPO = <GITHUB REPOSITORY>

$Headers = @{
    "Accept"               = "application/vnd.github+json"
    "Authorization"        = "Bearer $TOKEN"
    "X-GitHub-Api-Version" = "2022-11-28"
}

# 变量

$DL_URL = Read-Host -Prompt "Enter the link"

# 命令

if ($DL_URL -eq "") {
    Write-Host "Invalid url." -ForegroundColor Red
} else {
    Invoke-WebRequest -Uri "https://api.github.com/repos/${OWNER}/${REPO}/actions/variables/DL_URL" `
                      -Method PATCH `
                      -Headers $Headers `
                      -Body "{""name"":""DL_URL"",""value"":""${DL_URL}""}"
    Invoke-WebRequest -Uri "https://api.github.com/repos/${OWNER}/${REPO}/actions/workflows/transit.yml/dispatches" `
                      -Method POST `
                      -Headers $Headers `
                      -Body '{"ref":"main"}'
    Write-Host "Finished." -ForegroundColor Green
}
```

## Linux / Shell

```shell
# 常量

TOKEN=<GITHUB TOKEN>
OWNER=<GITHUB ACCOUNT>
REPO=<GITHUB REPOSITORY>

# 变量
echo -n "Enter the link: "
read DL_URL

# 命令

if [ "$DL_URL" == '' ]; then
  echo -e "\033[31mInvalid url.\033[0m"
else
  curl "https://api.github.com/repos/${OWNER}/${REPO}/actions/variables/DL_URL" \
       -L -X PATCH \
       -H "Accept: application/vnd.github+json" \
       -H "Authorization: Bearer ${TOKEN}" \
       -H "X-GitHub-Api-Version: 2022-11-28" \
       -d "{\"name\":\"DL_URL\",\"value\":\"${DL_URL}\"}"
  curl "https://api.github.com/repos/${OWNER}/${REPO}/actions/workflows/transit.yml/dispatches" \
       -L -X POST \
       -H "Accept: application/vnd.github+json" \
       -H "Authorization: Bearer ${TOKEN}" \
       -H "X-GitHub-Api-Version: 2022-11-28" \
       -d '{"ref":"main"}'
  echo -e "\033[32mFinished.\033[0m"
fi
```