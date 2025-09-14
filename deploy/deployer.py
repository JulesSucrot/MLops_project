import os, subprocess
from fastapi import FastAPI, Header, HTTPException

app = FastAPI()
SECRET = os.getenv("WEBHOOK_SECRET", "")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/deploy")
def deploy(x_token: str = Header(default="")):
    if x_token != SECRET:
        raise HTTPException(status_code=403, detail="forbidden")
    # Lance le script PowerShell
    cmd = ["powershell","-NoProfile","-ExecutionPolicy","Bypass","-File","deploy/deploy.ps1"]
    subprocess.run(cmd, check=True)
    return {"status":"deploying"}
