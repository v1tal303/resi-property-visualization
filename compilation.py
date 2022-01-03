import folium
from folium import plugins
import branca
import branca.colormap as cm
from IPython.display import display
import webbrowser
import pandas as pd


class MapPlotter:

    def __init__(self, data):
        # clean_price = pd.to_numeric(data['propertyPrice'], errors='coerce')
        # print(clean_price.columns)
        # self.data = clean_price
        self.data = data

        self.m = folium.Map([self.data['latitude'][1], self.data['longitude'][1]], zoom_start=10,
                            tiles="CartoDB positron")
        self.linear = cm.linear.RdYlBu_09.scale(50000, 500000)


    # Reverses the color map
    def reversed_colormap(self, existing):
        return cm.LinearColormap(
            colors=list(reversed(existing.colors)),
            vmin=existing.vmin, vmax=existing.vmax)

    # Generates the map, saves it as a html file and opens it. Should provide file name
    def generate_map(self, path):
        self.linear = self.reversed_colormap(self.linear)
        for index, row in self.data.iterrows():
            try:
                html = f'''<b><font size=5><font face=Arial>{self.data['propertyBeds'].loc[index]} bed {self.data['propertyType'].loc[index]}</b><br>
                <br>
                <font size=3>Price: £{self.data['propertyPrice'].loc[index]}<br>
                <br>
                Address: {self.data['propertyAddress'].loc[index]}<br>
                <br>
                <a href={self.data['propertyLink'].loc[index]} target="_blank">Link to property</a><br>'''
            except:
                html = f'''<b><font size=5><font face=Arial>{self.data['propertyType'].loc[index]}</b><br>
                <br>
                <font size=3>Price: £{self.data['propertyPrice'].loc[index]}<br>
                <br>
                Address: {self.data['propertyAddress'].loc[index]}<br>
                <br>
                <a href={self.data['propertyLink'].loc[index]} target="_blank">Link to property</a><br>'''

            iframe = folium.IFrame(html,
                                   width=300,
                                   height=300)

            popup = folium.Popup(iframe,
                                 max_width=300)

            folium.CircleMarker([row['latitude'], row['longitude']],
                                radius=10,
                                popup=popup,
                                fill_color=self.linear(int(self.data['propertyPrice'].loc[index])),
                                color=self.linear(int(self.data['propertyPrice'].loc[index])),
                                fill=True,
                                opacity=0.7
                                ).add_to(self.m)
        self.linear.caption = 'Price'
        self.linear.add_to(self.m)
        html_page = f'{path}'
        self.m.save(html_page)
        # open in browser.
        new = 2
        webbrowser.open(html_page, new=new)
