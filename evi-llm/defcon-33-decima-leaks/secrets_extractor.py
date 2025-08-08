import re

CONFIG_FILES = ['config.env', 'credentials.txt']
KEYWORDS = ['key', 'password', 'secret']

def extract_secrets(filename):
    with open(filename, 'r') as f:
        for line in f:
            if any(kw in line.lower() for kw in KEYWORDS):
                print(f"[{filename}] {line.strip()}")

if __name__ == "__main__":
    for file in CONFIG_FILES:
        try:
            extract_secrets(file)
        except FileNotFoundError:
            print(f"File not found: {file}") 