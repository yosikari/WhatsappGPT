import json
from datetime import datetime


# Get empty user props
def getEmptyUser():
    return {
        "gpt": "30",
        "dalle": "3",
        "deepai": "3",
        "notes": {}
    }

# Add new user to data


def add_user(new_user_phone):
    with open('data/users.json', 'r+') as file:
        data = json.load(file)
        if 'users' not in data:
            data['users'] = {}
            data['users'][new_user_phone] = getEmptyUser()
            file.seek(0)
            json.dump(data, file, indent=4)
        else:
            data['users'][new_user_phone] = getEmptyUser()
            file.seek(0)
            json.dump(data, file, indent=4)

# Get user by phone number


def get_user(user_phone):
    with open('data/users.json', 'r') as file:
        data = json.load(file)
        if user_phone in data["users"]:
            return data["users"][user_phone]
        else:
            return None

# Update user counter


def update_user_counter(user_key, counter_key, new_value):
    with open('data/users.json', 'r+') as file:
        data = json.load(file)
        if user_key in data["users"]:
            data["users"][user_key][counter_key] = new_value
            file.seek(0)
            json.dump(data, file, indent=4)
        else:
            print("Update user counter, User not found")
            return None

# Add user note


def add_user_note(user_key, new_value):
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    with open('data/users.json', 'r+') as file:
        data = json.load(file)
        if user_key in data["users"]:
            data["users"][user_key]["notes"][dt_string] = new_value
            file.seek(0)
            json.dump(data, file, indent=4)
        else:
            print("Add user note, User not found")
            return None

# Clear user notes


def clear_user_note(user_key):
    with open('data/users.json', 'r+') as file:
        data = json.load(file)
        if user_key in data["users"]:
            data["users"][user_key]["notes"] = {}
            with open('data/users.json', 'w') as f:
                json.dump(data, f, indent=4)
        else:
            print("Clear user notes, User not found")
            return None

# Get user notes


def get_user_notes(user_phone):
    with open('data/users.json', 'r') as file:
        data = json.load(file)
        if user_phone in data["users"]:
            return data["users"][user_phone]["notes"]
        else:
            return None
