from apps.worker.celery_app import celery_app
from sqlalchemy.orm import Session
from apps.api.database import SessionLocal
from apps.api.models import PullRequest
import logging

logger = logging.getLogger(__name__)

@celery_app.task(bind=True, max_retries=3)
def review_pull_request(self, pr_github_id: int):
    """
    Background task to review a pull request
    
    Args:
        pr_github_id: GitHub ID of the PR to review
        self: Celery task instance (for retries)
    """
    try:
        # get database session
        db = SessionLocal()

        # find the pull request
        pr = db.query(PullRequest).filter(PullRequest.github_id == pr_github_id).first()
        if not pr: 
            logger.error(f"PR {pr_github_id} not found")
            return {"status": "error", "message": f"PR {pr_github_id} not found"}
        
        logger.info(f"Starting to review PR #{pr.pr_number} from {pr.repo_name}")
        
        #TODO: Implement the actual review logic here
        #1. Fetch PR from GitHub
        #2. Analyze the code with AI
        #3. Store the findings in the database
        #4. Send notifications to the maintainer

        logger.info(f"Review completed for PR #{pr.pr_number} from {pr.repo_name}")
        return {"status": "success", "message": f"Review completed for PR #{pr.pr_number} from {pr.repo_name}"}
    
    except Exception as exc:
        logger.error(f"Error reviewing PR {pr_github_id}: {str(exc)}", exc_info=True)
        
        #retry the task
        if self.request.retries < self.max_retries:
            logger.info(f"Retrying task for PR {pr_github_id} (attempt {self.request.retries + 1}/{self.max_retries})")
            raise self.retry(countdown=60, exc=exc) #wait 60 seconds before retrying
        
        return {"status": "error", "message": f"Error reviewing PR {pr_github_id}: {str(exc)}"}
    
    finally:
        db.close()