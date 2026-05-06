import streamlit as st
import json
from pathlib import Path
import pandas as pd
import data_manager
import service


# data layer

def load_inventory(json_path):
    if json_path.exists():
        with open(json_path, "r") as f:
            return json.load(f)
    return []

def save_inventory(inventory, json_path):
    with open(json_path, "w") as f:
        json.dump(inventory, f, indent=4)

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

st.session_state["inventory"] = data_manager.load_inventory(json_path_inventory)

json_path_users = Path("users.json")

if json_path_users.exists():
    with json_path_users.open("r") as f:
        st.session_state["users"] = json.load(f)
else:
    st.session_state["users"] = []

manager = service.InventoryManager(
    st.session_state["inventory"],
    st.session_state["users"]
)

# page routing

# login page
if st.session_state["page"] == "login":

    st.title("Small Business Inventory Manager")
    st.write("Welcome to the inventory system")
    st.header("Login Page")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
                
        user = manager.login(email, password)

        if user:
            
            st.session_state["logged_in"] = True
            st.session_state["user"] = user
            st.session_state["role"] = user["role"]

            if user["role"] == "Owner":
                st.session_state["page"] = "owner_dashboard"

            else:
                st.session_state["page"] = "employee_dashboard"

            st.rerun()

        else:
            st.error("Invalid email or password")

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

        manager.register(name, email, password, role)

        with json_path_users.open("w") as f:
            json.dump(st.session_state["users"], f, indent=4)

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

    st.divider()

    st.subheader("Inventory Table")

    if len(st.session_state["inventory"]) > 0:
        df = pd.DataFrame(st.session_state["inventory"])
        st.dataframe(df)
    else:
        st.info("No products available")
    

    product_name = st.text_input("Product Name")
    product_quantity = st.number_input("Quantity", min_value=0)

    if st.button("Add Product"):

        manager.add(product_name, product_quantity)

        save_inventory(st.session_state["inventory"], json_path_inventory)

        st.write("Product added")
    
    st.divider()

    st.subheader("Update or Delete Product")

    for item in st.session_state["inventory"]:

        new_quantity = st.number_input(
            f"Update quantity for {item['name']}",
            min_value=0, value=item["quantity"]
            )

        if st.button(f"Update {item['name']}"):
            item["quantity"] = new_quantity

            with json_path_inventory.open("w") as f:
                json.dump(st.session_state["inventory"], f, indent=4)

            st.write("Product updated")
            st.rerun()

        if st.button(f"Delete {item['name']}"):
            st.session_state["inventory"].remove(item)

            with json_path_inventory.open("w") as f:
                json.dump(st.session_state["inventory"], f, indent=4)

            st.write("Product deleted")
            st.rerun()


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

    st.divider()

    st.subheader("Inventory Table")

    if len(st.session_state["inventory"]) > 0:
        df = pd.DataFrame(st.session_state["inventory"])
        st.dataframe(df)
    else:
        st.info("No products available")

    if st.button("Logout"):
        st.session_state["logged_in"] = False
        st.session_state["user"] = None
        st.session_state["role"] = None
        st.session_state["page"] = "login"
        st.rerun()

   







