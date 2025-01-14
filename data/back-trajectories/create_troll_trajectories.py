# %%
import sys
import pandas as pd
import numpy as np

# ....Import hysplit
sys.path.append('/home/vonw/work/vaults/software/backTrajectories/')
import hysplit

def download_GFS_data(date):
    # ....Retrieve GFS data for given date
    dates = pd.date_range(date.strftime('%Y-%m-%d'), date.strftime('%Y-%m-%d'), freq='D')
    data_source = 'GFS'
    hy = hysplit.HYSPLIT(dates,data_source)
    hy.retrieveGFSdataFromNOAA()
    return

def generate_back_trajectories(times):
    # ....Create hysplit back trajectories for particular time 
    data_source = 'GFS'
    length = 120    # 120 hours = 5 days
    # From Steve Hudson (72.0102S, 2.5453E)
    lat    = -72.0102
    lon    = +2.5453
    alts   = np.arange(100, 10000, 500)
    descriptor = 'Troll_'
    hy = hysplit.HYSPLIT(times,data_source,length,lat,lon,alts,descriptor)
    hy.runBackTrajectory()
    return

# %%
today     = pd.Timestamp.now()
yesterday = today - pd.Timedelta('1 days')
times = pd.date_range(yesterday.strftime('%Y-%m-%d')+' 00:00', yesterday.strftime('%Y-%m-%d')+' 23:00', freq='1h')

# %%
download_GFS_data(today)

# %%
generate_back_trajectories(times)

# %%
