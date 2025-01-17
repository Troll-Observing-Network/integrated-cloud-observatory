# %%
import html
import hvplot.pandas
import panel as pn
from io import StringIO

from bs4 import BeautifulSoup

# %%
pn.extension()

# %%
# Read the HTML content and escape it
with open("/Users/vonw/work/vaults/software/Troll-Observing-Network/integrated-cloud-observatory/data/back-trajectories/docs/index.html", "r") as f:
    html_content = f.read()
escaped_html = html.escape(html_content)

# %%
# Create iframe embedding the escaped HTML and display it
iframe_html = f'<iframe srcdoc="{escaped_html}" style="height:100%; width:100%" frameborder="0"></iframe>'


# %%
pn.template.FastListTemplate(
    title="Hello World",
    sidebar=["# Hello Sidebar", "This is text for the *sidebar*"],
    main=["# Back Trajectories", pn.pane.HTML(iframe_html, height=350, sizing_mode="stretch_both")],
).servable()