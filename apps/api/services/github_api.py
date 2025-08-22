import httpx
import jwt
import time
from typing import Dict, List, Optional
import os
from dotenv import load_dotenv
import logging

load_dotenv('infra/.env')
logger = logging.getLogger(__name__)

class GitHubAPIClient:
    def __init__(self):
        self.app_id = os.getenv('GITHUB_APP_ID')
        self.private_key_path = os.path.expanduser(os.getenv('GITHUB_PRIVATE_KEY_PATH'))
        self.base_url = "https://api.github.com"

        if not self.app_id or not self.private_key_path:
            raise ValueError("GITHUB_APP_ID and GITHUB_PRIVATE_KEY_PATH must be set")

    def _load_private_key(self) -> str:
        """Load private key from file"""

        try: 
            with open(self.private_key_path, 'r') as f:
                return f.read()
        except FileNotFoundError:
            logger.error(f"Private key file not found at {self.private_key_path}")
            raise 
        except Exception as e:
            logger.error(f"Error loading private key: {e}")
            raise
        
    def _generate_jwt(self) -> str:
        """Generate JWT token for GitHub App authentication"""
        try:
            private_key = self._load_private_key()

            # JWT payload for GitHub App authentication
            payload = {
                'iat': int(time.time()), 
                'exp': int(time.time()) + 600, #10 minutes
                'iss': self.app_id
            }

            #Sign the JWT
            token = jwt.encode(payload, private_key, algorithm='RS256')
            logger.debug("JWT token generated successfully")
            return token
        
        except Exception as e:
            logger.error(f"Error generating JWT token: {e}")
            raise
        
    async def _get_installation_token(self, installation_id: int) -> str:
        """Get installation access token"""
        try:
            jwt_token = self._generate_jwt()

            headers = {
                'Authorization': f'Bearer {jwt_token}',
                'Accept': 'application/vnd.github.v3+json'
            }

            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/app/installations/{installation_id}/access_tokens",
                    headers=headers
                )

                response.raise_for_status()

                data = response.json()
                logger.debug(f"Installation token retrieved for installation {installation_id}")
                return data['token']
            
        except Exception as e:
            logger.error(f"Error getting installation token: {e}")
            raise

    async def get_pull_request(self, owner: str, repo: str, pr_number: int, installation_id: int) -> Dict:
        """Fetch pull request details"""
        try: 
            token = await self._get_installation_token(installation_id)

            headers = {
                'Authorization': f'token {token}',
                'Accept': 'application/vnd.github.v3+json'
            }

            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/repos/{owner}/{repo}/pulls/{pr_number}",
                    headers=headers
                )

                response.raise_for_status()

                data = response.json()
                logger.debug(f"Pull request {pr_number} retrieved from {owner}/{repo}")
                return data
            
        except Exception as e:
            logger.error(f"Error getting pull request {pr_number} from {owner}/{repo}: {e}")
            raise
        
        
    async def get_pull_request_files(self, owner: str, repo: str, pr_number: int, installation_id: int) -> List[Dict]:
        """Fetch files changed in pull request"""
        try:
            token = await self._get_installation_token(installation_id)

            headers = {
                'Authorization': f'token {token}',
                'Accept': 'application/vnd.github.v3+json'
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/repos/{owner}/{repo}/pulls/{pr_number}/files",
                    headers=headers
                )

                response.raise_for_status()

                data = response.json()
                logger.info(f"Fetched {len(data)} files for PR #{pr_number} in {owner}/{repo}")
                return data
            
        except Exception as e:
            logger.error(f"Error getting pull request files for PR #{pr_number} in {owner}/{repo}: {e}")
            raise

    async def get_file_content(self, file_url: str, installation_id: int) -> str:
        """Get the content of a file from GitHub"""
        try:
            # Get installation token
            token  = await self._get_installation_token(installation_id)
            
            # Make request to get file content
            headers = {
                'Authorization': f'token {token}',
                'Accept': 'application/vnd.github.v3.raw'
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.get(file_url, headers=headers)
                response.raise_for_status()
                return response.text
                
        except Exception as e:
            logger.error(f"Error getting file content: {e}")
            raise
        
        
    async def post_review_comment(self, owner: str, repo: str, pr_number: int, 
                                 comments: List[Dict]) -> Dict:
        """Post review comments to pull request"""
        # Implementation will go here
        pass