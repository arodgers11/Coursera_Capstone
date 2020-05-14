import requests

import folium


import pandas as pd

import matplotlib.pyplot as plt

from math import sin,cos,sqrt

from geopy.geocoders import Nominatim

url='https://api.census.gov/data/2017/acs/acs5/subject'

key='7bad81938d25611bd2d0362e77c32f0594ea0243'

zips='44301,44302,44303,44304,44305,44306,44307,44308,44310,44311,44313,44314,44320'

call='%s?key=%s&get=NAME,S0101_C01_001E&for=zip%%20code%%20tabulation%%20area:%s'

call = call % (url,key,zips)

resp=requests.get(call).json()

df=pd.DataFrame(columns=['name','population','zip'],data=resp[1:])

df=df[['zip','population']]

df=df.sort_values(by=['zip']).reset_index(drop=True)

df=df.astype(int)

git='https://github.com/arodgers11/Coursera_Capstone/blob//master/centerzips.txt?raw=True'

df2 = pd.read_csv(git,sep=",",header=0)

df['lat']=df2['LAT']

df['lng']=df2['LNG']

address='Akron, OH'
geolocator = Nominatim(user_agent="akron_zips")
location = geolocator.geocode(address)
latitude = location.latitude
longitude = location.longitude
map_akron = folium.Map(location=[latitude, longitude], zoom_start=10)

for lat, lng, zipcode, pop in zip(df['lat'], df['lng'], df['zip'],df['population']):
    label = "zip:{}\n pop:{}".format(zipcode,pop)
    label = folium.Popup(label, parse_html=True)
    folium.CircleMarker(
        [lat, lng],
        radius=5,
        popup=label,
        color='#ce1141',
        fill=True,
        fill_color='#ce1141',
        fill_opacity=0.7,
        parse_html=False).add_to(map_akron)
    
map_akron

R = 6371
x=[0]*len(df)
y=[0]*len(df)
for i in range(0,len(df)):
    lat=df['lat'][i]
    lng=df['lng'][i]
    x[i]= R * cos(lat*3.1415/180) * cos(lng*3.1415/180)
    y[i] = R * cos(lat*3.1415/180) * sin(lng*3.1415/180)
df['x']=x
df['y']=y

plt.plot(df['x'],df['y'],'ro')
plt.show()

def distance(x,y,x1,y1):
    return (float(x)-x1)**2+(float(y)-y1)**2

with open('df.csv','w') as f:
    df.to_csv(f,index=False)