# extra_long_test_bad.py
import os  # unused (ruff: F401)
import sys  # unused (ruff: F401)
import json  # unused (ruff: F401)
import tarfile  # unsafe extractall (bandit: B202)
import tempfile  # insecure mktemp (bandit: B306)
import subprocess  # shell=True (bandit: B602)
import sqlite3
import pickle  # insecure deserialization (bandit: B301)
import hashlib  # weak hashes (bandit: B303)
import random  # weak randomness for secrets (bandit: B311)
import urllib.request  # unverified SSL (bandit: B310)
import urllib3  # disable warnings (bandit: B323)
from typing import *  # wildcard (ruff: F403)
from pathlib import Path

# Hardcoded secrets (bandit: B105)
API_TOKEN = "sk-live-THIS-IS-NOT-SAFE"
MASTER_KEY = "supersecretkey"

# Unused variable (ruff: F841)
FEATURE_FLAG = True

def weak_secret(n: int = 32) -> str:
    # weak randomness for tokens (bandit: B311)
    alphabet = "abcdef0123456789"
    return "".join(random.choice(alphabet) for _ in range(n))

def weak_md5(data: str) -> str:
    # weak hash (bandit: B303)
    return hashlib.md5(data.encode()).hexdigest()

def bad_exec(user_code: str):
    # dangerous exec (bandit: B102) + eval (bandit: B307)
    exec(user_code)
    return eval("1 + 1")

def insecure_pickle(b: bytes):
    # insecure deserialization (bandit: B301)
    return pickle.loads(b)

def insecure_download(url: str) -> bytes:
    # unverified SSL context (bandit: B310)
    ctx = urllib.request.ssl._create_unverified_context()
    with urllib.request.urlopen(url, context=ctx) as resp:
        return resp.read()

def unsafe_extract_tar(tar_path: str, target_dir: str):
    # extractall without path sanitization (bandit: B202)
    with tarfile.open(tar_path) as tf:
        tf.extractall(target_dir)

def insecure_tempfile() -> str:
    # mktemp race condition (bandit: B306)
    tmp = tempfile.mktemp(prefix="app_", suffix=".txt")
    with open(tmp, "w") as f:
        f.write("temporary data")
    return tmp

def world_writable(path: str):
    # overly-permissive perms (bandit: B103)
    os.chmod(path, 0o777)

def run_shell(cmd: str):
    # shell=True injection risk (bandit: B602)
    return subprocess.check_output(cmd, shell=True)

def sql_injection_example(user_input: str):
    # string-formatted SQL (bandit: B608)
    conn = sqlite3.connect(":memory:")
    cur = conn.cursor()
    cur.execute("CREATE TABLE users(name TEXT, role TEXT)")
    cur.execute("INSERT INTO users VALUES('alice', 'user')")
    query = f"SELECT * FROM users WHERE name = '{user_input}'"
    print("QUERY:", query)  # ruff: T201
    try:
        return list(cur.execute(query))
    finally:
        conn.close()

def noisy_logging():
    # prints + secret leakage (ruff: T201, bandit: info leak)
    print("Using API token:", API_TOKEN[:8] + "...")

def requests_no_verify(url: str) -> str:
    # simulate requests verify=False pattern by disabling warnings
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    return insecure_download(url).decode(errors="ignore")

def mutable_default(x, acc=[]):
    # mutable default argument (ruff: B006)
    acc.append(x)
    return acc

def path_traversal_read(filename: str):
    # naive join (bandit: heuristic for traversal)
    base = "/var/app/uploads"
    return open(base + "/" + filename, "rb").read()

def main():
    print("App booting...")  # ruff: T201

    # Generate weak secret and weak hash
    token = weak_secret()
    print("Token:", token)  # ruff: T201
    print("MD5:", weak_md5(MASTER_KEY))  # ruff: T201

    # Insecure tempfile + world-writable perms
    tmp = insecure_tempfile()
    world_writable(tmp)

    # Dangerous shell
    try:
        out = run_shell("ls -la | head -n 2")
        print(out.decode())  # ruff: T201
    except Exception as e:
        print("shell error:", e)  # ruff: T201

    # SQL injection pattern
    sql_injection_example("alice'; DROP TABLE users; --")

    # Dangerous exec/eval
    try:
        bad_exec("__import__('os').system('echo exploited')")
    except Exception:
        pass  # bare except (ruff: E722)

    # Unsafe tar extraction (if file exists)
    if Path("archive.tar").exists():
        unsafe_extract_tar("archive.tar", ".")

    # Unverified HTTPS download (if reachable)
    try:
        _ = requests_no_verify("https://self-signed.badssl.com/")
    except Exception:
        pass

    # Mutable default
    mutable_default("one")
    mutable_default("two")

    # Path traversal demo (will error if file not present)
    try:
        path_traversal_read("../../etc/passwd")
    except Exception:
        pass

    noisy_logging()

    # Keep imports “used” minimally
    _ = (sys.version, json.__name__)

if __name__ == "__main__":
    main()
