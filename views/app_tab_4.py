import streamlit as st
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from urllib.parse import urlparse
import os
import json
import logging
from src.secrets import get_secret
from src.oauth import authorize,handle_callback
from streamlit_javascript import st_javascript
from werkzeug.exceptions import Unauthorized


url = "https://8080-cs-1028725031988-default.cs-asia-southeast1-ajrg.cloudshell.dev"#st_javascript("await fetch('').then(r => window.parent.location.href)")

st.write(url)

st.session_state["SECRET_KEY"] = (get_secret("streamlit-secret-key"))
st.session_state["CLIENT_SECRET"]=json.loads(get_secret('thermo-calc-app-client-secrets'))
# Save the credentials JSON locally

# Scopes for the Google Drive API
SCOPES = ['https://www.googleapis.com/auth/drive.readonly','openid']
EXTERNAL_HOST_URL=os.getenv('EXTERNAL_HOST_URL'),
def external_url(url):
    """
    Cloud Shell routes https://8080-***/ to localhost over http
    This function replaces the localhost host with the configured scheme + hostname
    """
    external_host_url = EXTERNAL_HOST_URL
    if external_host_url is None:
        # force https
        if url.startswith('http://'):
            url = f"https://{url[7:]}"
        return url

    # replace the scheme and hostname with the external host URL
    parsed_url = urlparse(url)
    replace_string = f"{parsed_url.scheme}://{parsed_url.netloc}"
    print(f"url: {url} (type: {type(url)})")
    print(f"external_host_url: {external_host_url} (type: {type(external_host_url)})")
    print(f"replace_string: {replace_string} (type: {type(replace_string)})")
    new_url = f"{external_host_url}{url[len(replace_string):]}"
    return new_url

def logout_session():
    """
    Clears known session items.
    """
    st.session_state.pop('credentials', None)
    st.session_state.pop('user', None)
    st.session_state.pop('state', None)
    st.session_state.pop('error_message', None)
    st.session_state.pop('login_return', None)
    return




def login():
    if "CLIENT_SECRET" not in st.session_state:
        st.session_state["SECRET_KEY"] = (get_secret("streamlit-secret-key"))
        st.session_state["CLIENT_SECRET"]=json.loads(get_secret('thermo-calc-app-client-secrets'))
    # Authentication step
    if "credentials" not in st.session_state:
        if 'state' not in st.session_state:
            logging.info('logging in')

            authorization_url, state = authorize(callback_uri=url,
                client_config=st.session_state['CLIENT_SECRET'],
                scopes=SCOPES)
            logging.info(f"authorization_url={authorization_url}")
            st.session_state['state'] = state
            st.write(f"[Click here to authenticate with Google]({authorization_url})")
        else:
            # Step 2: Handle the callback
            query_params = st.experimental_get_query_params()
            if 'code' in query_params and 'state' in query_params:
                code = query_params['code'][0]
                received_state = query_params['state'][0]

                callback_uri = external_url(url)
                
                try:
                    credentials, user_info = handle_callback(
                        callback_uri,
                        client_config=st.session_state['CLIENT_SECRETS'],
                        scopes=['https://www.googleapis.com/auth/drive.readonly'],
                        request_url=url,
                        stored_state=st.session_state.state,
                        received_state=received_state
                    )
                    st.session_state.credentials = credentials
                    st.session_state.user_info = user_info
                    st.success("Authentication successful!")
                except Unauthorized as e:
                    st.error(str(e))
                    st.session_state.state = None
                    st.experimental_rerun()
            else:
                st.write("Waiting for authentication callback...")
    else:
        st.write("Authenticated with Google Drive")
        credentials = Credentials(**st.session_state.credentials)
        drive_service = build('drive', 'v3', credentials=credentials)
        results = drive_service.files().list(pageSize=10, fields="files(id, name)").execute()
        items = results.get('files', [])

        if not items:
            st.write('No files found.')
        else:
            st.write('Files:')
            for item in items:
                st.write(f"{item['name']} ({item['id']})")

 

    # already logged in
    # return redirect(session.pop('login_return', url_for('.list')))
# Function to create OAuth 2.0 flow
def create_flow():
    return Flow.from_client_secrets_file(st.session_state["SECRET_KEY"], SCOPES, redirect_uri='http://localhost:8501/')


# def oauth2callback():
#     """
#     Callback destination during OAuth process.
#     """

#     # check for error, probably access denied by user
#     error = request.args.get('error', None)
#     if error:
#         st.error(error)

#     # handle the OAuth2 callback
#     credentials, user_info = oauth.handle_callback(
#         callback_uri=external_url(url_for('oauth2callback', _external=True)),
#         client_config=current_app.config['CLIENT_SECRETS'],
#         scopes=current_app.config['SCOPES'],
#         request_url=external_url(request.url),
#         stored_state=session.pop('state', None),
#         received_state=request.args.get('state', ''))

#     st.session_state['credentials'] = credentials
#     st.session_state['user'] = user_info
#     logging.info(f"user_info={user_info}")
#     return redirect(session.pop('login_return', url_for('.list')))