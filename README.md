#### Always remember to make your changes on a new branch.  
#### The new branch has to come from ***develop***


## - Check in what branch you are  
`git branch`

## - If you are not in develop switch to it  
`git checkout develop`


If you have some changes that have not been updated it won't let you checkout. Then do the following:  
`git checkout HEAD^`  
`git checkout -f develop`  
You will lose the changes, so if you wanna keep them, store them somewhere else and paste them after you create the new branch.  
Remember to check that you are in ***develop*** after this


## - Once there, update the files to the latest version  
`git pull`


## - Now create the new branch  
`git checkout -b FEATURE/name-of-branch`  
i.e. `git checkout -b FEATURE/inverse-kinematic`


## - Work on your changes


## - Once you want to update your changes to the global repository, first check the files that have been modified  
`git status`


This shows you the files that have been modified in your branch. In green, the ones that are already ready to commit.  
In red, the ones that have not been added yet.


## - Only add the ones you want, as sometimes it understands you have modified some configuration files as they were not in the repo  
`git add name-of-file`  
i.e. `git add main.py`


## - After adding all the ones you want, check again the status  
`git status`


## - If all the files you want are in green, then commit  
`git commit -m "message"`
i.e. `git commit -m "modified the way inverse kinematics was being done`


## - Push the changes  
`git push origin name-of-branch`   
i.e. `git push origin FEATURE/inverse-kinematic`


## - After this it will probably print many lines and a link to the bitbucket repo. Follow the link to create the pull request.  
It can also be done from the bitbucket page under Pull Requests


## - Create the pull request from your branch to develop. Select as reviewers the other team members.




