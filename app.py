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

if "users" not in st.session_state:
    st.session_state["users"] = []

# page routing

# login page
if st.session_state["page"] == "login":

    st.title("Small Business Inventory Manager")
    st.write("Welcome to the inventory system")
    st.header("Login Page")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):

        for user in st.session_state["users"]:
            if user["email"] == email and user["password"] == password:

                st.session_state["logged_in"] = True
                st.session_state["user"] = user
                st.session_state["role"] = user["role"]

                if user["role"] == "Owner":
                    st.session_state["page"] = "owner_dashboard"
                else:
                    st.session_state["page"] = "employee_dashboard"

                st.rerun()

    if st.button("Go to Register"):
        st.session_state["page"] = "register"
        st.rerun()

# Register Page 
elif st.session_state["page"] == "register":

    st.title("Register Account")
    st.write("Create a new account")

    name = st.text_input("Full Name")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    role = st.selectbox("Role", ["Owner", "Employee"])

    if st.button("Register"):

        new_user = {
            "name": name,
            "email": email,
            "password": password,
            "role": role
    }

        st.session_state["users"].append(new_user)
        st.write("Account created successfully")

    if st.button("Go to Login"):
        st.session_state["page"] = "login"
        st.rerun()


elif st.session_state["page"] == "owner_dashboard":

    st.title("Owner Dashboard")
    st.write("Welcome,", st.session_state["user"]["name"])
    st.write("Role:", st.session_state["role"])

elif st.session_state["page"] == "employee_dashboard":

    st.title("Employee Dashboard")
    st.write("Welcome,", st.session_state["user"]["name"])
    st.write("Role:", st.session_state["role"])







