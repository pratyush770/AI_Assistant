import streamlit as st
import pyrebase
# from secret_key import (
#     FIREBASE_API_KEY, AUTH_DOMAIN, PROJECT_ID, DATABASE_URL, STORAGE_BUCKET,
#     MESSAGING_SENDER_ID, APP_ID, MEASUREMENT_ID
# )

st.set_page_config(
    page_title="Login User",
    page_icon="👤"
)

# load credentials
firebase_api_key = st.secrets["FIREBASE_API_KEY"]
auth_domain = st.secrets["AUTH_DOMAIN"]
project_id = st.secrets["PROJECT_ID"]
database_url = st.secrets["DATABASE_URL"]
storage_bucket = st.secret["STORAGE_BUCKET"]
messaging_sender_id = st.secrets["MESSAGING_SENDER_ID"]
app_id = st.secrets["APP_ID"]
measurement_id = st.secrets["MEASUREMENT_ID"]

# firebase configuration
firebaseConfig = {
    "apiKey": firebase_api_key,
    "authDomain": auth_domain,
    "projectId": project_id,
    "databaseURL": database_url,
    "storageBucket": storage_bucket,
    "messagingSenderId": messaging_sender_id,
    "appId": app_id,
    "measurementId": measurement_id
}

# initialize firebase app and authentication
firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()

# initialize database
db = firebase.database()

st.markdown('<h1 style="text-align: center;">Welcome Back!</h1>', unsafe_allow_html=True)
st.write("")

email = st.text_input("Enter your email")
password = st.text_input("Enter your password", type="password").strip()
login = st.button("Sign in", use_container_width=True)
if login:
    try:
        # sign in with email and password
        user = auth.sign_in_with_email_and_password(email, password)
        # refresh token
        refreshed_user = auth.refresh(user['refreshToken'])
        id_token = refreshed_user['idToken']
        local_id = refreshed_user['userId']
        # store user information in the session state
        st.session_state['user'] = {
            'id': local_id,
            'email': email,
            'id_token': id_token
        }
        st.switch_page("pages/app.py")
    except Exception as e:
        # Extract the error message from the exception
        try:
            error_json = e.args[1]  # The second argument contains the JSON response
            error_message = eval(error_json)["error"]["message"]  # Extract the "message" field
            error_message = error_message.title()
            st.error(f"Error: {error_message}")
        except:
            st.error("An unexpected error occurred. Please try again.")

register = st.button("Don't have an account? Register", type="tertiary", use_container_width=True)
if register:
    st.switch_page("pages/register.py")
