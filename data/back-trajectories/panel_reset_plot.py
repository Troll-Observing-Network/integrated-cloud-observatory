import numpy as np
import panel as pn
from matplotlib.figure import Figure
from matplotlib import cm
import param

pn.extension(sizing_mode="stretch_width", throttled=True)


def plot_streamplot(xrange, yrange):
    xmin, xmax = xrange
    ymin, ymax = yrange
    Y, X = np.mgrid[ymin:ymax:100j, xmin:xmax:100j]
    U = -1 - X**2 + Y
    V = 1 + X - Y**2

    fig = Figure(figsize=(4, 3))
    ax = fig.subplots()

    strm = ax.streamplot(X, Y, U, V, color=U, linewidth=2, cmap=cm.autumn)
    fig.colorbar(strm.lines)

    mpl_pane = pn.pane.Matplotlib(fig, dpi=144)
    return mpl_pane


xrange_slider = pn.widgets.RangeSlider(
    name="X Range Slider", start=-10, end=+10, value=(-3, +3), step=0.01
)
yrange_slider = pn.widgets.RangeSlider(
    name="Y Range Slider", start=-10, end=+10, value=(-3, +3), step=0.01
)


def reset_range_sliders(_event):
    xrange_slider.value = (-3, +3)
    yrange_slider.value = (-3, +3)


reset_button = pn.widgets.Button(
    name="Reset ranges",
    button_type="primary",
    on_click=reset_range_sliders,
    margin=(20,10)
)

bound_plot_streamplot = pn.bind(
    plot_streamplot,
    xrange_slider.param.value,
    yrange_slider.param.value,
)

# Instantiate the template with widgets displayed in the sidebar
pn.template.EditableTemplate(
    editable=True,
    title="Matplotlib Streamlines demo (EditableTemplate)",
    sidebar=[xrange_slider, yrange_slider, reset_button],
    main=[bound_plot_streamplot],
).servable()
