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
        """
        signature_header = request.headers.get('X-Hub-Signature-256')
        if not signature_header:
            print("Debug: No signature header found")
            return False
            
        # GitHub sends signature as: sha256=<hash>
        expected_signature = signature_header.replace('sha256=', '')
        print(f"Debug: Expected signature: {expected_signature}")
        print(f"Debug: Webhook secret: {self.webhook_secret}")
        
        # Calculate the signature
        calculated_signature = hmac.new(
            self.webhook_secret,
            body,
            hashlib.sha256
        ).hexdigest()
        print(f"Debug: Calculated signature: {calculated_signature}")
        
        # Compare signatures
        is_valid = hmac.compare_digest(expected_signature, calculated_signature)
        print(f"Debug: Signatures match: {is_valid}")
        print(f"Debug: Expected length: {len(expected_signature)}")
        print(f"Debug: Calculated length: {len(calculated_signature)}")
        
        return is_valid