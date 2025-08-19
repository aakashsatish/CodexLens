from fastapi import APIRouter, Request, HTTPException, Depends
from sqlalchemy.orm import Session
from apps.api.database import get_db
from apps.api.models import PullRequest
from apps.api.services.github import GitHubWebhookVerifier
import json
import os


router = APIRouter(prefix="/webhooks", tags=["webhooks"])

# Initialize verifier
verifier = GitHubWebhookVerifier(os.getenv('GITHUB_WEBHOOK_SECRET', ''))

@router.post("/github")
async def github_webhook(request: Request):
    """
    Handle GitHub webhook events for pull requests
    """
    # Read the raw body for signature verification
    body = await request.body()
    
    # Verify the webhook signature
    if not verifier.verify_signature(request, body):
        raise HTTPException(status_code=401, detail="Invalid webhook signature")
    
    # Parse the JSON payload
    payload = await request.json()
    
    # Log the event type for debugging
    event_type = request.headers.get('X-GitHub-Event')
    print(f"Received {event_type} event")

    # Store the pull request data if it's a PR event
    if event_type == "pull_request":
        pr_data = payload.get("pull_request", {})
        pr - PullRequest(
            github_id=pr_data.get("number"),
            repo_name=payload.get("repository", {}).get("full_name"),
            title=pr_data.get("title"),
            author=pr_data.get("user", {}).get("login"),
            state=pr_data.get("state"),
        )
        db.add(pr)
        db.commit()
        print(f"Stored pull request {pr.github_id} for {pr.repo_name}")

    return {"status": "received", "event": event_type}

@router.get("/github")
async def github_webhook_verification():
    """
    GitHub webhook verification endpoint
    """
    return {"status": "webhook endpoint ready"}