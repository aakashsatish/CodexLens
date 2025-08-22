#!/usr/bin/env python3
"""
AI-powered code review service.
"""

from typing import List, Dict, Any
import re

class AIReviewService:
    def __init__(self):
        self.severity_weights = {
            'error': 3,
            'warning': 2,
            'info': 1
        }
    
    def generate_review_comments(self, findings: List[Dict]) -> List[Dict]:
        """
        Generate intelligent review comments from static analysis findings.
        """
        if not findings:
            return []
        
        # Group findings by file and line
        grouped_findings = self._group_findings_by_location(findings)
        
        # Generate comments for each group
        comments = []
        for (file_path, line), file_findings in grouped_findings.items():
            comment = self._generate_comment_for_location(file_path, line, file_findings)
            if comment:
                comments.append(comment)
        
        return comments
    
    def _group_findings_by_location(self, findings: List[Dict]) -> Dict:
        """Group findings by file path and line number."""
        grouped = {}
        for finding in findings:
            key = (finding['path'], finding['line'])
            if key not in grouped:
                grouped[key] = []
            grouped[key].append(finding)
        return grouped
    
    def _generate_comment_for_location(self, file_path: str, line: int, findings: List[Dict]) -> Dict:
        """Generate a single comment for a specific file location."""
        # Sort findings by severity
        sorted_findings = sorted(findings, key=lambda f: self.severity_weights.get(f['severity'], 0), reverse=True)
        
        # Generate comment body
        comment_body = self._create_comment_body(sorted_findings)
        
        return {
            'path': file_path,
            'line': line,
            'body': comment_body,
            'position': line  # GitHub API expects position
        }
    
    def _create_comment_body(self, findings: List[Dict]) -> str:
        """Create the comment body with findings and suggestions."""
        comment_lines = []
        
        # Header
        comment_lines.append("🔍 **CodexLens AI Review**")
        comment_lines.append("")
        
        # Summary
        total_issues = len(findings)
        severity_counts = {}
        for finding in findings:
            severity = finding['severity']
            severity_counts[severity] = severity_counts.get(severity, 0) + 1
        
        comment_lines.append(f"Found **{total_issues} issue(s)** on this line:")
        for severity, count in severity_counts.items():
            emoji = "🔴" if severity == "error" else "🟡" if severity == "warning" else "🔵"
            comment_lines.append(f"- {emoji} **{count} {severity}(s)**")
        comment_lines.append("")
        
        # Individual findings
        for i, finding in enumerate(findings, 1):
            emoji = "��" if finding['severity'] == "error" else "��" if finding['severity'] == "warning" else "🔵"
            comment_lines.append(f"### {i}. {emoji} {finding['tool'].upper()} - {finding['severity'].upper()}")
            comment_lines.append(f"**Code:** `{finding['code']}`")
            comment_lines.append(f"**Message:** {finding['message']}")
            
            # Add suggestions based on the issue type
            suggestion = self._get_suggestion_for_issue(finding)
            if suggestion:
                comment_lines.append(f"**💡 Suggestion:** {suggestion}")
            
            comment_lines.append("")
        
        # Footer
        comment_lines.append("---")
        comment_lines.append("*Powered by CodexLens AI Code Review*")
        
        return "\n".join(comment_lines)
    
    def _get_suggestion_for_issue(self, finding: Dict) -> str:
        """Get helpful suggestions based on the issue type."""
        tool = finding['tool']
        code = finding['code']
        message = finding['message']
        
        suggestions = {
            'ruff': {
                'F401': 'Remove unused import or use it in your code.',
                'F841': 'Remove the unused variable or use it in your code.',
                'E501': 'Break the long line into multiple lines or use line continuation.',
                'E302': 'Add two blank lines before this class/function definition.',
                'E303': 'Remove extra blank lines.',
            },
            'bandit': {
                'B101': 'Use assert statements only for debugging, not for production logic.',
                'B102': 'Avoid using exec() as it can execute arbitrary code.',
                'B103': 'Avoid using set_badkey() as it can be a security risk.',
                'B104': 'Avoid using hardcoded bind addresses.',
                'B105': 'Use environment variables or secure configuration for passwords.',
                'B106': 'Avoid using hardcoded passwords in source code.',
                'B107': 'Avoid using hardcoded passwords in source code.',
            }
        }
        
        # Return specific suggestion if available
        if tool in suggestions and code in suggestions[tool]:
            return suggestions[tool][code]
        
        # Return generic suggestion based on tool
        if tool == 'ruff':
            return 'Consider following Python style guidelines (PEP 8).'
        elif tool == 'bandit':
            return 'Review this code for potential security vulnerabilities.'
        else:
            return 'Review this code for potential issues.'