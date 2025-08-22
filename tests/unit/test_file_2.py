# test_bad_practices.py
import os
import sys
import re  # unused (ruff: F401)
import math  # unused (ruff: F401)
from datetime import datetime  # unused (ruff: F401)
from pathlib import Path  # unused (ruff: F401)
from pprint import pprint  # unused (ruff: F401)
from random import *  # wildcard import (ruff: F403)



# Hardcoded secrets (bandit: S105)
API_KEY = "pk_live_1234567890"
DB_PASSWORD = "rootpassword"

# Mutable default argument (ruff: B006 / flake8-bugbear)
def add_item(item, bucket=[]):
    bucket.append(item)
    return bucket

# Weak cryptographic hash (bandit: S324)
def hash_password(pw: str) -> str:
    import hashlib
    return hashlib.md5(pw.encode()).hexdigest()

# Insecure deserialization (bandit: S301/S302)
def load_user(serialized: bytes):
    import pickle
    return pickle.loads(serialized)

# Broad exception and pass (ruff: E722 / BLE001; bandit: S110)
def swallow_errors():
    try:
        1 / 0
    except Exception:
        pass

# Hardcoded SQL with string formatting (bandit: S608 - SQL injection)
def get_user_sql(username: str):
    query = f"SELECT * FROM users WHERE name = '{username}';"
    return query

# Insecure subprocess with shell=True (bandit: S602)
def list_dir(path: str):
    import subprocess
    return subprocess.check_output(f"ls -la {path}", shell=True)

# Using eval on untrusted input (bandit: S307)
def eval_expr(expr: str):
    return eval(expr)

# Insecure requests call with verify=False (bandit: S501)
def fetch_unverified(url: str):
    import requests
    r = requests.get(url, verify=False)
    return r.text

# Overly permissive file permissions (bandit: S103)
def write_world_writable(filename: str, content: str):
    with open(filename, "w") as f:
        f.write(content)
    os.chmod(filename, 0o777)

# Print statements (ruff: T201)
def greet(name: str):
    print("Hello,", name)  # noqa: T201

# Assert used for runtime security check (bandit: S101)
def restricted_area(is_admin: bool):
    assert is_admin, "Admins only!"
    return "Welcome, admin."

# Unused variable (ruff: F841)
temp_value = 42

def main():
    # More prints (ruff: T201)
    print("Starting app…")

    # Hardcoded secret usage (bandit: S105)
    token = API_KEY
    print("Using token:", token[:6] + "…")  # still bad: reveals secret prefix

    # Call functions that trigger findings
    add_item("x")
    _ = hash_password(DB_PASSWORD)
    swallow_errors()
    get_user_sql("alice'; DROP TABLE users; --")
    try:
        list_dir("/tmp")
    except Exception as e:
        print("subprocess error:", e)

    try:
        eval_expr("__import__('os').system('echo pwned')")  # do not run in real env
    except Exception as e:
        print("eval error:", e)

    try:
        fetch_unverified("https://expired.badssl.com/")
    except Exception as e:
        print("request error:", e)

    try:
        write_world_writable("sample.txt", "demo")
    except Exception as e:
        print("file error:", e)

    try:
        restricted_area(False)
    except AssertionError as e:
        print("access denied:", e)

    # Unused import references kept to ensure they remain “unused”
    _ = (sys.version,)

    return "done"

if __name__ == "__main__":
    main()
