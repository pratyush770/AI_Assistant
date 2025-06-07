import streamlit as st
import mysql.connector
import re

st.set_page_config(
    page_title="Register User",
    page_icon="📝"
)

host_name = st.secrets["HOST"]
user_name = st.secrets["USER"]
pwd = st.secrets["PASSWORD"]
db = st.secrets["DATABASE"]

mydb = mysql.connector.connect(
    host=host_name,
    user=user_name,
    password=pwd,
    port=3306,
    database=db
)

mycursor = mydb.cursor()

st.markdown('<h1 style="text-align: center;">Create Account</h1>', unsafe_allow_html=True)
st.write("")
email = st.text_input("Enter your email")
password = st.text_input("Enter your password", type="password").strip()
confirm_pwd = st.text_input("Confirm password", type="password").strip()
register = st.button("Sign Up", use_container_width=True)
if register:
    errors = []
    if not email or not password or not confirm_pwd:
        errors.append("Error: All fields are required")
    # check email validity
    if not re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email):
        errors.append("Error: Enter a valid email format.")
    # check password length
    if len(password) < 8:
        errors.append("Error: Password must be of at least 8 characters")
    # check if passwords match
    if password != confirm_pwd:
        errors.append("Error: Passwords do not match")
    if errors:
        st.error(errors[0])
    else:
        try:
            sql = "INSERT INTO users VALUES (%s,%s)"
            values = (email, password)  # Pass parameters as a tuple
            mycursor.execute(sql, values)
            mydb.commit()
            st.switch_page("login.py")
        except mysql.connector.IntegrityError:
            st.error("Error: This email is already registered")
        except Exception as e:
            st.error(e)

login = st.button("Already have an account? Login", type="tertiary", use_container_width=True)
if login:
    st.switch_page("login.py")
