from fastapi import APIRouter, Request, HTTPException, Depends
from typing import Dict, Any
import os
from dotenv import load_dotenv
from sqlalchemy.orm import Session
from apps.api.database import get_db
from apps.api.models import PullRequest
from apps.api.services.github import GitHubWebhookVerifier

# Load environment variables
load_dotenv('infra/.env')

router = APIRouter(prefix="/webhooks", tags=["webhooks"])

# Initialize verifier with the loaded secret
webhook_secret = os.getenv('GITHUB_WEBHOOK_SECRET', '')
print(f"Debug: Loaded webhook secret: {webhook_secret}")
verifier = GitHubWebhookVerifier(webhook_secret)

@router.post("/github")
async def github_webhook(request: Request, db: Session = Depends(get_db)):
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
    
    # Handle pull request events
    if event_type == 'pull_request':
        pr_data = payload['pull_request']
        
        # Create or update PR record
        db_pr = db.query(PullRequest).filter(
            PullRequest.github_id == pr_data['id']
        ).first()
        
        if not db_pr:
            db_pr = PullRequest(
                github_id=pr_data['id'],
                pr_number=pr_data['number'],
                title=pr_data['title'],
                repo_name=payload['repository']['full_name'],
                state=pr_data['state'],
                action=payload['action']
            )
            db.add(db_pr)
            print(f"Created new PR #{pr_data['number']} from {payload['repository']['full_name']}")
        else:
            db_pr.state = pr_data['state']
            db_pr.action = payload['action']
            print(f"Updated PR #{pr_data['number']} from {payload['repository']['full_name']}")
        
        db.commit()
        return {"status": "PR processed and stored"}
    
    return {"status": "webhook received"}