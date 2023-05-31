import csv


CSV_PATH = 'ID-Part-1.csv'
EN_LANGUAGE = 3


class User:
    def __init__(self, id, language, address):
        self.id = id
        self.language = language
        self.address = address

    def __str__(self) -> str:
        return f'User: {self.id}, {self.language}, {self.address}'

def get_user_from_db(id):
    """
    Get user from csv file
    """
    user = None
    try:
        with open(CSV_PATH, 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                if row[8] == id:
                    user = User(id, row[6][0], get_address_vn(row[5]))
    except Exception as e:
        print(e)
    finally:
        return user

def get_address_vn(address):
    if address == "Middle Vietnam":
        return "Miền Trung Việt Nam"
    elif address == "North Vietnam":
        return "Miền Bắc Việt Nam"
    elif address == "South Vietnam":
        return "Miền Nam Việt Nam"
    return address