# %%
import xarray as xr
import hvplot.xarray
import hvplot.pandas
import datetime as dt
import cartopy.crs as ccrs
import panel as pn
pn.extension('tabulator')

from socket import gethostname
hostname = gethostname()

# %%
if ('nuia' in hostname):
    fn = '/Users/vonw/data/troll/hysplit/troll_back_trajectories'
elif ('gaia' in hostname):
    fn = '/mnt/disk2/data/hysplit/backTrajectories/troll_back_trajectories'
else:
    print('No data file containing back trajectories. Exiting.')
    exit()

# %%
@pn.cache
def get_data(filename):
    return xr.open_zarr(filename, consolidated=True)
back_trajectories = get_data(fn)

# %% widgets
variables = [variable for variable in back_trajectories.variables]

time      = pn.widgets.DatetimePicker(name='Date of Trajectories', value=dt.datetime(2024, 11, 3), start=dt.datetime(2024, 11, 3), end = dt.datetime.today() - dt.timedelta(days=1))
level     = pn.widgets.IntSlider(name='Vertical Level of Trajectory (m)', start=100, end=9100, value=100, step=500, bar_color='green')
variable  = pn.widgets.Select(name='Trajectory Variable', options=variables)
kind      = pn.widgets.Select(name='Plot Type', options=['line', 'hist'])

# %%
def get_dataframe(time, level):
    df = back_trajectories.sel(time=time.strftime('%Y-%m-%d %H'), vertical_level=level, method='nearest').to_dataframe()
    return df

df = pn.rx(get_dataframe)(time=time, level=level)

# %% Indicators
indicators = pn.FlexBox(
    pn.indicators.Number(
        value=df['air temperature'].mean(), name="Mean Air Temperature", format="{value:,.1f}", font_size='24pt', title_size='8pt', colors=[(250, 'blue'), (273.15, 'teal'), (290, 'red')],
    ),
    pn.indicators.Number(
        value=df['air temperature'].max(),  name="Max Air Temperature", format="{value:,.1f}", font_size='24pt', title_size='8pt', colors=[(250, 'blue'), (273.15, 'teal'), (290, 'red')],
    ),
    pn.indicators.Number(
        value=df['air temperature'].min(),  name="Min Air Temperature", format="{value:,.1f}", font_size='24pt', title_size='8pt', colors=[(250, 'blue'), (273.15, 'teal'), (290, 'red')],
    ),
)

# %% Figure definition
trj = pn.pane.HoloViews(df.hvplot.points('longitude',
                                        'latitude',
                                        geo=True, 
                                        color=variable, 
                                        cmap='viridis',
                                        xlim=[-90, 0], 
                                        ylim=[50, 84], 
                                        coastline=True, 
                                        projection=ccrs.NearsidePerspective(central_longitude=+2.5453, central_latitude=-72.0102), 
    )
)

fig = df[variable].hvplot(kind=kind, grid=True)

# %%
plot  = pn.pane.HoloViews(fig, sizing_mode='stretch_both', name='Plot')
table = pn.widgets.Tabulator(df, sizing_mode='stretch_both', name='Table')

tabs = pn.Tabs(
    plot, table, sizing_mode="stretch_width", height=500, margin=10
)

# %% Serve the template
pn.template.FastListTemplate(
    title="Troll back trajectory dashboard",
    sidebar=[time, level, variable, kind],
    main=[pn.Column(pn.Row(trj, indicators), tabs, sizing_mode="stretch_both")],
).servable()

# %%
