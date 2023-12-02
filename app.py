import pandas as pd
import numpy as np
import plotly.figure_factory as ff
import plotly.graph_objects as go
import streamlit as st
from streamlit_option_menu import option_menu

from audio_recorder_streamlit import audio_recorder
import wave
import time

from ibm_watson import SpeechToTextV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

PAGE_CONFIG = {"page_title": "Healthy Buddy",
               "page_icon": "icon.jpg", "layout": "centered"}
st.set_page_config(**PAGE_CONFIG)

page_bg_img = f"""
<style>
[data-testid="stAppViewContainer"] > .main {{
background-image: url("https://img.freepik.com/premium-photo/green-background-with-bokeh-rays_582451-37.jpg");
background-size: cover;
background-position: top left;
background-repeat: no-repeat;
}}
[data-testid="stHeader"] {{
background: rgba(0,0,0,0);
}}
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)

menu = ["About", "Set Goals", "Plan Schedule", "Kids Space", "Notes"]

if 'goal_df' not in st.session_state:
    st.session_state['goal_df'] = None

if 'schedule_df' not in st.session_state:
    st.session_state['schedule_df'] = None

with st.sidebar:
    selected = option_menu(
        menu_title = None,
        options = menu,
        icons = ['house', 'bullseye', 'card-checklist', 'emoji-smile', 'journal']
    )
    name = st.text_input("Enter kid's name: ")

if selected == 'About':
    st.markdown("<h1 style='text-align: center;'>Healthy Buddy</h1>", unsafe_allow_html=True)
    st.markdown("*Welcome to Healthy Buddy, a holistic approach to fostering a balanced and healthy lifestyle for both kids and parents. Our website is designed with the goal of assisting families in regulating and optimizing their daily routines. We understand the challenges parents face in managing their children's time effectively, from ensuring adequate sleep and study hours to monitoring screen time and promoting physical activities. Healthy Buddy provides a user-friendly platform where parents can set personalized goals for their kids, tailoring schedules that encompass study sessions, sleep patterns, screen time, physical exercise, and social interactions.*")
    st.markdown(" ")
    st.markdown("*At Healthy Buddy, we believe that a well-structured routine contributes to a child's overall well-being. The **Set Goals** feature empowers parents to define achievable objectives for their kids, promoting a healthy balance between education, leisure, and social engagement. The **Plan Schedule** section allows parents to create daily planners, outlining specific timeframes for various activities. Our platform not only helps in setting goals but also generates visual schedules, making it easy for both parents and children to follow and track progress.*")
    st.markdown(" ")
    st.markdown("*In the **Kids Space** section, each child gets their personalized space, displaying their set goals and daily schedules. Parents can monitor their child's progress and access insightful charts illustrating the distribution of time across different activities. Additionally, our website offers a unique **Notes** feature, allowing kids to add voice notes, fostering self-expression and creativity. Join us on the journey to cultivate healthy habits, enabling children to thrive both academically and emotionally with Healthy Buddy.*")

if selected == 'Set Goals':
    if name != '':
        st.title('Set Goals for ' + name.capitalize())
        st.markdown('*Make a planner for your child. Enter their daily goals here.*')
        
        for i in range(3):
            st.markdown(" ")

        st.markdown('**Study**')
        c1, c2 = st.columns(2)
        study_regulation = c1.selectbox('Choose regulation:', ('', 'Increase', 'Keep the same', 'Decrease'), key = '1')
        study_hrs = c2.slider('Hours', min_value=0, max_value=5, value=0, step=1, key = '6')

        st.markdown('**Sleep**')
        c1, c2 = st.columns(2)
        sleep_regulation = c1.selectbox('Choose regulation:', ('', 'Increase', 'Keep the same', 'Decrease'), key = '2')
        sleep_hrs = c2.slider('Hours', min_value=0, max_value=5, value=0, step=1, key = '7')

        st.markdown('**Screen Time**')
        c1, c2 = st.columns(2)
        screen_time_regulation = c1.selectbox('Choose regulation:', ('', 'Increase', 'Keep the same', 'Decrease'), key = '3')
        screen_time_hrs = c2.slider('Hours', min_value=0, max_value=5, value=0, step=1, key = '8')

        st.markdown('**Physical Exercise**')
        c1, c2 = st.columns(2)
        phy_regulation = c1.selectbox('Choose regulation:', ('', 'Increase', 'Keep the same', 'Decrease'), key = '4')
        phy_hrs = c2.slider('Hours', min_value=0, max_value=5, value=0, step=1, key = '9')

        st.markdown('**Social Time**')
        c1, c2 = st.columns(2)
        social_time_regulation = c1.selectbox('Choose regulation:', ('', 'Increase', 'Keep the same', 'Decrease'), key = '5')
        social_time_hrs = c2.slider('Hours', min_value=0, max_value=5, value=0, step=1, key = '10')

        if st.button('Publish Goals'):
            goal_dict = {'Activity': ['Study', 'Sleep', 'Screen Time', 'Physical Exercise', 'Social Time'],
                         'Action': [study_regulation, sleep_regulation, screen_time_regulation, phy_regulation, social_time_regulation],
                         'Hours': [study_hrs, sleep_hrs, screen_time_hrs, phy_hrs, social_time_hrs]}
            
            df = pd.DataFrame(goal_dict)
            df['Hours'].apply(np.ceil)
            st.dataframe(df, width = 10**3)
            st.session_state['goal_df'] = df

    else:
        st.header("Kindly enter kid's name in the sidebar to continue.")

if selected == 'Plan Schedule':
    if name != '':
        st.title('Plan Schedule for ' + name.capitalize())
        st.markdown('*Build planner for your kid.*')

        for i in range(3):
            st.markdown(" ")

        st.markdown('**Set Study Time**')
        st.markdown(" ")
        c1, c2, c3, c4, c5, c6, c7 = st.columns(7)
        c1.markdown('**Start**')
        c5.markdown('**End**')
        c1, c2, c3, c4, c5, c6, c7 = st.columns(7)
        s_h1 = c1.text_input('Hrs', key = '11')
        s_m1 = c2.text_input('Min', key = '12')
        s_t1 = c3.selectbox('Time', ('', 'AM', 'PM'), key = '13', label_visibility = 'hidden')
        e_h1 = c5.text_input('Hrs', key = '14')
        e_m1 = c6.text_input('Min', key = '15')
        e_t1 = c7.selectbox('Time', ('', 'AM', 'PM'), key = '16', label_visibility = 'hidden')
        
        for i in range(3):
            st.markdown(" ")

        st.markdown('**Set Sleep Time**')
        st.markdown(" ")
        c1, c2, c3, c4, c5, c6, c7 = st.columns(7)
        c1.markdown('**Start**')
        c5.markdown('**End**')
        c1, c2, c3, c4, c5, c6, c7 = st.columns(7)
        s_h2 = c1.text_input('Hrs', key = '17')
        s_m2 = c2.text_input('Min', key = '18')
        s_t2 = c3.selectbox('Time', ('', 'AM', 'PM'), key = '19', label_visibility = 'hidden')
        e_h2 = c5.text_input('Hrs', key = '20')
        e_m2 = c6.text_input('Min', key = '21')
        e_t2 = c7.selectbox('Time', ('', 'AM', 'PM'), key = '22', label_visibility = 'hidden')
    
        for i in range(3):
            st.markdown(" ")

        st.markdown('**Set Screen Time**')
        st.markdown(" ")
        c1, c2, c3, c4, c5, c6, c7 = st.columns(7)
        c1.markdown('**Start**')
        c5.markdown('**End**')
        c1, c2, c3, c4, c5, c6, c7 = st.columns(7)
        s_h3 = c1.text_input('Hrs', key = '23')
        s_m3 = c2.text_input('Min', key = '24')
        s_t3 = c3.selectbox('Time', ('', 'AM', 'PM'), key = '25', label_visibility = 'hidden')
        e_h3 = c5.text_input('Hrs', key = '26')
        e_m3 = c6.text_input('Min', key = '27')
        e_t3 = c7.selectbox('Time', ('', 'AM', 'PM'), key = '28', label_visibility = 'hidden')

        for i in range(3):
            st.markdown(" ")

        st.markdown('**Set Physical Exercise Time**')
        st.markdown(" ")
        c1, c2, c3, c4, c5, c6, c7 = st.columns(7)
        c1.markdown('**Start**')
        c5.markdown('**End**')
        c1, c2, c3, c4, c5, c6, c7 = st.columns(7)
        s_h4 = c1.text_input('Hrs', key = '29')
        s_m4 = c2.text_input('Min', key = '30')
        s_t4 = c3.selectbox('Time', ('', 'AM', 'PM'), key = '31', label_visibility = 'hidden')
        e_h4 = c5.text_input('Hrs', key = '32')
        e_m4 = c6.text_input('Min', key = '33')
        e_t4 = c7.selectbox('Time', ('', 'AM', 'PM'), key = '34', label_visibility = 'hidden')

        for i in range(3):
            st.markdown(" ")

        st.markdown('**Set Social Time**')
        st.markdown(" ")
        c1, c2, c3, c4, c5, c6, c7 = st.columns(7)
        c1.markdown('**Start**')
        c5.markdown('**End**')
        c1, c2, c3, c4, c5, c6, c7 = st.columns(7)
        s_h5 = c1.text_input('Hrs', key = '35')
        s_m5 = c2.text_input('Min', key = '36')
        s_t5 = c3.selectbox('Time', ('', 'AM', 'PM'), key = '37', label_visibility = 'hidden')
        e_h5 = c5.text_input('Hrs', key = '38')
        e_m5 = c6.text_input('Min', key = '39')
        e_t5 = c7.selectbox('Time', ('', 'AM', 'PM'), key = '40', label_visibility = 'hidden')

        if st.button('Publish Schedule'):
            schedule_dict = {'Activity': ['Study', 'Sleep', 'Screen Time', 'Physical Exercise', 'Social Time'],
                         'Start': [s_h1 + ':' + s_m1 + ' ' + s_t1, 
                                   s_h2 + ':' + s_m2 + ' ' + s_t2,
                                   s_h3 + ':' + s_m3 + ' ' + s_t3,
                                   s_h4 + ':' + s_m4 + ' ' + s_t4,
                                   s_h5 + ':' + s_m5 + ' ' + s_t5],
                         'End': [e_h1 + ':' + e_m1 + ' ' + e_t1, 
                                e_h2 + ':' + e_m2 + ' ' + e_t2,
                                e_h3 + ':' + e_m3 + ' ' + e_t3,
                                e_h4 + ':' + e_m4 + ' ' + e_t4,
                                e_h5 + ':' + e_m5 + ' ' + e_t5]}
            
            sch_df = pd.DataFrame(schedule_dict)
            st.dataframe(sch_df, width = 10**3)
            st.session_state['schedule_df'] = sch_df

    else:
        st.header("Kindly enter kid's name in the sidebar to continue.")

if selected == 'Kids Space':
    if name != '':
        st.title(name.capitalize() + "'s Space")

        if st.session_state['goal_df'] is not None:
            st.markdown('*Goals for you*')
            st.dataframe(st.session_state['goal_df'], width = 10**3)
        else:
            st.markdown('*No active goals available.*')
            st.markdown(' ')

        if st.session_state['schedule_df'] is not None:
            st.markdown('*Your suggested schedule for the day*')
            st.dataframe(st.session_state['schedule_df'], width = 10**3)
        else:
            st.markdown('*Schedule not published for today.*')
            st.markdown(' ')

        st.markdown("*Progress Report*")

        def get_charts():
            labels = ['Study','Sleep','Physical Activity','Social', 'Screen']
            values = [45, 25, 10, 50]
            fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.3)])
            st.plotly_chart(fig, theme="streamlit")

            x1 = np.random.randn(200)-2
            x2 = np.random.randn(200)
            x3 = np.random.randn(200)+2
            x4 = np.random.randn(200)+4
            x5 = np.random.randn(200)-4
            hist_data = [x1, x2, x3, x4, x5]
            group_labels = ['Study','Sleep','Physical Activity','Social', 'Screen']
            fig = ff.create_distplot(hist_data, group_labels, bin_size=[.1, .25, .5, 1, 0.25])
            st.plotly_chart(fig, theme="streamlit")

        get_charts()

    else:
        st.header("Kindly enter kid's name in the sidebar to continue.")

if selected == 'Notes':
    st.title('Notes')
    st.markdown('*Click the icon to add new note.*')
    c1, c2, c3, c4, c5, c6, c7, c8 = st.columns(8)
    with c1:
      audio_bytes = audio_recorder(text="Add", icon_size="0.5x", pause_threshold=10.0)
    try:
      if audio_bytes:
        st.audio(audio_bytes, format="audio/wav")
        
        apiUrl = "https://api.eu-gb.speech-to-text.watson.cloud.ibm.com/instances/5f9e33da-3d8f-4924-9b18-2ef9c3dd288d"
        myKey = "7NwfZMJOeoVniUj5-XIFYclesdc0VjHzkPZPDBigsD8Y"
    
        auth = IAMAuthenticator(myKey)
        Speech2Text = SpeechToTextV1(authenticator = auth)
        Speech2Text.set_service_url(apiUrl)
    
        response = Speech2Text.recognize(audio = audio_bytes, content_type = "audio/wav")
        recognized_text = response.result['results'][0]['alternatives'][0]['transcript']
        st.markdown(" ")
        st.markdown("*Content Recognized*")
        st.info(recognized_text)
    
        st.markdown(" ")
        time.sleep(2)
        st.success('Note Saved!')
    except:
      st.error('Try recording again.')
