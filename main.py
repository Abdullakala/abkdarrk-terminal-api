from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import subprocess

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

SECRET_CODE = "123123"

class TerminalRequest(BaseModel):
    command: str
    code: str

@app.post("/terminal")
def execute_terminal(data: TerminalRequest):
    if data.code != SECRET_CODE:
        raise HTTPException(status_code=403, detail="Invalid code")
    try:
        result = subprocess.run(data.command, shell=True, capture_output=True, text=True)
        return {"stdout": result.stdout, "stderr": result.stderr}
    except Exception as e:
        return {"error": str(e)}
