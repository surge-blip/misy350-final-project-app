import streamlit as st

# Session Setup

if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if "user" not in st.session_state:
    st.session_state["user"] = None

if "role" not in st.session_state:
    st.session_state["role"] = None

if "page" not in st.session_state:
    st.session_state["page"] = "login"


# page routing

if st.session_state["page"] == "login":

    st.title("Small Business Inventory Manager")
    st.write("Welcome to the inventory system")
    st.header("Login Page")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        st.write("Login clicked")

    if st.button("Go to Register"):
        st.session_state["page"] = "register"
        st.rerun()


elif st.session_state["page"] == "register":

    st.title("Register Account")
    st.write("Create a new account")

    name = st.text_input("Full Name")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    role = st.selectbox("Role", ["Owner", "Employee"])

    if st.button("Register"):
        st.write("Account created")

    if st.button("Go to Login"):
        st.session_state["page"] = "login"
        st.rerun()


elif st.session_state["page"] == "owner_dashboard":
    st.header("Owner Dashboard")

elif st.session_state["page"] == "employee_dashboard":
    st.header("Employee Dashboard")







