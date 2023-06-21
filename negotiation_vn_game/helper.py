import csv


CSV_PATH = 'ID-Part-1.csv'
EXCEL_PATH = 'ID-Part-2.xlsx'
EN_LANGUAGE = 3


class User:
    def __init__(self, id, language, address, email):
        self.id = id
        self.language = language
        self.address = address
        self.email = email

    def __str__(self) -> str:
        return f'User: {self.id}, {self.language}, {self.address}, {self.email}'

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
                    user = User(id, row[6][0], row[5], "")
    except Exception as e:
        print(e)
    finally:
        return user
    
def get_user_from_excel(id):
    """
    Get user from excel file
    """
    user = None
    try:
        import pandas as pd
        df = pd.read_excel(EXCEL_PATH)
        for index, row in df.iterrows():
            if str(row['RandomID']) == id:
                user = User(id, row['level of English language proficiency'], get_address_vn(row['Coming from']), row['Email'])
                break
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