

import streamlit as st 
import warnings
import folium


from streamlit_folium import st_folium



header = st.container()
body = st.container()
home_sidebar = st.container()






with header:
	st.image('https://media.licdn.com/dms/image/v2/D4D12AQEo894zSr1O3w/article-cover_image-shrink_720_1280/article-cover_image-shrink_720_1280/0/1714114002782?e=2147483647&v=beta&t=_gvb2B4js5cY2DLt_fS8MtqJfpmy8LZmppYB6qPJVJY',  width=900)


with body:

	# ================== About Us ================== ================== #

	 st.write("<h3 style='text-align: left; color: #3EA99F; margin-bottom: 1px;'>About Us</h3>", unsafe_allow_html=True)
	 st.write("<h4 style='text-align: left; color: #3EA99F; margin-bottom: 1px;'>We Work to Alleviate Human Suffering</h3>", unsafe_allow_html=True)

	 st.write('''

	 		GeoSister is a women-led company aimed at transforming how communities across Africa prepare for 
	 		and respond to disasters. Leveraging the power of satellite imagery, geospatial intelligence, and mobile communication, GeoSister provides an interactive 
	 		platform that maps disaster-prone areas, tracks climate patterns, and delivers real-time alerts via SMS and USSD to even the most remote regions. 

	 		\nOur mission is to democratize access to life-saving information by combining space technology with grassroots reach—empowering women, youth, and local 
	 		communities to become active agents in resilience and disaster management. At GeoSister, we believe that safety is not a privilege—it’s a right, and we’re
	 		mapping a future where every African, regardless of geography or gender, can thrive in the face of adversity.

	 		''')





	# ================== Our Services ================== ================== #

	 st.write("<h3 style='text-align: left; color: #3EA99F; margin-bottom: 1px;'>What We Do</h3>", unsafe_allow_html=True)

	 disaster_mgt, health, youth_dvp = st.columns(3, vertical_alignment="center")
	 special_pgm, natl_society, crisis_resp = st.columns(3, vertical_alignment="center")

	 with disaster_mgt:
	 	cont1 = st.container(border=True)
	 	cont1.write("<h5 style='text-align: center; margin-bottom: 1px;'>🚨 Disaster Management</h5>", unsafe_allow_html=True)
	 	cont1.write('''The department provides immediate relief to affected populations to save lives, protect livelihoods, and strengthen recovery from disasters 
	 		and crisis''')


	 with health:
	 	cont2 = st.container(border=True)
	 	cont2.write("<h5 style='text-align: center; margin-bottom: 1px;'>🚑 Health</h5>", unsafe_allow_html=True)
	 	cont2.write('''The health department embraces the integration approach to ensure affordable, accessible and equitable community-based health care.''') 


	 with youth_dvp:
	 	cont3 = st.container(border=True)
	 	cont3.write("<h5 style='text-align: center; margin-bottom: 1px;'>🛃 Youth Development</h5>", unsafe_allow_html=True)
	 	cont3.write('''In a bid to promote youth-led volunteerism and sustainable action, the department has created You-Red spaces, that are open to all young people interested.''') 


	 with special_pgm:
	 	cont4 = st.container(border=True)
	 	cont4.write("<h5 style='text-align: center; margin-bottom: 1px;'>🦺 Special Programmes</h5>", unsafe_allow_html=True)
	 	cont4.write('''GeoSisters has special programmes that cater for special needs of vunerable communities accross the country.''') 


	 with natl_society:
	 	cont5 = st.container(border=True)
	 	cont5.write("<h5 style='text-align: center; margin-bottom: 1px;'>🎯 National Society \nDevelopment</h5>", unsafe_allow_html=True)
	 	cont5.write('''Organizational Development focuses on the capacity of KRCS to adequetely perform its mandate, this includes branches and volunteers.''') 


	 with crisis_resp: 
	 	cont5 = st.container(border=True)
	 	cont5.write("<h5 style='text-align: center; margin-bottom: 1px;'>🧯 Crisis Response</h5>", unsafe_allow_html=True)
	 	cont5.write('''Organizational Development focuses on the capacity of KRCS to adequetely perform its mandate, this includes branches and volunteers.''') 


	 # ================== Our Partners ================== ================== #

	 st.write("<h3 style='text-align: left; color: #3EA99F; margin-bottom: 1px;'>Our Partners</h3>", unsafe_allow_html=True)
	 # st.write("<h6 style='text-align: left; margin-bottom: 1px;'>here are some of our partners</h6>", unsafe_allow_html=True)

	 col1, col2, col3, col4, col5, col6, col7 = st.columns(7)

	 with col1:
	 	st.image('./src/AT_Color-71519b9f-5507-4527-a596-45a7698d82b7.png', width=150)

	 with col2:
	 	st.image('./src/PartnersArtboard-58-copy-19@3x.png', width=150)

	 with col3:
	 	st.image('./src/The_global_fund_logo.png', width=150)

	 with col4:
	 	st.image('./src/pngimg.com - google_PNG19644.png', width=150)

	 with col5:
	 	st.image('./src/PartnersArtboard-58-copy-2@3x.png', width=150)

	 with col6:
	 	st.image('./src/PartnersArtboard-58-copy-16@3x.png', width=150)

	 with col7:
	 	st.image('./src/Team-2Artboard-58@3x.png', width=150)



	 # ================== Contact US ================== ================== #	

	 st.write("<h3 style='text-align: left; color: #3EA99F; margin-bottom: 1px;'>Contact Us</h3>", unsafe_allow_html=True)

	 loc_map, loc_text = st.columns(2)

	 with loc_map:

	 	# Coordinates for Africa's Talking HQ
	 	location = [-1.2921, 36.7765]

	 	# Create the folium map
	 	m = folium.Map(location=location, zoom_start=12)

	 	folium.Marker(
	 		location,
	 		popup="GeoSister",
	 		tooltip="Click for more info",
	 		icon=folium.Icon(color="blue", icon="info-sign"),
	 		).add_to(m)

	 	st_folium(m, width=900, height=300)


	 with loc_text:
	 	st.write('')
	 	st.write('')
	 	st.write("<h6 style='text-align: left; margin-bottom: 1px;'>🏢 Apple Cross 23 - Lavington</h6>", unsafe_allow_html=True)
	 	st.write("<h6 style='text-align: left; margin-bottom: 1px;'>📬 P.O. Box 00200</h6>", unsafe_allow_html=True)
	 	st.write("<h6 style='text-align: left; margin-bottom: 1px;'>📌 Nairobi, Kenya</h6>", unsafe_allow_html=True)
	 	st.write("<h6 style='text-align: left; margin-bottom: 1px;'>📞 Tel: +254 71234 5678</h6>", unsafe_allow_html=True)
	 	st.write("<h6 style='text-align: left; margin-bottom: 1px;'>📧 Email: info@echominds.africa</h6>", unsafe_allow_html=True)



