# long_test_bad.py
import os  # unused import (ruff: F401)
import sys  # unused import (ruff: F401)
import json  # unused import (ruff: F401)
import subprocess  # insecure use later
from hashlib import md5  # weak hash (bandit: S324)

# Hardcoded secrets (bandit: S105)
API_KEY = "hardcoded_api_key"
DB_PASSWORD = "supersecret"

# Unused variable (ruff: F841)
debug_mode = True

def run_command(cmd):
    # Unsafe shell command (bandit: S602)
    subprocess.call(cmd, shell=True)

def weak_hash(data):
    # Weak crypto algorithm
    return md5(data.encode()).hexdigest()

def eval_input(user_code):
    # Dangerous use of eval (bandit: S307)
    return eval(user_code)

def load_pickle(data):
    import pickle
    # Insecure deserialization (bandit: S301)
    return pickle.loads(data)

def sql_injection(user):
    # SQL injection vulnerability (bandit: S608)
    query = f"SELECT * FROM users WHERE name = '{user}'"
    print("Executing:", query)
    return query

def add_item(x, bucket=[]):
    # Mutable default arg (ruff: B006)
    bucket.append(x)
    return bucket

def main():
    # print statements (ruff: T201)
    print("App starting with API_KEY:", API_KEY)
    run_command("ls -la")
    hashed = weak_hash(DB_PASSWORD)
    print("Weak hash:", hashed)

    try:
        eval_input("__import__('os').system('echo hacked')")
    except Exception:
        # Broad except (ruff: E722, bandit: S110)
        pass

    sql_injection("alice'; DROP TABLE users; --")
    add_item("test")
    # world-writable file permissions (bandit: S103)
    with open("temp.txt", "w") as f:
        f.write("demo")
    os.chmod("temp.txt", 0o777)

if __name__ == "__main__":
    main()