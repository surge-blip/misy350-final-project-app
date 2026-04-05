import streamlit as st
import json
from pathlib import Path
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

json_path_inventory = Path("inventory.json")

if json_path_inventory.exists():
    with json_path_inventory.open("r") as f:
        st.session_state["inventory"] = json.load(f)
else:
    st.session_state["inventory"] = []

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

    st.divider()

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

    st.divider()


elif st.session_state["page"] == "owner_dashboard":

    st.title("Owner Dashboard")
    st.write("Welcome,", st.session_state["user"]["name"])
    st.write("Role:", st.session_state["role"])

    st.subheader("Inventory Section")
    st.write("Manage your products here")

    product_name = st.text_input("Product Name")
    product_quantity = st.number_input("Quantity", min_value=0)

    if st.button("Add Product"):

        product = {
            "name": product_name,
            "quantity": product_quantity
        }

        st.session_state["inventory"].append(product)

        with json_path_inventory.open("w") as f:
            json.dump(st.session_state["inventory"], f, indent=4)

        st.write("Product added")



    if st.button("Logout"):
        st.session_state["logged_in"] = False
        st.session_state["user"] = None
        st.session_state["role"] = None
        st.session_state["page"] = "login"
        st.rerun()

        

elif st.session_state["page"] == "employee_dashboard":

    st.title("Employee Dashboard")
    st.write("Welcome,", st.session_state["user"]["name"])
    st.write("Role:", st.session_state["role"])

    st.subheader("Inventory Overview")
    st.write("View available products")

    if st.button("Logout"):
        st.session_state["logged_in"] = False
        st.session_state["user"] = None
        st.session_state["role"] = None
        st.session_state["page"] = "login"
        st.rerun()

   







