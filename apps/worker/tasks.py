from apps.worker.celery_app import celery_app
from sqlalchemy.orm import Session
from apps.api.database import SessionLocal
from apps.api.models import PullRequest
from apps.api.services.github_api import GitHubAPIClient
from apps.api.services.static_analysis import StaticAnalyzer
from typing import List, Dict
import logging

logger = logging.getLogger(__name__)

@celery_app.task(bind=True, max_retries=3)
async def review_pull_request(self, pr_github_id: int):
    """Enhanced background task to review a pull request"""
    try:
        # Get database session
        db = SessionLocal()
        
        # Find the PR
        pr = db.query(PullRequest).filter(
            PullRequest.github_id == pr_github_id
        ).first()
        
        if not pr:
            logger.error(f"PR {pr_github_id} not found in database")
            return {"status": "error", "message": "PR not found"}
        
        logger.info(f"Starting comprehensive review for PR #{pr.pr_number}")
        
        # Initialize services
        github_client = GitHubAPIClient()
        analyzer = StaticAnalyzer()
        
        # 1. Fetch PR details from GitHub
        pr_details = await github_client.get_pull_request(
            owner=pr.repo_name.split('/')[0],
            repo=pr.repo_name.split('/')[1],
            pr_number=pr.pr_number
        )
        
        # 2. Get changed files
        changed_files = await github_client.get_pull_request_files(
            owner=pr.repo_name.split('/')[0],
            repo=pr.repo_name.split('/')[1],
            pr_number=pr.pr_number
        )
        
        # 3. Run static analysis on each file
        all_findings = []
        for file_info in changed_files:
            if file_info['status'] in ['added', 'modified']:
                findings = await analyzer.analyze_file(
                    file_info['filename'],
                    file_info.get('patch', '')
                )
                all_findings.extend(findings)
        
        # 4. Generate review comments
        review_comments = self._generate_review_comments(all_findings)
        
        # 5. Post comments to GitHub
        if review_comments:
            await github_client.post_review_comment(
                owner=pr.repo_name.split('/')[0],
                repo=pr.repo_name.split('/')[1],
                pr_number=pr.pr_number,
                comments=review_comments
            )
        
        logger.info(f"Review completed for PR #{pr.pr_number} - {len(all_findings)} findings")
        return {
            "status": "success", 
            "pr_number": pr.pr_number,
            "findings_count": len(all_findings)
        }
        
    except Exception as exc:
        logger.error(f"Error reviewing PR {pr_github_id}: {exc}")
        if self.request.retries < self.max_retries:
            raise self.retry(countdown=60, exc=exc)
        return {"status": "error", "message": str(exc)}
    
    finally:
        db.close()

def _generate_review_comments(self, findings: List[Dict]) -> List[Dict]:
    """Convert findings into GitHub review comments"""
    # Implementation will go here
    pass