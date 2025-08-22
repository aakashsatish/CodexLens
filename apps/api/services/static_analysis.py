import subprocess
import json
from typing import List, Dict
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

class StaticAnalyzer:
    def __init__(self):
        self.supported_languages = ['python', 'javascript', 'typescript']
        self.tools = ['ruff', 'bandit', 'semgrep']
        
    def analyze_file(self, file_path: str, content: str) -> List[Dict]:
        """
        Analyze a single file with all available static analysis tools.
        
        Args:
            file_path: Path to the file to analyze
            
        Returns:
            List of findings in standardized format
        """
        findings = []

        # Only Python files for now
        if not file_path.endswith('.py'):
            logger.info(f"Skipping non-Python file: {file_path}")
            return findings
        
        logger.info(f"Analyzing {file_path}")

        for tool in self.tools:
            try:
                if tool == 'ruff':
                    findings.extend(self.run_ruff(file_path))
                elif tool == 'bandit':
                    findings.extend(self.run_bandit(file_path))
                elif tool == 'semgrep':
                    findings.extend(self.run_semgrep(file_path))
            except Exception as e:
                logger.error(f"Error running {tool} on {file_path}: {e}")
        logger.info(f"Found {len(findings)} findings in {file_path}")
        return findings
    
    def run_ruff(self, file_path: str) -> List[Dict]:
        """Run ruff linter on a file."""
        try:
            result = subprocess.run(
                ['ruff', 'check', file_path, '--output-format=json'],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                return []  # No issues found
            
            # Parse ruff output
            issues = json.loads(result.stdout)
            findings = []
            
            for issue in issues:
                findings.append({
                    'tool': 'ruff',
                    'severity': self._map_ruff_severity(issue.get('code', '')),
                    'message': issue.get('message', ''),
                    'path': file_path,
                    'line': issue.get('location', {}).get('row', 0),
                    'column': issue.get('location', {}).get('column', 0),
                    'code': issue.get('code', '')
                })
            
            return findings
            
        except subprocess.TimeoutExpired:
            logger.warning(f"Ruff timed out for {file_path}")
            return []
        except Exception as e:
            logger.error(f"Error running ruff on {file_path}: {e}")
            return []
        
    def run_bandit(self, file_path: str) -> List[Dict]:
        """Run bandit security scanner on a file."""
        try:
            result = subprocess.run(
                ['bandit', '-f', 'json', '-r', file_path],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            # Parse bandit output
            output = json.loads(result.stdout)
            findings = []
            
            for issue in output.get('results', []):
                findings.append({
                    'tool': 'bandit',
                    'severity': self._map_bandit_severity(issue.get('issue_severity', '')),
                    'message': issue.get('issue_text', ''),
                    'path': file_path,
                    'line': issue.get('line_number', 0),
                    'column': 0,  # Bandit doesn't provide column info
                    'code': issue.get('test_id', '')
                })
            
            return findings
            
        except subprocess.TimeoutExpired:
            logger.warning(f"Bandit timed out for {file_path}")
            return []
        except Exception as e:
            logger.error(f"Error running bandit on {file_path}: {e}")
            return []
        
    def run_semgrep(self, file_path: str) -> List[Dict]:
        """Run semgrep pattern matcher on a file."""
        try:
            result = subprocess.run(
                ['semgrep', '--json', '--config=auto', file_path],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            # Parse semgrep output
            output = json.loads(result.stdout)
            findings = []
            
            for result_item in output.get('results', []):
                findings.append({
                    'tool': 'semgrep',
                    'severity': self._map_semgrep_severity(result_item.get('extra', {}).get('severity', '')),
                    'message': result_item.get('extra', {}).get('message', ''),
                    'path': file_path,
                    'line': result_item.get('start', {}).get('line', 0),
                    'column': result_item.get('start', {}).get('col', 0),
                    'code': result_item.get('check_id', '')
                })
            
            return findings
        except subprocess.TimeoutExpired:
            logger.warning(f"Semgrep timed out for {file_path}")
            return []
        except Exception as e:
            logger.error(f"Error running semgrep on {file_path}: {e}")
            return []

    def _map_ruff_severity(self, code: str) -> str:
        """Map ruff codes to severity levels."""
        if code.startswith('E'):
            return 'error'
        elif code.startswith('W'):
            return 'warning'
        else:
            return 'info'
        
    def _map_bandit_severity(self, severity: str) -> str:
        """Map bandit severity levels."""
        severity_map = {
            'LOW': 'info',
            'MEDIUM': 'warning',
            'HIGH': 'error'
        }
        return severity_map.get(severity.upper(), 'info')
    
    def _map_semgrep_severity(self, severity: str) -> str:
        """Map semgrep severity levels."""
        severity_map = {
            'ERROR': 'error', 
            'WARNING': 'warning',
            'INFO': 'info'
        }
        return severity_map.get(severity.upper(), 'info')