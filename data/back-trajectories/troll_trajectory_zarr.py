# %%
from glob import glob
from datetime import datetime
import numpy as np
import pandas as pd
import xarray as xr
import hvplot.xarray
import cartopy.crs as ccrs

# %%
def repair_trajectory_dataframe(df, hours):
    # ....Initialize a new dataframe
    ndf = pd.DataFrame({})
    for trj_df in df.groupby('trajectory'):
        # Extract trajectory and dataframe from group
        trj = trj_df[0]
        tdf = trj_df[1]
        # ....Check if trajectory dataframe has expected hours.
        #     If not, repair
        if len(tdf) < len(hours):
            for hour in hours:
                # ....Create date and time variables
                date = pd.Timestamp(df.year.iloc[0]+2000, df.month.iloc[0], df.day.iloc[0], df.hour.iloc[0]) + pd.Timedelta(hour, 'h')
                if hour not in tdf.time.values:
                    # ....Create a new row
                    new_row = pd.DataFrame({'trajectory': trj,
                                'run': 1,
                                'year': date.year,
                                'month': date.month,
                                'day': date.day,
                                'hour': date.hour,
                                'minute': 0,
                                'seconds': 0,
                                'time': hour,
                                'latitude': np.nan,
                                'longitude': np.nan,
                                'altitude': np.nan,
                                'pressure': np.nan,
                                'potential temperature': np.nan,
                                'air temperature': np.nan,
                                'rainfall': np.nan,
                                'mix depth': np.nan,
                                'relative humidity': np.nan,
                                'terrain above msl': np.nan,
                                'solar flux': np.nan,
                                }, index=[trj])
                    tdf = pd.concat([tdf, new_row.reset_index()])
        
        # ....Concat trajectory dataframe onto new dataframe
        ndf = pd.concat([ndf, tdf.reset_index()])
        ndf.reset_index(drop=True, inplace=True)

    return ndf

# %%
# ....Initialize variables
hours = np.arange(0,-121,-1).astype(float)
variables = ['trajectory', 'latitude', 'longitude', 'altitude', 'pressure', 'potential temperature', 'air temperature', 'rainfall', 'mix depth', 'relative humidity', 'terrain above msl', 'solar flux']
time = []
ref_time_along_trajectories = np.nan * np.ones((121,1))
vertical_level = np.nan * np.ones((20,1))
ds = xr.Dataset({}, coords={'time': time})

fns = sorted(glob('/mnt/disk2/data/hysplit/backTrajectories/Troll*.trj'))
for fn in fns:
    print(fn)
    df = pd.read_csv(fn, skiprows=32, delimiter=r"\s+", names=['trajectory', 'run', 'year', 'month', 'day', 'hour', 'minute', 'seconds', 'time', 'latitude', 'longitude', 'altitude', 'pressure', 'potential temperature', 'air temperature', 'rainfall', 'mix depth', 'relative humidity', 'terrain above msl', 'solar flux'])
    time = [np.array(pd.Timestamp(2000+df.year[0], df.month[0], df.day[0], df.hour[0], df.minute[0], df.seconds[0]))]
    if fn == fns[0]:
        ref_time_along_trajectories = df[df.trajectory==1]['time'].values
        vertical_level = df.altitude.values[0:20]
    # ....Deals with trajectories that have less than desired number of hours
    ndf = repair_trajectory_dataframe(df, hours)
    # ....Convert dataframe to a dataset and append
    nds = xr.Dataset({'trajectory':            (['time', 'vertical_level', 'ref_time_along_trajectories'], ndf.trajectory.values.reshape(1, 20, 121)),
                      'latitude':              (['time', 'vertical_level', 'ref_time_along_trajectories'], ndf.latitude.values.reshape(1, 20, 121)),
                      'longitude':             (['time', 'vertical_level', 'ref_time_along_trajectories'], ndf.longitude.values.reshape(1, 20, 121)),
                      'altitude':              (['time', 'vertical_level', 'ref_time_along_trajectories'], ndf.altitude.values.reshape(1, 20, 121)),
                      'pressure':              (['time', 'vertical_level', 'ref_time_along_trajectories'], ndf.pressure.values.reshape(1, 20, 121)),
                      'potential temperature': (['time', 'vertical_level', 'ref_time_along_trajectories'], ndf['potential temperature'].values.reshape(1, 20, 121)),
                      'air temperature':       (['time', 'vertical_level', 'ref_time_along_trajectories'], ndf['air temperature'].values.reshape(1, 20, 121)),
                      'rainfall':              (['time', 'vertical_level', 'ref_time_along_trajectories'], ndf.rainfall.values.reshape(1, 20, 121)),
                      'mix depth':             (['time', 'vertical_level', 'ref_time_along_trajectories'], ndf['mix depth'].values.reshape(1, 20, 121)),
                      'relative humidity':     (['time', 'vertical_level', 'ref_time_along_trajectories'], ndf['relative humidity'].values.reshape(1, 20, 121)),
                      'terrain above msl':     (['time', 'vertical_level', 'ref_time_along_trajectories'], ndf['terrain above msl'].values.reshape(1, 20, 121)),
                      'solar flux':            (['time', 'vertical_level', 'ref_time_along_trajectories'], ndf['solar flux'].values.reshape(1, 20, 121)),
                      }, 
                    coords={
                        'ref_time_along_trajectories': ref_time_along_trajectories,
                        'vertical_level': vertical_level,
                        'time': time})
    ds = xr.concat([ds, nds], dim='time')
ds['time'] = np.array([t.values for t in ds.time])

# %%
ds.to_netcdf('/mnt/disk2/data/hysplit/backTrajectories/troll_back_trajectories.nc')

# %%
ds.to_zarr('/mnt/disk2/data/hysplit/backTrajectories/troll_back_trajectories')

# %%
