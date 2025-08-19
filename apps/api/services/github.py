import hmac
import hashlib
from typing import Optional
from fastapi import HTTPException, Request

class GitHubWebhookVerifier:
    def __init__(self, webhook_secret: str):
        self.webhook_secret = webhook_secret.encode('utf-8')
    
    def verify_signature(self, request: Request, body: bytes) -> bool:
        """
        Verify GitHub webhook signature using HMAC-SHA256
        
        Args:
            request: FastAPI request object
            body: Raw request body
            
        Returns:
            True if signature is valid, False otherwise
        """
        signature_header = request.headers.get('X-Hub-Signature-256')
        if not signature_header:
            return False
            
        # GitHub sends signature as: sha256=<hash>
        expected_signature = signature_header.replace('sha256=', '')
        
        # Calculate our signature
        calculated_signature = hmac.new(
            self.webhook_secret,
            body,
            hashlib.sha256
        ).hexdigest()
        
        return hmac.compare_digest(expected_signature, calculated_signature)
