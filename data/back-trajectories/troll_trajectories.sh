#!/usr/bin/bash

# ....Calculate the back trajectories for yesterday
cd /home/vonw/work/software/Troll-Observing-Network/integrated-cloud-observatory/data/back-trajectories
/home/vonw/vpwenv/.venv/bin/python create_troll_trajectories.py
/home/vonw/vpwenv/.venv/bin/python troll_trajectory_plots.py
cp docs/index.html ../../website/data/back-trajectories/.

# ....Render the website with changes
cd /home/vonw/work/software/Troll-Observing-Network/integrated-cloud-observatory/
quarto render website

# ....Push changes to GitHub (and GitHub Pages)
eval $(ssh-agent -s)
ssh-add ~/.ssh/id_rsa
git add .
d=$(date -d "yesterday" -u -I)
git commit -m "Daily trajectories for ${d}"
git fetch
git merge origin/main
git push

# ....Remove the large GFS file
d=$(date -d "2 days ago" -u +%Y%m%d)
rm ${d}_gfs0p25
