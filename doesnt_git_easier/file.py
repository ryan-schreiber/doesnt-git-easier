

import requests
import io
import re
from copy import deepcopy
from contextlib import contextmanager
import smart_open
import doesnt_git_easier.config 


class GitStringIO(io.StringIO):

    def __init__(self, *args, **kwargs):
        # super().__init__(self, *args, **kwargs)
        super().__init__(*args)
        self.base_url = kwargs.get("base_url")
        self.owner = kwargs.get("owner")
        self.filepath = kwargs.get("filepath")
        self.repo = kwargs.get("repo")
        self.ref = kwargs.get("ref")
        self.headers = kwargs.get("headers")
        self.mode = kwargs.get("mode")

class GitBytesIO(io.BytesIO):

    def __init__(self, *args, **kwargs):
        super().__init__(*args)
        self.base_url = kwargs.get("base_url")
        self.owner = kwargs.get("owner")
        self.filepath = kwargs.get("filepath")
        self.repo = kwargs.get("repo")
        self.ref = kwargs.get("ref")
        self.headers = kwargs.get("headers")
        self.mode = kwargs.get("mode")



class _File():

    def __init__(self, path, mode="r", *args, **kwargs):
        self.config = doesnt_git_easier.config.get_config()
        self.config.update(**kwargs)
        self.config = doesnt_git_easier.config.Config(**self.config)
        self.path = path
        self.mode = mode
        self.parsed = self._parse_path(path)
        self.base_url = self.parsed["base_url"]
        self.owner = self.parsed["owner"]
        self.repo = self.parsed["repo"]
        self.filepath = self.parsed["path"]
        self.ref = self.parsed["ref"]
        self.headers = headers = {"Authorization": f"Bearer {self.config.attributes['token']}"}
        if "r" in self.mode:
            self.buffer = self._open_readable(path)
        if "w" in self.mode:
            self.buffer = GitStringIO("", **self.__dict__) if "b" not in self.mode else GitBytesIO(b"", **self.__dict__)

    def _parse_path(self, path):
        pattern = "|".join([
            "https://(raw\.)?(.+?\.com)/(.+?)/(.+?)/(.+?)\?ref=(.+)",
            "https://(raw\.)?(.+?\.com)/(.+?)/(.+?)/(.+?)",
        ])
        matches = re.findall(pattern, path)
        return {
            "base_url": matches[0][1],
            "owner": matches[0][2],
            "repo": matches[0][3],
            "path": matches[0][4],
            "ref": matches[0][5],
        }

    def _open_readable(self, path):
        headers = {"Authorization": f"Bearer {self.config.attributes['token']}"}
        if self.base_url == "github.com":
            raw_path = "https://raw.githubusercontent.com/{owner}/{repo}/{ref}/{path}".format(**self.parsed)
        else:
            raw_path = "https://raw.{base_url}/{owner}/{repo}/{ref}/{path}".format(**self.parsed)
        response = requests.get(raw_path, headers=headers)
        if not response.ok:
            response.raise_for_status()
        return GitStringIO(response.text) if "b" not in self.mode else GitBytesIO(response.text.encode("utf-8"))


@contextmanager
def open(*args, **kwargs):
    prefixes = [
        "https://github",
        "https://raw.github",
    ]
    for prefix in prefixes:
        if args[0].startswith(prefix):
            f = _File(*args, **kwargs)
            yield f.buffer
            return
    with smart_open.open(*args, **kwargs) as f:
        yield f
        

