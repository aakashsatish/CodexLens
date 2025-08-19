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
    
    # Debug: Print the signature header
    signature_header = request.headers.get('X-Hub-Signature-256')
    print(f"Debug: Signature header: {signature_header}")
    print(f"Debug: Body length: {len(body)}")
    print(f"Debug: First 100 chars of body: {body[:100]}")
    
    # Verify the webhook signature
    if not verifier.verify_signature(request, body):
        print("Debug: Signature verification failed")
        raise HTTPException(status_code=401, detail="Invalid webhook signature")
    
    print("Debug: Signature verification passed")
    
    # Parse the JSON payload
    payload = await request.json()
    
    # Log the event type for debugging
    event_type = request.headers.get('X-GitHub-Event')
    print(f"Received {event_type} event")
    
    # Handle pull request events
    if event_type == 'pull_request':
        print(f"Stored PR #{payload['number']} from {payload['repository']['full_name']}")
        return {"status": "PR processed"}
    
    return {"status": "webhook received"}

@router.get("/github")
async def github_webhook_verification():
    """
    GitHub webhook verification endpoint
    """
    return {"status": "webhook endpoint ready"}