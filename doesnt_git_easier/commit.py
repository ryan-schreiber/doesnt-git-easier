
import requests
import io
import re
from copy import deepcopy
from contextlib import contextmanager
import smart_open


class Commit():

    def __init__(self, message=None):
        self.message = message
        self.context = None
        self.blobs = []

    def add(self, file):
        file_context = {
            "base_url": file.base_url,
            "owner": file.owner,
            "repo": file.repo,
            "ref": file.ref,
        }
        if not self.context:
            self.context = file_context
            self.headers = file.headers
        else:
            assert(file_context == self.context)

        api_url = "https://api.github.com" if self.context["base_url"] == "github.com" else f"https://{self.context['base_url']}/api/v3"
        url = "{api_url}/repos/{owner}/{repo}/git/blobs".format(api_url=api_url, **self.context)
        file.seek(0)
        data = {
            "content": file.read().decode("utf-8") if "b" in file.mode else file.read(),
            "encoding": "utf-8"
        }
        response = requests.post(url, json=data, headers=self.headers)
        response.raise_for_status()
        self.blobs.append({
            "path": file.filepath,
            "sha": response.json()["sha"],
            "mode": "100644",
            "type": "blob",
        })

    def push(self):
        if not len(self.blobs):
            # print("nothing to push")
            return

        self.context["api_url"] = "https://api.github.com" if self.context["base_url"] == "github.com" else f"https://{self.context['base_url']}/api/v3"
        # Step 1: Get the SHA of the latest commit on the branch
        url = "{api_url}/repos/{owner}/{repo}/git/refs/heads/{ref}".format(**self.context)
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        latest_commit_sha = response.json()["object"]["sha"]
        
        # Step 2: Get the tree associated with the latest commit
        url = "{api_url}/repos/{owner}/{repo}/git/trees/{latest_commit_sha}".format(latest_commit_sha=latest_commit_sha,**self.context)
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        tree_sha = response.json()["sha"]

        # Step 4: Create a new tree with the new file added
        url = "{api_url}/repos/{owner}/{repo}/git/trees".format(**self.context)
        data = {
            "base_tree": tree_sha,
            "tree": self.blobs
        }
        response = requests.post(url, json=data, headers=self.headers)
        response.raise_for_status()
        new_tree_sha = response.json()["sha"]
        
        # Step 5: Create a new commit with the new tree
        url = "{api_url}/repos/{owner}/{repo}/git/commits".format(**self.context)
        data = {
            "message": self.message,
            "tree": new_tree_sha,
            "parents": [latest_commit_sha]
        }
        response = requests.post(url, json=data, headers=self.headers)
        response.raise_for_status()
        new_commit_sha = response.json()["sha"]
        
        # Step 6: Update the branch reference to the new commit
        url = "{api_url}/repos/{owner}/{repo}/git/refs/heads/{ref}".format(**self.context)
        data = {
            "sha": new_commit_sha
        }
        response = requests.patch(url, json=data, headers=self.headers)
        response.raise_for_status()

    def _get_base_tree_sha(self):
        pass
        

@contextmanager
def commit(*args, **kwargs):
    c = Commit(*args, **kwargs)
    yield c
    c.push()


