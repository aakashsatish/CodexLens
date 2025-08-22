import os
import sys

# Unused import (should be caught by ruff)
import json

# Hardcoded password (should be caught by bandit)
password = "secret123"

# Unused variable (should be caught by ruff)
unused_var = "hello"

def main():
    # Print statement (should be caught by ruff)
    print("Hello world")
    
    # Hardcoded password in function (should be caught by bandit)
    db_password = "admin123"
    
    return "success"

if __name__ == "__main__":
    main()