import os
import streamlit as st
from views.app_tab1 import render_story_tab
# from vertexai.preview.generative_models import GenerativeModel
# import vertexai
import logging
# from google.cloud import logging as cloud_logging

# configure logging
logging.basicConfig(level=logging.INFO)

st.header("Thermo Calcs", divider="rainbow")

st.session_state["outer_hist"]=[]
tab1, tab2, tab3 = st.tabs(["Home", "Colour Mapper", "Record"])

with tab1:
    render_story_tab()
from views.app_tab_3 import render_objects
with tab3:
    render_objects()
with tab2:
    st.title("Coming soon")
    
