import streamlit as st
st.title("Small Business Inventory Manager")

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

# page routing
if st.session_state["page"] == "login":
    st.header("Login Page")

elif st.session_state["page"] == "register":
    st.header("Register Page")

elif st.session_state["page"] == "owner_dashboard":
    st.header("Owner Dashboard")

elif st.session_state["page"] == "employee_dashboard":
    st.header("Employee Dashboard")