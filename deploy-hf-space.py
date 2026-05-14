"""
Hugging Face Space 部署腳本
用法: python deploy-hf-space.py
"""
import os
import sys

SPACE_DIR = r"C:\Users\Greg\Desktop\AI\mimo2codex-hf-space"
REPO_ID = "gregcho/mimo2codex"

def get_hf_token():
    cred_path = os.path.expanduser("~/.git-credentials")
    if os.path.exists(cred_path):
        with open(cred_path, "r") as f:
            for line in f:
                if "huggingface.co" in line:
                    return line.split("://")[1].split("@")[0].split(":")[-1]
    return os.environ.get("HF_TOKEN")

def main():
    try:
        from huggingface_hub import HfApi
    except ImportError:
        print("Error: huggingface_hub not installed. Run: pip install huggingface_hub")
        sys.exit(1)

    token = get_hf_token()
    if not token:
        print("Error: No Hugging Face token found.")
        print("Set HF_TOKEN environment variable or configure ~/.git-credentials")
        sys.exit(1)

    api = HfApi(token=token)

    print(f"Deploying to {REPO_ID}...")

    try:
        api.create_repo(
            repo_id=REPO_ID,
            repo_type="space",
            space_sdk="gradio",
            exist_ok=True,
            private=False,
        )
        print(f"Space repo ready: {REPO_ID}")
    except Exception as e:
        print(f"Create repo: {e}")

    for fname in os.listdir(SPACE_DIR):
        fpath = os.path.join(SPACE_DIR, fname)
        if os.path.isfile(fpath):
            print(f"  Uploading {fname}...")
            api.upload_file(
                path_or_fileobj=fpath,
                path_in_repo=fname,
                repo_id=REPO_ID,
                repo_type="space",
            )

    print(f"\nDone! Space URL: https://huggingface.co/spaces/{REPO_ID}")

if __name__ == "__main__":
    main()
