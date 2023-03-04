# `doesnt-git-easier`
Making it easy to read and write files to Git in a Pythonic way with context managers and the Git REST API.

## Sample Usage
```python
import doesnt_git_easier as git
from doesnt_git_easier import open

with git.commit(message = "Pushing with Doesn't Git Easier") as commit:
        
  with open("https://github.com/ryan-schreiber/doesnt-git-easier/test/README1.md?ref=main", mode="w") as f:
    f.write("testing python lib")
    commit.add(f)

  with open("https://github.com/ryan-schreiber/doesnt-git-easier/test/README2.md?ref=main", mode="wb") as f:
    f.write(b"testing python lib again")
    commit.add(f)
    
  #  automatically pushes when exiting the 'with' git.commit context
```
#### Install
``` 
pip install doesnt-git-easier
```

## Features

* Read and write files in Git with the standard python "open" function
* Commit and push files easily without cloning a repo
* Abstracts away the interactions with Git REST API in a Pythonic way for simpler use
* Multiple ways of storing token information to help keep your keys secure
* Uses the "smart_open" library for opening files when not a git file
* Can be used with Pandas and other libraries that work with files

## Full Usage

#### Authentication

Authentication section

#### Using Context Managers

context managers section

#### Without Context Managers

without context managers section



