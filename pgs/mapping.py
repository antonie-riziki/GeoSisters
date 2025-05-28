import streamlit as st
import pandas as pd
import africastalking
import os
import sys
import folium
import google.generativeai as genai
import streamlit.components.v1 as components, html

from opencage.geocoder import OpenCageGeocode
from streamlit_folium import st_folium

from folium.plugins import MarkerCluster
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter

sys.path.insert(1, './models')
print(sys.path.insert(1, '../models/'))

from dotenv import load_dotenv

load_dotenv()



genai.configure(api_key = os.getenv("GOOGLE_API_KEY"))

africastalking.initialize(
    username='EMID',
    api_key = os.getenv("AT_API_KEY")
)

sms = africastalking.SMS
airtime = africastalking.Airtime



df = pd.read_csv('./src/data.csv', encoding='latin1')

data = df[['Disaster Group', 'Disaster Subgroup', 'Disaster Type', 'Disaster Subtype', 'Event Name', 'Country', 'Region', 'Location', 'Magnitude', 'Magnitude Scale', 'Start Year', 'Start Month', 'Start Day', 'End Year', 'End Month', 'End Day', 'Total Deaths', 'No. Injured', 'Total Affected']].copy()

data['Location'] = data['Location'] + ', ' + data['Country']

data['Start Month'] = data['Start Month'].fillna(method='bfill')
data['Start Day'] = data['Start Day'].fillna(method='bfill')
data['End Month'] = data['End Month'].fillna(method='bfill')
data['End Day'] = data['End Day'].fillna(method='bfill')

data.dropna(subset=['End Day', 'End Month', 'Start Day'], inplace=True)


data['Start Year'] = data['Start Year'].astype(int)
data['Start Month'] = data['Start Month'].astype(int)
data['Start Day'] = data['Start Day'].astype(int)

data['End Year'] = data['End Year'].astype(int)
data['End Month'] = data['End Month'].astype(int)
data['End Day'] = data['End Day'].astype(int)



data['Start Date'] = pd.to_datetime(data['Start Year'].astype(str) + '-' +
                                    data['Start Month'].astype(str) + '-' +
                                    data['Start Day'].astype(str),
                                    errors='coerce')  

data['End Date'] = pd.to_datetime(data['End Year'].astype(str) + '-' +
                                  data['End Month'].astype(str) + '-' +
                                  data['End Day'].astype(str),
                                  errors='coerce')

data['Length in Days'] = data['End Date'] - data['Start Date']

data.drop(columns=['Start Year', 'Start Month', 'Start Day', 'End Year', 'End Month', 'End Day'], inplace=True)
# data.drop(columns=['Country'], inplace=True)



# st.dataframe(data.head(15))

# st.table(f"{data.isnull().sum()}")


# @st.dialog("AI Generated Text")
# def get_auto_params(item):
#     alert_message = st.text_input(label=f'more information about the {item}')
#     more_infor_btn = st.button('Generate')

#     if 'response' not in st.session_state:
#         st.session_state.response = "No message yet."
    
#     if more_infor_btn==True:
#         st.session_state.response = generate_auto_message(alert_message)

#     return st.session_state.response




OCG = OpenCageGeocode(os.getenv("OPENCAGE_API_KEY"))
# results = OCG.reverse_geocode(14.666, 76.833)
# st.write(results[0]['formatted'])
# Sirigedoddi, Gummagatta, India

results = OCG.geocode(u'Kencom')
# st.write(u'%f;%f;%s;%s' % (results[0]['geometry']['lat'],
#                         results[0]['geometry']['lng'],
#                         results[0]['components']['country_code'],
#                         results[0]['annotations']['timezone']['name']))


results = OCG.geocode(u'Kenya, Kencom', language='en')
# st.write(results[0]['components']['country'])



map_html = """
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.3/dist/leaflet.css" />
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@opencage/leaflet-opencage-geosearch/leaflet-opencage-geosearch.css" />
  </head>
  <body>
    <div id="map1" style="width: 100%; height: 500px;"></div>
    <script src="https://unpkg.com/leaflet@1.9.3/dist/leaflet.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/@opencage/geosearch-bundle"></script>
    <script src="https://cdn.jsdelivr.net/npm/@opencage/leaflet-opencage-geosearch"></script>
    <script>
      document.addEventListener('DOMContentLoaded', () => {
        var map = L.map('map1').setView([-1.286389, 36.817223], 6); // Centered on Nairobi, Kenya
        L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}.png', {
          attribution: '© OpenStreetMap contributors, © CARTO'
        }).addTo(map);

        var options = {
          key: '38ff8c82792943e7a68b48793f58f6ea',
          position: 'topright',
        };

        var geosearchControl = L.Control.openCageGeosearch(options).addTo(map);
      });
    </script>
  </body>
</html>
"""

# Embed the map in Streamlit
components.html(map_html, height=550)





# @st.cache_data(show_spinner=False)
# def geocode_locations(locations):
#     geolocator = Nominatim(user_agent="geoapi")
#     geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)
#     latitudes = []
#     longitudes = []
#     for loc in locations:
#         try:
#             geo = geocode(loc)
#             latitudes.append(geo.latitude if geo else None)
#             longitudes.append(geo.longitude if geo else None)
#         except:
#             latitudes.append(None)
#             longitudes.append(None)
#     return latitudes, longitudes






if 'geo_cache' not in st.session_state:
    st.session_state.geo_cache = {}

def get_coordinates(location):
    # Check cache first
    if location in st.session_state.geo_cache:
        return st.session_state.geo_cache[location]

    try:
        result = OCG.geocode(location)
        if result and len(result):
            lat = result[0]['geometry']['lat']
            lng = result[0]['geometry']['lng']
            st.session_state.geo_cache[location] = (lat, lng)
            return lat, lng
    except Exception as e:
        st.warning(f"Failed to geocode {location}: {e}")
        return None, None

    return None, None


# with st.form(key="Dataset Filter"):
col1, col2 = st.columns(2)

with col1:
    
    region = st.multiselect(label='Region', options=data['Region'].unique())

    # Filter the original dataframe (not groupby) by selected region(s)
    if region:
        filtered_by_region = data[data['Region'].isin(region)]
    else:
        filtered_by_region = data.copy()


    country = st.multiselect(label='Country', options=filtered_by_region['Country'].unique())

    if country:
        filtered_by_country = filtered_by_region[filtered_by_region['Country'].isin(country)]
    else:
        filtered_by_country = filtered_by_region.copy()



with col2:

    disaster_subgroup = st.multiselect(label='Disaster', options=filtered_by_country['Disaster Subgroup'].unique())

    if disaster_subgroup:
        filtered_by_disaster_subgroup = filtered_by_country[filtered_by_country['Disaster Subgroup'].isin(disaster_subgroup)]
    else:
        filtered_by_disaster_subgroup = filtered_by_country.copy()

    col1_1, col1_2 = st.columns(2)

    with col1_1:
      disaster_type = st.multiselect(label='Disaster Type', options=filtered_by_disaster_subgroup['Disaster Type'].unique())

      if disaster_type:
          filtered_by_disaster_type = filtered_by_disaster_subgroup[filtered_by_disaster_subgroup['Disaster Type'].isin(disaster_type)]
      else:
          filtered_by_disaster_type = filtered_by_disaster_subgroup.copy()


    with col1_2:
      disaster_subtype = st.multiselect(label='Disaster Subtype', options=filtered_by_disaster_subgroup['Disaster Subtype'].unique())

      if disaster_subtype:
          filtered_by_disaster_subtype = filtered_by_disaster_type[filtered_by_disaster_type['Disaster Subtype'].isin(disaster_subtype)]
      else:
          filtered_by_disaster_subtype = filtered_by_disaster_type.copy()


filtered = filtered_by_disaster_subtype.copy().head(100)

filtered.dropna(subset=['Location'], inplace=True)

if 'Latitude' not in filtered.columns or 'Longitude' not in filtered.columns:
    filtered['Latitude'] = None
    filtered['Longitude'] = None

for idx, row in filtered.iterrows():
    if pd.isna(row['Latitude']) or pd.isna(row['Longitude']):
        lat, lon = get_coordinates(row['Location'])
        filtered.at[idx, 'Latitude'] = lat
        filtered.at[idx, 'Longitude'] = lon



submit_btn = st.button('🌍 Map the Mayhem', use_container_width=True, type='primary')

# if submit_btn:
m = folium.Map(location=[0, 20], zoom_start=4)
marker_cluster = MarkerCluster().add_to(m)

popup_columns = [
    'Country', 'Disaster Group', 'Disaster Subtype', 'Disaster Type',
    'Event Name', 'Magnitude', 'Magnitude Scale',
    'Length in Days', 'No. Injured', 'Total Affected', 'Total Deaths'
]

for _, row in filtered.iterrows():
    if pd.notna(row['Latitude']) and pd.notna(row['Longitude']):
        popup_html = "<b>Location Info:</b><br>"
        for col in popup_columns:
            popup_html += f"<b>{col}:</b> {row[col]}<br>"

        folium.Marker(
            location=[row['Latitude'], row['Longitude']],
            popup=folium.Popup(popup_html, max_width=300),
            tooltip=row['Location']
        ).add_to(marker_cluster)

# st.title("🗺️ Disaster Events Map")
st_folium(m, width=1200, height=600)





























