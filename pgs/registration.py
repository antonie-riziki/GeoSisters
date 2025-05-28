import streamlit as st
import africastalking
import os
import requests
import google.generativeai as genai

from streamlit_lottie import st_lottie


from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key = os.getenv("GOOGLE_API_KEY"))

africastalking.initialize(
    username='EMID',
    api_key = os.getenv("AT_API_KEY")
)

sms = africastalking.SMS
airtime = africastalking.Airtime

col1, col2 = st.columns(2)




with col1:
	with st.form(key="user_registration"):
	    st.subheader("User Self Registration")
	    fname, sname = st.columns(2)
	    with fname:
	    	first_name = st.text_input("First Name")
	    with sname:
	    	surname = st.text_input("Surname")
	    	
	    gender_text = st.write('Gender')
	    
	    chk_male, chk_female = st.columns(2)
	    
	    with chk_male:
	    	gender = st.checkbox('Male')
	    
	    with chk_female: 
	    	gender = st.checkbox('Female')
	    
	    username = st.text_input('Username:')
	    email = st.text_input("Email: ")
	    phone_number = st.number_input("Phone Number:", value=None, min_value=0, max_value=int(10e10))
	    password = st.text_input('Passowrd', type="password")
	    confirm_password = st.text_input('Confirm password', type='password')

	    checkbox_val = st.checkbox("Subscribe to our Newsletter")

	    submit_personal_details = st.form_submit_button("Submit")

	    # Every form must have a submit button.
	    if password != confirm_password:
	    	st.error('Password mismatch', icon='⚠️')

	    else:
		    
		    if not (email and password):
		    	st.warning('Please enter your credentials!', icon='⚠️')
		    else:
		    	st.success('Proceed to engaging with the system!', icon='👉')

		    	

		    	if submit_personal_details:

			        amount = "10"
			        currency_code = "KES"

			        recipients = [f"+254{str(phone_number)}"]

			        # airtime_rec = "+254" + str(phone_number)

			        print(recipients)
			        print(phone_number)

			        # Set your message
			        message = f"Hi {first_name} ! Welcome to the GeoSisters, your trusted space for reporting and tracking disaster events in real time. Stay safe, stay informed"
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

	

	# st.write("Outside the form")


# def load_lottieurl(url: str):
# 	r = requests.get(url)
# 	if r.status_code != 200:
# 		return None
# 	else:
# 		return r.json()


with col2:
	# st.image('https://media.licdn.com/dms/image/v2/D4D12AQEo894zSr1O3w/article-cover_image-shrink_720_1280/article-cover_image-shrink_720_1280/0/1714114002782?e=2147483647&v=beta&t=_gvb2B4js5cY2DLt_fS8MtqJfpmy8LZmppYB6qPJVJY',  width=900)
	st.image('https://www.dakotasumc.org/media/library/fluid-ext-editor-widget/380/image/extedning-impact-across-the-conference-disaster-.jpg', width=800)
	st.image('https://aegex.com/images/uploads/articles/digitization-brings-real-time-situational-awareness.jpg', width=900)