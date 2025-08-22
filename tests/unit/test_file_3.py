# test_insecure_example_2.py
import os
import sys
import json  # unused (ruff: F401)
import tempfile
import sqlite3
import subprocess  # used insecurely
from typing import *  # wildcard (ruff: F403)
from hashlib import sha1  # weak/hash misuse
import random  # used for secrets (bandit: S311)

# Hardcoded secrets / creds (bandit: S105)
AWS_ACCESS_KEY = "AKIAFAKEACCESSKEY"
AWS_SECRET_KEY = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYFAKE"

# Global mutable (ruff: B006 if used as default elsewhere)
CONFIG = {"env": "dev", "debug": True}

# Insecure temp file handling (bandit: S108)
TMP_PATH = tempfile.gettempdir() + "/app.log"

# Unused variable (ruff: F841)
_ignored_count = 123

def gen_token():
    # Weak randomness for security tokens (bandit: S311)
    return "".join(random.choice("abcdef0123456789") for _ in range(32))

def weak_hash(data: str) -> str:
    # Weak hash (bandit: S324)
    return sha1(data.encode()).hexdigest()

def run_shell(cmd: str) -> str:
    # shell=True (bandit: S602), user-controlled command
    return subprocess.check_output(cmd, shell=True).decode()

def list_home():
    # os.system (bandit: S605)
    os.system("ls -la ~")  # noqa: S605

def unsafe_yaml_load(s: str):
    import yaml  # nosec
    # yaml.load without Loader (bandit: S506)
    return yaml.load(s)

def unsafe_pickle_load(b: bytes):
    import pickle
    # Insecure deserialization (bandit: S301)
    return pickle.loads(b)

def sql_injection(username: str):
    # String-format SQL (bandit: S608)
    conn = sqlite3.connect(":memory:")
    cur = conn.cursor()
    cur.execute("CREATE TABLE users(name TEXT, admin INT)")
    cur.execute("INSERT INTO users VALUES('alice', 0)")
    query = f"SELECT * FROM users WHERE name = '{username}'"
    print("Running query:", query)  # ruff: T201
    try:
        return list(cur.execute(query))
    finally:
        conn.close()

def bad_exception_handling():
    try:
        1 / 0
    except:  # bare except (ruff: E722, bandit: S110)
        pass

def path_traversal(filename: str):
    # Naive join allows traversal (bandit: S508 inference)
    base = "/var/app/uploads"
    return open(base + "/" + filename, "rb").read()

def dynamic_exec(user_code: str):
    # exec (bandit: S102) and eval (bandit: S307)
    exec(user_code)
    return eval("2 + 2")

def world_writable(path: str, text: str):
    with open(path, "w") as f:
        f.write(text)
    os.chmod(path, 0o777)  # bandit: S103

def leaky_logging():
    # Logs secrets (bandit: information leak; ruff: T201)
    print("Using AWS keys:", AWS_ACCESS_KEY, AWS_SECRET_KEY)  # noqa: T201

def start_debug_server():
    # Flask debug with 0.0.0.0 (bandit: S201)
    try:
        from flask import Flask
        app = Flask(__name__)

        @app.get("/")
        def index():
            return "ok"

        app.run(host="0.0.0.0", port=5000, debug=True)
    except Exception:
        pass

def main():
    print("Token:", gen_token())  # ruff: T201
    print("Hash:", weak_hash("password"))  # weak hash
    list_home()
    try:
        run_shell("cat /etc/passwd | head -n 3")
    except Exception as e:
        print("shell error:", e)
    sql_injection("alice'; DROP TABLE users; --")
    bad_exception_handling()
    leaky_logging()
    world_writable(TMP_PATH, "hello")

    # Keep some imports “unused”
    _ = sys.version

if __name__ == "__main__":
    main()
