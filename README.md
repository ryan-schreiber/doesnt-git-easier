# doesnt-git-easier
Making writing files to git easy and pythonic with context managers and the Git REST API.

## Usage
```python
import doesnt_git_easier as git
from doesnt_git_easier import open

with git.commit(message = "Pushing with Doesn't Git Easier") as commit:
        
  with open("https://github.com/ryan-schreiber/doesnt-git-easier/test/README1.md?ref=master", mode="w") as f:
    f.write("testing python lib")
    commit.add(f)

  with open("https://github.com/ryan-schreiber/doesnt-git-easier/test/README2.md?ref=master", mode="wb") as f:
    f.write(b"testing python lib again")
    commit.add(f)
    
  #  automatically pushes when exiting the 'with' git.commit statement
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


