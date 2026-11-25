
from fastapi import FastAPI, HTTPException

from run_all import main
from db import get_latest_briefing

app = FastAPI(
    title="OmniScope API",
    description="API for OmniScope research platform",
    version="1.0"
)


@app.get("/")
def home():
    return {
        "message": "OmniScope API is running",
        "status": "online"
    }


@app.post("/run")
def run_research():

    try:
        # Run all three agents and the coordinator
        main()

        # Retrieve the newly generated briefing
        latest = get_latest_briefing()

        if not latest:
            raise HTTPException(
                status_code=500,
                detail="Research completed but no briefing was saved."
            )

        return {
            "status": "success",
            "message": "OmniScope research completed",
            "briefing": latest["briefing"],
            "created_at": latest["created_at"]
        }

    except HTTPException:
        raise

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=str(error)
        )


@app.get("/latest")
def get_latest():

    latest = get_latest_briefing()

    if not latest:
        raise HTTPException(
            status_code=404,
            detail="No briefing available yet."
        )

    return {
        "status": "success",
        "briefing": latest["briefing"],
        "created_at": latest["created_at"]
    }
