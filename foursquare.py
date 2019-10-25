import requests  #access APIs
import folium  #create map
import pandas as pd  #data manipulation
import matplotlib.pyplot as plt  #scatterplots
from math import sin,cos,sqrt,asin,atan2,pow,acos  #operations to convert spherical to cartesian
import utm #utm module for lat/lon to x/y
from geopy.geocoders import Nominatim  #geolocator data
from datetime import datetime  #date for API requests


df=pd.DataFrame(columns=['name','population','zip'],data=[])
df=df[['zip','population']]
df=df.sort_values(by=['zip']).reset_index(drop=True)
df=df.astype(int)


address='Cleveland, OH'
geolocator = Nominatim(user_agent="cle_bars")
location = geolocator.geocode(address)
latitude = location.latitude
longitude = location.longitude
map_cle = folium.Map(location=[latitude, longitude], zoom_start=12)

df['lat']=[]
df['lon']=[]

url = 'https://api.foursquare.com/v2/venues/explore'

params = dict(
  client_id='DYLLTWFBCB0RPXB3RKFNAWYZGXGJMGCKPGMPG4LEKLQ4MFSL',
  client_secret='TBKXLTH2RESZKL5FFAF1I5HKQF1AERA0WKRKXY444YCHT1KO',
  v=datetime.today().strftime('%Y%m%d'),
  ll='41.5051613,-81.6934446',
  query='bar',
  limit=100,
  radius=1609*10 # miles from location
)
resp = requests.get(url=url, params=params).json()
r = resp['response']['groups'][0]['items']
lat=[]
lon=[]
name=[]
for i in r:
      name.append(i['venue']['name'])
      lat.append(i['venue']['location']['lat'])
      lon.append(i['venue']['location']['lng']) 
ch=pd.DataFrame(list(zip(name,lat,lon)),columns=['Name','lat','lon'])

for name,lat,lon in zip(ch['Name'],ch['lat'],ch['lon']):
    label = "{}".format(name)
    label = folium.Popup(label, parse_html=True)
    folium.CircleMarker(
        [lat, lon],
        radius=5,
        popup=label,
        color='#daa520',
        fill=True,
        fill_color='#daa520',
        fill_opacity=0.5,
        parse_html=False).add_to(map_cle)
    
map_cle
