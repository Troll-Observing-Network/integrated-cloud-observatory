# %%
import datetime as dt
import panel as pn

pn.extension()

# %%
datetime_slider = pn.widgets.DatetimeSlider(name='Datetime Slider', start=dt.datetime(2019, 1, 1), end=dt.datetime(2019, 6, 1), value=dt.datetime(2019, 2, 8, 15), step=3600)

datetime_slider

# %%
datetime_range_input = pn.widgets.DatetimeRangeInput(
    name='Datetime Range Input',
    start=dt.datetime(2017, 1, 1), end=dt.datetime(2019, 1, 1),
    value=(dt.datetime(2017, 1, 1), dt.datetime(2018, 1, 10)),
    width=300
)

datetime_range_input

# %%
datetime_range_slider = pn.widgets.DatetimeRangeSlider(
    name='Datetime Range Slider',
    start=dt.datetime(2017, 1, 1), end=dt.datetime(2019, 1, 1),
    value=(dt.datetime(2017, 1, 1), dt.datetime(2018, 1, 10)),
    step=3600000
)

datetime_range_slider

# %%
