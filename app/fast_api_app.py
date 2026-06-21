# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.agent import app as student_concierge_app

app = FastAPI(title="Student Life Concierge API")


class UserRequestPayload(BaseModel):
    user_input: str
    user_id: str


@app.get("/")
def health_check():
    """Baseline health-check to prevent background container handshake timeouts."""
    return {"status": "ok"}


@app.post("/chat")
def chat(payload: UserRequestPayload):
    """Exposes chat interactions with the student_concierge_hub."""
    input_str = payload.user_input.lower()
    
    # Prompt injection check to block agent from automatic execution
    # and direct the user to a manual approval state.
    if "ignore previous rules" in input_str or "bypass criteria" in input_str:
        return {
            "status": "manual-approval",
            "message": "Potential policy override detected. Action blocked pending manual review.",
            "requires_review": True
        }

    # Run the student concierge hub application
    try:
        response = student_concierge_app.run(
            input=payload.user_input,
            session_id=payload.user_id
        )
        return {"status": "success", "response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
