
import doesnt_git_easier as git
from doesnt_git_easier import open

with git.commit(message = "Pushing with Doesn't Git Easier") as commit:
        
  with open("https://github.com/ryan-schreiber/doesnt-git-easier/test/README.md?ref=test", mode="w") as f:
    f.write("testing python lib file fix")
    commit.add(f)

  with open("https://github.com/ryan-schreiber/doesnt-git-easier/test/README2.md?ref=test", mode="wb") as f:
    f.write(b"testing python lib file fix again")
    commit.add(f)

import pandas
data = [{"a":i, "b":i**2, "c":i**3} for i in [1,2,3,4,5]]
df = pandas.DataFrame.from_records(data)



with git.commit(message = "Pushing with Doesn't Git Easier") as commit:
    
	with open("https://github.com/ryan-schreiber/doesnt-git-easier/test/test.csv?ref=test", "w") as f:
		df.to_csv(f, index=False)
		commit.add(f)

