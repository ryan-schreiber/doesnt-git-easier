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

## Authentication

This library uses a Github Personal Access Token. Find out how to get one 
[here](https://docs.github.com/en/enterprise-server@3.4/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token). 
The following are all ways to authenticate the personal access token, and is the order of operations 
for reading. For example, if the git token is defined in the credentials file and an environment 
variable, then the environment variable would be used.

##### ~/.github/credentials File
```
[default]
GIT_TOKEN = ghp_xxxxxxx
```

##### Set Environment Variable
```sh
export GIT_TOKEN=ghp_xxxxxxx
```

##### .env File
```
GIT_TOKEN = ghp_xxxxxxx
```

##### doesnt_git_easier.configure Function
```python
import doesnt_git_easier as git
git.configure(token="ghp_xxxxxxx")
...
```

## More use cases

##### 1. Read contents of files in Git repo
```python
import doesnt_git_easier as git
from doesnt_git_easier import open

#configure your git token if it is not in env variable or credential file
git.configure(token="ghp_xxxxxxx")

# Example #1 leave out mode and it defaults to 'r' like builtin open function
with open("https://github.com/ryan-schreiber/doesnt-git-easier/test/README1.md?ref=main") as f:
  text = f.read()

# Example #2 read in as a string
with open("https://github.com/ryan-schreiber/doesnt-git-easier/test/README1.md?ref=main", mode="r") as f:
  text = f.read()

# Example #3 read in as a bytestring
with open("https://github.com/ryan-schreiber/doesnt-git-easier/test/README1.md?ref=main", mode="rb") as f:
  bytes = f.read()
```

##### 2. Work with a small dataset from Git repo as a dataframe
```python
import pandas
import doesnt_git_easier as git
from doesnt_git_easier import open

#configure your git token if it is not in env variable or credential file
git.configure(token="ghp_xxxxxxx")

# Example #1 How to read into a dataframe
with open("https://github.com/ryan-schreiber/doesnt-git-easier/test/test.csv?ref=main", mode="r") as f:
  df = pandas.from_csv(f)
  # if you're working with spark you can use this step to convert pandas df to spark df
  # df = spark.createDataFrame(pandas.from_csv(f))
  
# ... make some transformations ...

# Example #2 How to write a dataframe to git
with git.commit(message="updating csv file") as commit:

  with open("https://github.com/ryan-schreiber/doesnt-git-easier/test/test.csv?ref=main", mode="w") as f:
    df.to_csv(f, index=False)
    commit.add(f)
  
  # automatically pushes at the end of the git.commit scope
```


##### 3. Work without the context managers
```python
import doesnt_git_easier as git
from doesnt_git_easier import open

#configure your git token if it is not in env variable or credential file
git.configure(token="ghp_xxxxxxx")

# reading a file
f = open("https://github.com/ryan-schreiber/doesnt-git-easier/test/README.md?ref=main", mode="r")
text = f.read()
f.close()

# writing a file
commit = git.commit(message="without context managers")
f = open("https://github.com/ryan-schreiber/doesnt-git-easier/test/README.md?ref=main", mode="w")
f.write("testing testing")
commit.add(f)
f.close()
commit.push()

```


