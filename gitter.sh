#!/bin/bash         

echo "Starting the gitter shell script..."
#git submodule foreach 'git add . || :' 
git submodule foreach 'git --no-optional-locks -c color.branch=false -c color.diff=false -c color.status=false -c diff.mnemonicprefix=false -c core.quotepath=false -c credential.helper=sourcetree add . || :'
#git submodule foreach 'git commit -m everything || :' 
git submodule foreach 'git --no-optional-locks -c color.branch=false -c color.diff=false -c color.status=false -c diff.mnemonicprefix=false -c core.quotepath=false -c credential.helper=sourcetree commit -m everything || :'
git submodule foreach 'git push origin master || :' 
git add . 
git commit -m "push everything" 
git submodule foreach 'git status || :'
git push origin master
git status