from apps.worker.celery_app import celery_app
from sqlalchemy.orm import Session
from apps.api.database import SessionLocal
from apps.api.models import PullRequest, Finding
from apps.api.services.github_api import GitHubAPIClient
from apps.api.services.static_analysis import StaticAnalyzer
from typing import List, Dict
import logging
import asyncio 

logger = logging.getLogger(__name__)

@celery_app.task(bind=True, max_retries=3)
def review_pull_request(self, pr_id: int, repo_name: str, pr_number: int, installation_id: int):
    """
    Review pull request using static analysis and AI-based analysis.
    """
    try:
        # Get database session
        db = SessionLocal()

        print(f"Reviewing PR {pr_number} in {repo_name}")

        # Parse repo name into owner and repo
        owner, repo = repo_name.split('/', 1)

        # Initialize GitHub client
        github_client = GitHubAPIClient()

        # Create new event loop for async operations
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        try:
            pr_details = loop.run_until_complete(
                github_client.get_pull_request(owner, repo, pr_number, installation_id)
            )
            print(f"PR Title: {pr_details.get('title', 'Unknown')}")

            pr_files = loop.run_until_complete(
                github_client.get_pull_request_files(owner, repo, pr_number, installation_id)
            )
            print(f"Found {len(pr_files)} files to analyze")

            analyzer = StaticAnalyzer()
            all_findings = []

            for file_info in pr_files:
                filename = file_info['filename']
                file_url = file_info['contents_url']

                # Only analyze Python files
                if filename.endswith('.py'):
                    print(f"Analyzing {filename}")
                    
                    file_content = loop.run_until_complete(
                        github_client.get_file_content(file_url, installation_id)
                    )

                    if file_content:
                        # Run static analysis
                        findings = analyzer.analyze_file(filename, file_content)
                        all_findings.extend(findings)
                        print(f"Found {len(findings)} issues in {filename}")

            print(f"Found {len(all_findings)} issues in total")

            # Store findings in database
            for finding in all_findings:
                db_finding = Finding(
                    pr_github_id=pr_id, 
                    tool=finding['tool'], 
                    severity=finding['severity'], 
                    path=finding['path'],
                    line=finding['line'],
                    message=finding['message'],
                    code=finding['code']
                )
                db.add(db_finding)
            
            db.commit()
            print(f"Stored {len(all_findings)} findings in database")

            # TODO: Generate review comments
            # TODO: Post comments to GitHub

            print(f"Review completed for PR {pr_number} in {repo_name}")

        finally:
            loop.close()

    except Exception as exc:
        print(f"Error reviewing PR {pr_number} in {repo_name}: {exc}")
        db.rollback()
        raise self.retry(countdown=60, exc=exc)

    finally:
        db.close()

def _generate_review_comments(self, findings: List[Dict]) -> List[Dict]:
    """Convert findings into GitHub review comments"""
    # Implementation will go here
    pass