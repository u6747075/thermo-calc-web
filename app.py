import os
import streamlit as st
from views.app_tab1 import render_story_tab
# from vertexai.preview.generative_models import GenerativeModel
# import vertexai
import logging
leave_warning_js = """
<script>
window.addEventListener('beforeunload', function (e) {
  // Custom message
  var confirmationMessage = "Are you sure you want to leave this page? You may lose unsaved changes.";
  (e || window.event).returnValue = confirmationMessage; // Gecko + IE
  return confirmationMessage; // Gecko + Webkit, Safari, Chrome etc.
});
</script>
"""

st.components.v1.html(leave_warning_js,height=1,width=1)
# Inject JavaScript into the Streamlit app
# from google.cloud import logging as cloud_logging

# configure logging
logging.basicConfig(level=logging.INFO)



st.header("Thermo Calcs", divider="rainbow")

st.session_state["outer_hist"]=[]
tab1, tab2, = st.tabs(["Home", "Record"])

with tab1:
    render_story_tab()
from views.app_tab_3 import render_objects
with tab2:
    render_objects()
# with tab3:
#     st.title("Coming soon")
    
# # from views.app_tab_4 import login
# with tab4:
#     st.write("Coming soon")
#     # login()
    
