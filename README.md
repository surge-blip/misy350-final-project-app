# Inventory Management System

## Project Description

This project is a Streamlit-based Inventory Management System developed for MISY350 Business Application Development.

The application supports role-based functionality for Owners and Employees and includes inventory CRUD operations, JSON persistence, session state management, and an AI assistant integrated using OpenAI.



## Features

### Authentication
- User registration
- User login/logout
- Role-based access control

### Owner Dashboard
- Add inventory products
- Update product quantities
- Delete products
- View employee inventory requests
- Inventory summary dashboard
- AI inventory assistant

### Employee Dashboard
- View inventory
- Submit inventory requests

### Persistence
- Inventory data stored in `inventory.json`
- User data stored in `users.json`
- Employee requests stored in `requests.json`



## Technologies Used

- Python
- Streamlit
- Pandas
- OpenAI API
- dotenv
- JSON



## Project Structure

- `app.py` → UI Layer
- `service.py` → Business Logic Layer
- `data_manager.py` → Data Persistence Layer
- `inventory.json` → Inventory Storage
- `users.json` → User Storage
- `requests.json` → Employee Request Storage



## How to Run


Run the application:

```bash
streamlit run app.py
```



## Test Accounts

### Owner Account
Email: owner@inventory.com  
Password: owner123

### Employee Account
Email: employee@inventory.com  
Password: employee123



## AI Assistant

The Owner dashboard includes an AI-powered assistant integrated using the OpenAI API and Streamlit chat interface.

