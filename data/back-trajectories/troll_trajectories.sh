#!/usr/bin/bash

cd /home/vonw/work/software/Troll-Observing-Network/integrated-cloud-observatory-team/back-trajectories

/home/vonw/anaconda3/envs/work/bin/python create_troll_trajectories.py
/home/vonw/anaconda3/envs/work/bin/python troll_trajectory_plots.py

eval $(ssh-agent -s)
ssh-add ~/.ssh/id_rsa
git add .
d=$(date -d "yesterday" -u -I)
git commit -m "Daily trajectories for ${d}"
git fetch
git merge origin/main
git push
