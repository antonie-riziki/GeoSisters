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
OCG = OpenCageGeocode(os.getenv("OPENCAGE_API_KEY"))

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




# Initialize session state
if 'reports' not in st.session_state:
    st.session_state.reports = []

# Helper: Get lat/lon from location
def get_coordinates(location):
    try:
        results = OCG.geocode(location)
        if results:
            lat = results[0]['geometry']['lat']
            lng = results[0]['geometry']['lng']
            return lat, lng
    except Exception as e:
        st.error(f"Geocoding error: {e}")
    return None, None

# Page title
# st.title("📍 Community Disaster Reporting Map")

with st.expander("➕ Report a New Disaster Event", expanded=True):
    with st.form("report_form"):
        col1_1, col1, col2, col3 = st.columns(4)

        with col1_1:
            names = st.text_input(" Reporter Name", placeholder="e.g. Jane Doe")
            phone_number = st.number_input("📌 Reporter Name", placeholder="e.g. 0743158232", value=None, min_value=0, max_value=int(10e10))

        with col1:
            region = st.selectbox("🌍 Region", placeholder="e.g. Sub-Saharan Africa", options=data['Region'].unique())
            country = st.selectbox("🏳️ Country", placeholder="e.g. Kenya", options=data['Country'].unique())

        with col2:
            location = st.text_input("📌 Location Name", placeholder="e.g. Nairobi CBD")
            disaster_group = st.selectbox("🚨 Disaster Group", options=data['Disaster Subgroup'].unique())

        with col3:
            disaster_type = st.selectbox("🔸 Disaster Type", placeholder="e.g. Flood", options=data['Disaster Type'].unique())
            disaster_subtype = st.selectbox("🔹 Disaster Subtype", placeholder="e.g. Flash Flood", options=data['Disaster Subtype'].unique())

        submit = st.form_submit_button("📤 Submit Disaster Details", use_container_width=True)

        if submit:
            lat, lon = get_coordinates(f"{location}, {country}")

            recipients = [f"+254{str(phone_number)}"]

            # airtime_rec = "+254" + str(phone_number)

            print(recipients)
            print(phone_number)

            # Set your message
            message = f"Hi {names}, Thank you for reporting the disaster event. Your information has been received. Stay safe, stay informed"
            # Set your shortCode or senderId
            sender = 20880

            try:
                # responses = airtime.send(phone_number=airtime_rec, amount=amount, currency_code=currency_code)
                response = sms.send(message, recipients, sender)

                print(response)

                # print(responses)

            except Exception as e:
                print(f'Houston, we have a problem: {e}')

            st.toast(f"Account Created Successfully")

            if lat and lon:
                report = {
                    "Region": region,
                    "Country": country,
                    "Location": location,
                    "Disaster Group": disaster_group,
                    "Disaster Type": disaster_type,
                    "Disaster Subtype": disaster_subtype,
                    "Latitude": lat,
                    "Longitude": lon
                }
                st.session_state.reports.append(report)
                st.success("✅ Disaster reported successfully and added to map.")
            else:
                st.error("❌ Could not get coordinates. Please try a more precise location.")

# Create a map and add the reported disasters
m = folium.Map(location=[0, 20], zoom_start=3)
marker_cluster = MarkerCluster().add_to(m)

# Plot reported disasters
for report in st.session_state.reports:
    popup_html = (
        f"<b>Region:</b> {report['Region']}<br>"
        f"<b>Country:</b> {report['Country']}<br>"
        f"<b>Location:</b> {report['Location']}<br>"
        f"<b>Group:</b> {report['Disaster Group']}<br>"
        f"<b>Type:</b> {report['Disaster Type']}<br>"
        f"<b>Subtype:</b> {report['Disaster Subtype']}"
    )
    folium.Marker(
        location=[report['Latitude'], report['Longitude']],
        popup=popup_html,
        tooltip=report['Location']
    ).add_to(marker_cluster)

# Display the map
st.subheader("🗺️ Reported Disaster Map")
st_folium(m, width=1200, height=600)
























