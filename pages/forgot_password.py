import streamlit as st
import re
import mysql.connector
import bcrypt

st.set_page_config(
    page_title="Reset Password",
    page_icon="🔏"
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


# function to hash a password
def hash_password(password: str) -> bytes:
    password_bytes = password.encode('utf-8')
    return bcrypt.hashpw(password_bytes, bcrypt.gensalt())


st.markdown('<h1 style="text-align: center;">Reset Password </h1>', unsafe_allow_html=True)
st.write("")

email = st.text_input("Enter your email")
new_password = st.text_input("Enter new password", type="password")
change = st.button("Change password", use_container_width=True)
if change:
    errors = []
    if not email or not new_password:
        errors.append("Error: All fields are required")
    # check email validity
    if not re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email):
        errors.append("Error: Enter a valid email format.")
    if errors:
        st.error(errors[0])
    else:
        try:
            hash_pass = hash_password(new_password)  # hash the password
            sql = "UPDATE users SET password = %s WHERE email = %s"
            values = (hash_pass, email)  # pass parameters as a tuple
            mycursor.execute(sql, values)
            if mycursor.rowcount == 0:
                st.error("Error: Email does not exist")
            else:
                mydb.commit()
                st.switch_page("login.py")
        except Exception as e:
            st.error(e)
