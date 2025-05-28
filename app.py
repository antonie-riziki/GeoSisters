
import streamlit as st 


reg_page = st.Page("./pgs/registration.py", title="🚺 register")
signin_page = st.Page("./pgs/signin.py", title="🪧 sign in")
home_page = st.Page("./pgs/main.py", title="🏠 home page")
mapping_page = st.Page("./pgs/mapping.py", title="🗺️ GeoView 360")
report_page = st.Page("./pgs/report.py", title="Report", icon=":material/group_search:")
chatbot_page = st.Page("./pgs/chatbot.py", title="💭 chatbot")
# player_profile_page = st.Page("./pgs/player_profile.py", title="player profile", icon=":material/group_search:")
# player_similarity_page = st.Page("./pgs/player_similarity_search.py", title="player similarity search", icon=":material/simulation:")
# team_comparison_page = st.Page("./pgs/team_comparison.py", title="team comparison", icon=":material/group_work:")
# team_profile_page = st.Page("./pgs/team_profile.py", title="team profile", icon=":material/groups:")
# match_prediction_page = st.Page("./pgs/match_prediction.py", title="match prediction", icon=":material/online_prediction:")
# test_page = st.Page("./pgs/test.py", title="test page", icon=":material/online_prediction:")



pg = st.navigation([reg_page, signin_page, home_page, mapping_page, report_page, chatbot_page])



st.set_page_config(
    page_title="Geo Sisters",
    page_icon="🦸‍♀️",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.echominds.africa',
        'Report a bug': "https://www.echominds.africa",
        'About': "Driving Impact Through Communication \nTry *GeoSisters* and experience reality!"
    }
)


logo = "https://i.imgur.com/UbOXYAU.png"
st.sidebar.write("<h1 style='text-align: center; color: #3EA99F; margin-bottom: 1px;'>Geo Sisters</h1>", unsafe_allow_html=True)
st.sidebar.image(logo)




pg.run()



####### START: Footer
st.markdown(
    """
    <style>
        .footer {
            position: fixed;
            left: 0;
            bottom: 0;
            width: 100%;
            background-color: #f1f1f1;
            color: black;
            text-align: center;
            padding-left: 300px;
            padding-top: 20px;
        }
    </style>
    """,
    unsafe_allow_html=True,
)
st.markdown(
    """
    <div class="footer">
        <p>© 2025 EchoMinds Innovation. All rights reserved. Contact: <a href="mailto:antonriziki@gmail.com">antonriziki@gmail.com</a></p>
        <p>Visit our lab: <a href="https:echominds.africa">EchoMinds Innovation</a>.</p>
    </div>
    """,
    unsafe_allow_html=True,
)