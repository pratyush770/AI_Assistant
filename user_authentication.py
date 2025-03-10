import pyrebase
import streamlit as st
from secret_key import firebaseConfig
import time

st.set_page_config(page_title="AI Assistant", page_icon='🤖')

# initialize Firebase
firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()
db = firebase.database()

st.title("Login/Signup")  # page title

# initialize session state variables
if "user" not in st.session_state:
    st.session_state.user = None
if "login_success" not in st.session_state:
    st.session_state.login_success = False  # ensure it starts as false


def save_user_session(email, user_id, refresh_token):
    st.session_state.user = {"email": email, "user_id": user_id, "refresh_token": refresh_token}
    st.session_state.login_success = True  # set login success flag
    db.child("sessions").child(user_id).set({
        "email": email,
        "refresh_token": refresh_token,
        "last_refreshed": int(time.time())  # track when the token was last refreshed
    })


def load_user_session():
    if "user" in st.session_state and st.session_state.user:
        return  # session already loaded

    # try to retrieve the user ID from local storage (or another persistent mechanism)
    sessions = db.child("sessions").get().val()
    if sessions:
        for uid, session_data in sessions.items():
            refresh_token = session_data.get("refresh_token")
            if refresh_token:
                try:
                    user = auth.refresh(refresh_token)  # use the refresh token to get a new ID token
                    email = session_data.get("email")

                    # restore session state
                    st.session_state.user = {"email": email, "user_id": uid, "refresh_token": refresh_token}
                    st.session_state.login_success = True

                    # update the session in Firebase with the new ID token
                    db.child("sessions").child(uid).update({
                        "refresh_token": user['refreshToken'],
                        "last_refreshed": int(time.time())
                    })
                    break
                except Exception as e:
                    # handle invalid or expired refresh token
                    db.child("sessions").child(uid).remove()  # Remove invalid session


def refresh_token_if_needed():
    if "user" in st.session_state and st.session_state.user:
        user = st.session_state.user
        user_id = user["user_id"]
        refresh_token = user.get("refresh_token")

        session_data = db.child("sessions").child(user_id).get().val()
        last_refreshed = session_data.get("last_refreshed", 0)

        # check if 1 hour (3600 seconds) has passed since the last refresh
        current_time = int(time.time())
        if current_time - last_refreshed > 3600:  # 1 hour = 3600 seconds
            try:
                # use the refresh token to get a new ID token
                refreshed_user = auth.refresh(refresh_token)
                new_refresh_token = refreshed_user['refreshToken']

                # update session state and firebase
                st.session_state.user["refresh_token"] = new_refresh_token
                db.child("sessions").child(user_id).update({
                    "refresh_token": new_refresh_token,
                    "last_refreshed": int(time.time())
                })
                st.success("Token refreshed successfully!")
            except Exception as e:
                st.warning("Failed to refresh token. Please log in again.")

load_user_session()  # load session at the start

# redirect only if login just happened or session is already active
if st.session_state.login_success:
    refresh_token_if_needed()  # refresh token if needed
    st.switch_page("pages/home.py")  # redirect to home page after successful login

# authentication ui
choice = st.selectbox("Select an option", ["Login", "Signup"])
email = st.text_input("Enter your email")
password = st.text_input("Please enter your password", type='password')

# signup
if choice == "Signup":
    confirm_password = st.text_input("Please re-enter your password", type='password')
    submit = st.button("Create account")

    if submit:
        if email and password:
            if password == confirm_password:
                try:
                    user = auth.create_user_with_email_and_password(email, password)
                    st.success("Account created successfully! Please log in.")  # ✅ No auto-login

                    # Store user data in Firebase
                    user_id = user['localId']
                    db.child("users").child(user_id).set({"email": email})

                except Exception as e:
                    error_message = str(e)
                    if "EMAIL_EXISTS" in error_message:
                        st.error("Account already exists. Please log in.")
                    else:
                        st.error(f"Error: {error_message}")
            else:
                st.warning("Passwords do not match!")
        else:
            st.warning("Please fill all fields.")

# login
if choice == "Login":
    login = st.button("Login")

    if login:
        if email and password:
            try:
                user = auth.sign_in_with_email_and_password(email, password)
                st.success("Logged in successfully!")

                user_id = user['localId']
                refresh_token = user['refreshToken']  # get the refresh token

                # save session securely
                save_user_session(email, user_id, refresh_token)

                # redirect to home page after successful login
                st.switch_page("pages/home.py")
            except Exception as e:
                st.warning("Invalid login details. Please try again.")
        else:
            st.warning("Please fill all fields.")
