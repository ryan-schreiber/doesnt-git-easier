
import requests
import io
import re
from copy import deepcopy
from contextlib import contextmanager
import smart_open
from dotenv import load_dotenv
import os

load_dotenv()

# order of operations for configuration
# 1. .github/credentials
# 2. environment variables (GIT_TOKEN, GIT_BASE_URL)
# 3. parameters
# runtime. configure() function


class Config():

    def __init__(self, base_url=None, token=None):
        self.attributes = {
            "token": token,
            "base_url": base_url,
        }

    def update(self, *args, **kwargs):
        self.attributes.update(kwargs)

    def get(self):
        output = deepcopy(self.attributes)
        return output


def configure(*args, **kwargs):
    if len(args) > 0:
        raise ValueError('Only key word arguments are accepted (ie `configure(base_url="...", token="...")`')
    _CONFIG_OBJECT.update(*args, **kwargs)

def get_config():
    return _CONFIG_OBJECT.get()


_CONFIG_OBJECT = Config()

# 1. credentials file
pass

# 2. environment variables
configure(token=os.environ.get("GIT_TOKEN")) if os.environ.get("GIT_TOKEN") else None
configure(base_url=os.environ.get("GIT_BASE_URL")) if os.environ.get("GIT_BASE_URL") else None

