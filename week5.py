import requests  #access APIs
import folium  #create map
import pandas as pd  #data manipulation
import matplotlib.pyplot as plt  #scatterplots
from math import sin,cos,sqrt,asin,atan2,pow,acos  #operations to convert spherical to cartesian
import utm #utm module for lat/lon to x/y
from geopy.geocoders import Nominatim  #geolocator data
from datetime import datetime  #date for API requests

#get census data for zip codes
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
df['lon']=df2['LNG']

address='Akron, OH'
geolocator = Nominatim(user_agent="akron_zips")
location = geolocator.geocode(address)
latitude = location.latitude
longitude = location.longitude
map_akron = folium.Map(location=[latitude, longitude], zoom_start=12)

for lat, lon, zipcode, pop in zip(df['lat'], df['lon'], df['zip'],df['population']):
    label = "zip:{}\n pop:{}".format(zipcode,pop)
    label = folium.Popup(label, parse_html=True)
    folium.CircleMarker(
        [lat, lon],
        radius=5,
        popup=label,
        color='#ce1141',
        fill=True,
        fill_color='#ce1141',
        fill_opacity=0.5,
        parse_html=False).add_to(map_akron)
    
df.head()

ch=pd.read_csv("https://github.com/arodgers11/Coursera_Capstone/blob/master/ch.csv?raw=true",sep=",",header=0)
ch.head()

url = 'https://api.foursquare.com/v2/venues/explore'

params = dict(
  client_id='DYLLTWFBCB0RPXB3RKFNAWYZGXGJMGCKPGMPG4LEKLQ4MFSL',
  client_secret='TBKXLTH2RESZKL5FFAF1I5HKQF1AERA0WKRKXY444YCHT1KO',
  v=datetime.today().strftime('%Y%m%d'),
  ll='41.075576, -81.511134', # UA campus lat/long
  query='chinese',
  limit=40,
  radius=1609*3.5 # miles from location
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
        parse_html=False).add_to(map_akron)
    
map_akron

x=[0]*len(ch)
y=[0]*len(ch)
for i in range(0,len(ch)):
    lat=ch['lat'][i]
    lon=ch['lon'][i]
    x[i]=utm.from_latlon(lat,lon)[0]
    y[i]=utm.from_latlon(lat,lon)[1]
with open('ch.csv','w') as f:
    ch.to_csv(f,index=False)

x=[0]*len(df)
y=[0]*len(df)
for i in range(0,len(df)):
    lat=df['lat'][i]
    lon=df['lon'][i]
x[i]=utm.from_latlon(lat,lon)[0]
y[i]=utm.from_latlon(lat,lon)[1]
df['x']=x
df['y']=y

with open('df.csv','w') as f:
    df.to_csv(f,index=False)
  
pp=pd.read_csv("https://github.com/arodgers11/Coursera_Capstone/blob/master/potential_points.csv?raw=true",sep=",",header=0)
pp.head()

pp['lat']=[float(0)]*len(pp)
pp['lon']=[float(0)]*len(pp) 
for i in range(0,len(pp)):
    pp['lat'][i]=utm.to_latlon(pp['x'][i],pp['y'][i],zone_number=17,zone_letter='U')[0]
    pp['lon'][i]=utm.to_latlon(pp['x'][i],pp['y'][i],zone_number=17,zone_letter='U')[1]
    
with open('potential_points.csv','w') as f:
    pp.to_csv(f,index=False)
    
for name,lat,lon in zip(pp['Location'],pp['lat'],pp['lon']):
    label = "{}".format(name)
    label = folium.Popup(label, parse_html=True)
    folium.CircleMarker(
    [lat, lon],
    radius=5,
    popup=label,
    color='#0000ff',
    fill=True,
    fill_color='#0000ff',
    fill_opacity=0.5,
    parse_html=False).add_to(map_akron)
map_akron