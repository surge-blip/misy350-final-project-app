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

elif st.session_state["page"] == "register":
    st.header("Register Page")

elif st.session_state["page"] == "owner_dashboard":
    st.header("Owner Dashboard")

elif st.session_state["page"] == "employee_dashboard":
    st.header("Employee Dashboard")

## login page

if st.session_state["page"] == "login":
    st.title("Small Business Inventory Manager")
    st.write("Welcome to the inventory system")
    st.header("Login Page")

    EMAIL = st.text_input("Email")
    PASSWORD = st.text_input("Password")

    if st.button("Login"):
        st.write("Login clicked")

    if st.button("Go to Register"):
        st.session_state["page"] = "register"
        st.rerun()



