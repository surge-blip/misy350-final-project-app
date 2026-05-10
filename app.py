import streamlit as st
import json
from pathlib import Path
import pandas as pd
import data_manager
import service
import time
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=api_key)



def get_ai_response(client, messages):

    ai_response = client.chat.completions.create(
        model="gpt-5-mini",
        messages=messages,
        temperature=1
    )

    return ai_response.choices[0].message.content

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

if "requests" not in st.session_state:
    st.session_state["requests"] = []

if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {
            "role": "assistant",
            "content": "Hi, how can I help you?"
        }
    ]

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

with st.sidebar:

    st.title("Inventory Manager")

    if st.session_state["logged_in"]:

        st.write(f"Logged in as: {st.session_state['user']['name']}")

        st.divider()

        if st.session_state["role"] == "Owner":

            if st.button(
                "Owner Dashboard",
                key="owner_dashboard_btn",
                use_container_width=True
            ):

                st.session_state["page"] = "owner_dashboard"
                st.rerun()
            
        elif st.session_state["role"] == "Employee":

            if st.button(
                "Employee Dashboard",
                key="employee_dashboard_btn",
                use_container_width=True
            ):

                st.session_state["page"] = "employee_dashboard"
                st.rerun()
        
        st.divider()

        if st.button(
            "Logout",
            key="sidebar_logout_btn",
            use_container_width=True
        ):

            st.session_state["logged_in"] = False
            st.session_state["user"] = None
            st.session_state["role"] = None
            st.session_state["page"] = "login"

            st.rerun()

# page routing

# login page


if st.session_state["page"] == "login":


    with st.container(border=True):

        st.subheader("Test Accounts")

        st.markdown("Owner Account")

        with st.container(border=True):
                    st.text(
                        "Email: owner@inventory.com\nPassword: owner123"
                    )

        st.markdown("Employee Account")

        with st.container(border=True):
                    st.text(
                        "Email: employee@inventory.com\nPassword: employee123"
                    )



    st.title("Inventory Manager")
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

    with st.container(border=True):

        col1, col2 = st.columns([3,1])

        with col1:
            st.subheader(
                f"Welcome, {st.session_state['user']['name']}"
            )

        with col2:
            st.write("Role")
            st.write(st.session_state["role"])

    st.write("Manage your products here")

    st.divider()

    col1, col2 = st.columns([3,1])

    with col1:

        st.subheader("Inventory Table")

        with st.container(border=True):

            if len(st.session_state["inventory"]) > 0:

                df = pd.DataFrame(
                    st.session_state["inventory"]
                )

                st.dataframe(df)

            else:
                st.info("No products available")

    with col2:

        st.subheader("Inventory Summary")

        with st.container(border=True):

            st.write(
                "Total Products:",
                len(st.session_state["inventory"])
            )
    
    tab1, tab2 = st.tabs([
    "Add Product",
    "Manage Products"
    ])

    with tab1:

        col1, col2 = st.columns(2)

        with col1:
            product_name = st.text_input("Product Name")

        with col2:
            product_quantity = st.number_input(
                "Quantity",
                min_value=0
            )

        if st.button(
            "Add Product",
            key="add_product_btn"
        ):  

            with st.spinner("Adding product..."):

                time.sleep(3)

                manager.add(product_name, product_quantity)

                data_manager.save_inventory(
                    st.session_state["inventory"],
                    json_path_inventory
                )

            st.write("Product added")
    
    with tab2:

        st.subheader("Update or Delete Product")

        for item in st.session_state["inventory"]:

            new_quantity = st.number_input(
                f"Update quantity for {item['name']}",
                min_value=0, value=item["quantity"]
                )

            if st.button(
                f"Update {item['name']}",
                key=f"update_{item['name']}"
            ):
                manager.update(item["name"], new_quantity)

                with json_path_inventory.open("w") as f:
                    json.dump(st.session_state["inventory"], f, indent=4)

                st.write("Product updated")
                st.rerun()

            if st.button(
                f"Delete {item['name']}",
                key=f"delete_{item['name']}"
            ):
                manager.delete(item["name"])

                with json_path_inventory.open("w") as f:
                    json.dump(st.session_state["inventory"], f, indent=4)

                st.write("Product deleted")
                st.rerun()
            
    st.divider()

    st.subheader("Employee Requests")

    if len(st.session_state["requests"]) > 0:

        requests_df = pd.DataFrame(
            st.session_state["requests"]
        )

        st.dataframe(requests_df)

        if st.button(
            "Clear Requests",
            key="clear_requests_btn"
        ):

            st.session_state["requests"] = []

            st.rerun()

    else:
        st.info("No inventory requests submitted")

    st.divider()

    st.subheader("Inventory AI Assistant")

    with st.container(border=True, height=300):

        for message in st.session_state["messages"]:

            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    user_input = st.chat_input(
        "Ask inventory assistant..."
        )

    if user_input:

        st.session_state["messages"].append(
                {
                    "role": "user",
                    "content": user_input
                }
            )

        ai_response = get_ai_response(
            client,
            st.session_state["messages"]
        )

        st.session_state["messages"].append(
            {
                "role": "assistant",
                "content": ai_response
            }
        )

        st.rerun()

        

elif st.session_state["page"] == "employee_dashboard":

    st.title("Employee Dashboard")

    with st.container(border=True):

        col1, col2 = st.columns([3,1])

        with col1:
            st.subheader(
                f"Welcome, {st.session_state['user']['name']}"
            )

        with col2:
            st.write("Role")
            st.write(st.session_state["role"])

    st.subheader("Inventory Overview")
    st.write("View available products")

    st.divider()

    col1, col2 = st.columns([3,1])

    with col1:

        st.subheader("Inventory Table")

        with st.container(border=True):

            if len(st.session_state["inventory"]) > 0:
                df = pd.DataFrame(st.session_state["inventory"])
                st.dataframe(df)
            else:
                st.info("No products available")

    with col2:

        with st.container(border=True):

            st.subheader("Inventory Summary")

            st.write(
                "Total Products:",
                len(st.session_state["inventory"])
            )
    st.divider()

    st.subheader("Request Inventory")

    request_item = st.text_input(
        "Requested Product"
    )

    request_quantity = st.number_input(
        "Requested Quantity",
        min_value=1
    )

    if st.button(
        "Submit Request",
        key="submit_request_btn"
    ):

        st.session_state["requests"].append(
            {
        "item": request_item,
        "quantity": request_quantity,
        "employee": st.session_state["user"]["name"]
            }
        )

        st.write("Request submitted")



        


   







