from typing import List, Dict, Optional


class InventoryManager:
    def __init__(self, inventory: List[Dict], users: List[Dict]) -> None:
        self.inventory = inventory
        self.users = users


    def all(self):
        return list(self.inventory)

    def add(self, name: str, quantity: int):
        if not name.strip():
            raise ValueError("Product name is required")

        
        for item in self.inventory:
            if item["name"].lower() == name.lower():
                raise ValueError("Product already exists")

        product = {
            "name": name,
            "quantity": quantity
        }

        self.inventory.append(product)
        return product

    def find(self, name: str) -> Optional[Dict]:
        for item in self.inventory:
            if item["name"].lower() == name.lower():
                return item
        return None
    

    def update(self, name: str, quantity: int):
        item = self.find(name)

        if not item:
            raise ValueError("Product not found")

        item["quantity"] = quantity
        return item

    def delete(self, name: str):
        item = self.find(name)

        if not item:
            raise ValueError("Product not found")

        self.inventory.remove(item)

    def login(self, email: str, password: str):
        for user in self.users:
            if user["email"] == email and user["password"] == password:
                return user
        return None
    
    def register(self, name: str, email: str, password: str, role: str):
        if not name.strip():
            raise ValueError("Name is required")

        for user in self.users:
            if user["email"] == email:
                raise ValueError("User already exists")

        new_user = {
            "name": name,
            "email": email,
            "password": password,
            "role": role
        }

        self.users.append(new_user)
        return new_user