import streamlit as st
import pyrebase
# from secret_key import (
#     FIREBASE_API_KEY, AUTH_DOMAIN, PROJECT_ID, DATABASE_URL, STORAGE_BUCKET,
#     MESSAGING_SENDER_ID, APP_ID, MEASUREMENT_ID
# )

st.set_page_config(
    page_title="Register User",
    page_icon="📝"
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

# authentication
firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()

# initialize database
db = firebase.database()

st.markdown('<h1 style="text-align: center;">Create Account</h1>', unsafe_allow_html=True)
st.write("")
email = st.text_input("Enter your email")
password = st.text_input("Enter your password", type="password").strip()
confirm_pwd = st.text_input("Confirm password", type="password").strip()
passwords_match = False
register = st.button("Sign Up", use_container_width=True)
if register:
    # check if passwords match
    if password == confirm_pwd and password:
        passwords_match = True
    else:
        st.error("Error: Passwords do not match")

    if passwords_match:
        try:
            # create user
            user = auth.create_user_with_email_and_password(email, password)
            # sign in
            user = auth.sign_in_with_email_and_password(email, password)
            refreshed_user = auth.refresh(user['refreshToken'])  # now we have a fresh token
            id_token = refreshed_user['idToken']
            local_id = refreshed_user['userId']
            db.child(local_id).child("id").set(local_id, id_token)
            db.child(local_id).child("email").set(email, id_token)
            st.switch_page("login.py")
        except Exception as e:
            # Extract the error message from the exception
            try:
                error_json = e.args[1]  # The second argument contains the JSON response
                error_message = eval(error_json)["error"]["message"]  # Extract the "message" field
                error_message = error_message.title()
                st.error(f"Error: {error_message}")
            except:
                st.error("An unexpected error occurred. Please try again.")

login = st.button("Already have an account? Login", type="tertiary", use_container_width=True)
if login:
    st.switch_page("login.py")
