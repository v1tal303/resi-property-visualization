import folium
from folium import plugins
import branca
import branca.colormap as cm
from IPython.display import display
import webbrowser
import pandas as pd

# The coordinates entered in the function allows me to start the map at the City of London
m = folium.Map([52.4261112, -1.5987646], zoom_start = 10, tiles = "CartoDB positron")

df = pd.read_csv("test2.csv")

def reversed_colormap(existing):
    return cm.LinearColormap(
        colors=list(reversed(existing.colors)),
        vmin=existing.vmin, vmax=existing.vmax)

# Initialise the colormap that we want. You can get a list of colormaps by running cm.linear
linear = cm.linear.RdYlBu_10.scale(20000, 1000000)


# reverse the colormap
linear = reversed_colormap(linear)

# Adding points to the map
for index, row in df.iterrows():
    folium.CircleMarker([row['latitude'], row['longitude']],
                        radius=4,
                        popup=f"Link: {df['propertyLink'].iloc[index]}\n\n Price: £{int(df['propertyPrice'].iloc[index])}",
                        fill_color = linear(int(df['propertyPrice'].iloc[index])),
                        color=linear(int(df['propertyPrice'].iloc[index])),
                        fill=True,
                        opacity=0.7
                       ).add_to(m)
linear.caption = 'Price'
linear.add_to(m)


def auto_open(path):
    html_page = f'{path}'
    m.save(html_page)
    # open in browser.
    new = 2
    webbrowser.open(html_page, new=new)

auto_open('testing.html')

