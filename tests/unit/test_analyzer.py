#!/usr/bin/env python3
"""
Test script for the static analysis service.
"""

import sys
import os
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from apps.api.services.static_analysis import StaticAnalyzer
import json

def test_static_analysis():
    """Test the static analyzer with our test file."""
    
    # Create analyzer instance
    analyzer = StaticAnalyzer()
    
    # Test file path (relative to project root)
    test_file = "tests/unit/test_file.py"
    
    print(f"Testing static analysis on: {test_file}")
    print("=" * 50)
    
    # Run analysis
    findings = analyzer.analyze_file(test_file, "")
    
    # Display results
    if findings:
        print(f"Found {len(findings)} issues:")
        print()
        
        for i, finding in enumerate(findings, 1):
            print(f"{i}. {finding['tool'].upper()} - {finding['severity'].upper()}")
            print(f"   File: {finding['path']}:{finding['line']}")
            print(f"   Message: {finding['message']}")
            print(f"   Code: {finding['code']}")
            print()
    else:
        print("No issues found!")
    
    # Show summary by tool
    tool_counts = {}
    for finding in findings:
        tool = finding['tool']
        tool_counts[tool] = tool_counts.get(tool, 0) + 1
    
    print("Summary by tool:")
    for tool, count in tool_counts.items():
        print(f"   {tool}: {count} issues")
    
    return findings

if __name__ == "__main__":
    test_static_analysis()