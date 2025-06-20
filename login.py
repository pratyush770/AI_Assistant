import streamlit as st
import re
import mysql.connector
import bcrypt

st.set_page_config(
    page_title="Login User",
    page_icon="👤"
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


# function to verify a password
def verify_password(provided_password: str, stored_hash: str) -> bool:
    provided_password_bytes = provided_password.encode('utf-8')
    stored_hash_bytes = stored_hash.encode('utf-8')  # convert stored hash to bytes
    return bcrypt.checkpw(provided_password_bytes, stored_hash_bytes)


st.markdown('<h1 style="text-align: center;">Welcome Back!</h1>', unsafe_allow_html=True)
st.write("")

email = st.text_input("Enter your email")
password = st.text_input("Enter your password", type="password")
forgot_pass = st.button("Forgot password?", type="tertiary")
if forgot_pass:
    st.switch_page("pages/forgot_password.py")

login = st.button("Sign in", use_container_width=True)
if login:
    errors = []
    if not email or not password:
        errors.append("Error: All fields are required")
    # check email validity
    if not re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email):
        errors.append("Error: Enter a valid email format.")
    try:
        sql = "SELECT email, password FROM users WHERE email = %s"
        values = (email,)  # pass parameters as a tuple
        mycursor.execute(sql, values)
        result = mycursor.fetchone()
        if result is not None:
            db_email = result[0]
            db_pass = result[1]
            if verify_password(password, db_pass):
                st.switch_page("pages/home.py")
            else:
                errors.append("Error: Enter valid password")
        else:
            errors.append("Error: Email does not exist")
        if errors:
            st.error(errors[0])
    except Exception as e:
        st.error(e)

register = st.button("Don't have an account? Register", type="tertiary", use_container_width=True)
if register:
    st.switch_page("pages/register.py")
