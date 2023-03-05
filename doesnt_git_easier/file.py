

import requests
import io
import re
from copy import deepcopy
from contextlib import contextmanager
import smart_open
import doesnt_git_easier.config 


class File():

    def __init__(self, path, mode="r", *args, **kwargs):
        self.config = doesnt_git_easier.config.get_config()
        self.config.update(**kwargs)
        self.config = doesnt_git_easier.config.Config(**self.config)
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
        if self.base_url == "github.com":
            raw_path = "https://raw.githubusercontent.com/{org}/{repo}/{ref}/{path}".format(**self.parsed)
        else:
            raw_path = "https://raw.{base_url}/{org}/{repo}/{ref}/{path}".format(**self.parsed)
        response = requests.get(raw_path, headers=headers)
        if not response.ok:
            response.raise_for_status()
        return io.StringIO(response.text) if self.mode == "r" else io.BytesIO(response.text.encode("utf-8"))

    def read(self, *args, **kwargs):
        return self.buffer.read()

    def write(self, content):
        self.buffer = type(self.buffer)(self.buffer.read() + type(self.buffer)(content).read())


@contextmanager
def open(*args, **kwargs):
    prefixes = [
        "https://github",
        "https://raw.github",
    ]
    for prefix in prefixes:
        if args[0].startswith(prefix):
            f = File(*args, **kwargs)
            yield f
            return
    with smart_open.open(*args, **kwargs) as f:
        yield f
        

