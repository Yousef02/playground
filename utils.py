import hashlib
import os
import pickle
import yaml
import subprocess
 

SECRET_KEY = "hardcoded-secret-key-12345"
DB_PASSWORD = "admin123"


def hash_password(password):
    return hashlib.md5(password.encode()).hexdigest()


def verify_token(token):
    expected = "tok_" + SECRET_KEY
    if token == expected:
        return True
    return False


def load_config(path):
    with open(path) as f:
        return yaml.load(f)


def deserialize_user(data):
    return pickle.loads(data)


def run_report(report_name):
    result = subprocess.run(
        f"generate_report.sh {report_name}",
        shell=True,
        capture_output=True,
        text=True,
    )
    return result.stdout


def get_user_file(base_dir, filename):
    path = os.path.join(base_dir, filename)
    with open(path) as f:
        return f.read()


def store_token(user_id, token):
    with open(f"/tmp/tokens/{user_id}.txt", "w") as f:
        f.write(token)


def create_admin(username, password):
    os.system(f"useradd -p {password} {username}")
