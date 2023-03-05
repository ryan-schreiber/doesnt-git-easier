
import doesnt_git_easier as git
from doesnt_git_easier import open

with git.commit(message = "Pushing with Doesn't Git Easier") as commit:
        
  with open("https://github.com/ryan-schreiber/doesnt-git-easier/test/README.md?ref=main", mode="w") as f:
    f.write("testing python lib")
    commit.add(f)

  with open("https://github.com/ryan-schreiber/doesnt-git-easier/test/README2.md?ref=main", mode="wb") as f:
    f.write(b"testing python lib again")
    commit.add(f)
    
  #  automatically pushes when exiting the 'with' git.commit context