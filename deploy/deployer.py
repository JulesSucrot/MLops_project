import os, subprocess
from fastapi import FastAPI, Header, HTTPException

SECRET = os.getenv("WEBHOOK_SECRET","change-me")
app = FastAPI(title="Local Deployer")

@app.post("/deploy")
def deploy(x_token: str = Header(None)):
    if x_token != SECRET:
        raise HTTPException(status_code=403, detail="forbidden")
    # exécuter le script PowerShell
    cmd = ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", "deploy/deploy.ps1"]
    subprocess.run(cmd, check=True)
    return {"status":"ok"}
