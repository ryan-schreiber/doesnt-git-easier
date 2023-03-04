
import requests
import io
import re
from copy import deepcopy
from contextlib import contextmanager
import smart_open

class Config():

    def __init__(self, base_url=None, token=None):
        self.attributes = {
            "token": token,
            "base_url": base_url,
        }

    def update(self, *args, **kwargs):
        self.attributes.update(kwargs)

    def _censor_token(self, token, show_first=4, show_last=0):
        output = token[:show_first] + "*" * (len(token)-(show_first + show_last))
        if show_last > 0:
            output += token[-show_last:]
        return output

    def get(self):
        output = deepcopy(self.attributes)
        output["token"] = self._censor_token(output["token"])
        return output

_CONFIG_OBJECT = Config()

def configure(*args, **kwargs):
    if len(args) > 0:
        raise ValueError('Only key word arguments are accepted (ie `configure(base_url="...", token="...")`')
    _CONFIG_OBJECT.update(*args, **kwargs)

def get_config():
    return _CONFIG_OBJECT.get()


# -----------------------------------------------------------

class File():

    def __init__(self, path, mode="r", *args, **kwargs):
        self.config = get_config()
        self.config.update(**kwargs)
        self.config = Config(self.config)
        self.path = path
        self.mode = mode
        self.parsed = self._parse_path(path)
        self.base_url = self.parsed["base_url"]
        self.org = self.parsed["org"]
        self.repo = self.parsed["repo"]
        self.filepath = self.parsed["path"]
        self.ref = self.parsed["ref"]
        self.headers = headers = {"Authorization": f"Bearer {self.config.attributes['token']}"}
        if mode.startswith("r"):
            self.buffer = self._open_readable(path)
        if mode.startswith("w"):
            self.buffer = io.StringIO("") if self.mode == "w" else io.BytesIO(b"")

    def _parse_path(self, path):
        pattern = "|".join([
            "https://(raw\.)?(.+?\.com)/(.+?)/(.+?)/(.+?)\?ref=(.+)",
            "https://(raw\.)?(.+?\.com)/(.+?)/(.+?)/(.+?)",
        ])
        matches = re.findall(pattern, path)
        return {
            "base_url": matches[0][1],
            "org": matches[0][2],
            "repo": matches[0][3],
            "path": matches[0][4],
            "ref": matches[0][5],
        }

    def _open_readable(self, path):
        headers = {"Authorization": f"Bearer {self.config.attributes['token']}"}
        raw_path = "https://raw.{base_url}/{org}/{repo}/{ref}/{path}".format(**self.parsed)
        response = requests.get(raw_path, headers=headers)
        if not response.ok:
            response.raise_for_status()
        return io.StringIO(response.text) if self.mode == "r" else io.BytesIO(response.text.encode("utf-8"))

    def open(self):
        pass

    def read(self, *args, **kwargs):
        return self.buffer.read()

    def write(self, content):
        self.buffer = type(self.buffer)(self.buffer.read() + type(self.buffer)(content).read())

@contextmanager
def open(*args, **kwargs):
    if args[0].startswith("https://git"):
        f = File(*args, **kwargs)
        yield f
    else:
        with smart_open.open(*args, **kwargs) as f:
            yield f
        
# -------------------------------------------------

class Commit():

    def __init__(self, message=None):
        self.message = message
        self.context = None
        self.blobs = []

    def add(self, file):
        file_context = {
            "base_url": file.base_url,
            "org": file.org,
            "repo": file.repo,
            "ref": file.ref,
        }
        if not self.context:
            self.context = file_context
            self.headers = file.headers
        else:
            assert(file_context == self.context)
        url = "https://{base_url}/api/v3/repos/{org}/{repo}/git/blobs".format(**self.context)
        data = {
            "content": file.read(),
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
            print("nothing to push")
            return

        print("getting base tree")
        # Step 1: Get the SHA of the latest commit on the branch
        url = "https://{base_url}/api/v3/repos/{org}/{repo}/git/refs/heads/{ref}".format(**self.context)
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        latest_commit_sha = response.json()["object"]["sha"]
        
        # Step 2: Get the tree associated with the latest commit
        url = "https://{base_url}/api/v3/repos/{org}/{repo}/git/trees/{latest_commit_sha}".format(latest_commit_sha=latest_commit_sha,**self.context)
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        tree_sha = response.json()["sha"]

        # Step 4: Create a new tree with the new file added
        url = "https://{base_url}/api/v3/repos/{org}/{repo}/git/trees".format(**self.context)
        data = {
            "base_tree": tree_sha,
            "tree": self.blobs
        }
        response = requests.post(url, json=data, headers=self.headers)
        response.raise_for_status()
        new_tree_sha = response.json()["sha"]
        
        # Step 5: Create a new commit with the new tree
        url = "https://{base_url}/api/v3/repos/{org}/{repo}/git/commits".format(**self.context)
        data = {
            "message": self.message,
            "tree": new_tree_sha,
            "parents": [latest_commit_sha]
        }
        response = requests.post(url, json=data, headers=self.headers)
        response.raise_for_status()
        new_commit_sha = response.json()["sha"]
        
        # Step 6: Update the branch reference to the new commit
        url = "https://{base_url}/api/v3/repos/{org}/{repo}/git/refs/heads/{ref}".format(**self.context)
        data = {
            "sha": new_commit_sha
        }
        response = requests.patch(url, json=data, headers=self.headers)
        response.raise_for_status()
        print("pushed!!!")

    def _get_base_tree_sha(self):
        pass
        

@contextmanager
def git_commit(*args, **kwargs):
    c = Commit(*args, **kwargs)
    yield c
    c.push()


#open(file, mode='r', buffering=-1, encoding=None, errors=None, newline=None, closefd=True, opener=None. *args, **kwargs):
















if __name__ == "__main__":
    
    with git_commit(message = "testing") as commit:
        
        with open("https://github.azc.ext.hp.com/cirrostratus/dps_mms/README.md?ref=dev", mode="w") as f:
            f.write("testing python lib")
            commit.add(f)
            
        with open("https://github.azc.ext.hp.com/cirrostratus/dps_mms/README_2.md?ref=dev", mode="w") as f:
            f.write("testing python lib again")
            commit.add(f)


