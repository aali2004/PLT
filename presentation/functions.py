import json
from datetime import datetime

#Class Functions:
def __init__(self, license, brand, model, color):
        self.license = license
        self.brand = brand
        self.model = model
        self.color = color
        self.entry_time = datetime.now().isoformat()

def to_dict(self):
        return {
            "license": self.license,
            "brand": self.brand,
            "model": self.model,
            "color": self.color,
            "entry_time": self.entry_time
        }

def load_parking():
    with open("parking.txt", "r") as file:
        return json.load(file)

def save_parking(data):

    with open("parking.txt", "w") as file:
        json.dump(data, file, indent=4)



def enter(license, brand, model, color, is_vip):
 
    lots = load_parking()
    

    for lot in lots:
        if lots[lot]["car"] and lots[lot]["car"].get("license") == license:
            return "Error: Already parked"

    
    for lot in lots:
        if lots[lot]["status"] == "free" and lots[lot]["vip"] == is_vip:
            lots[lot]["status"] = "occupied"
            lots[lot]["car"] = {
                "license": license,
                "brand": brand,
                "model": model,
                "color": color,
                "entry_time": datetime.now().isoformat()
            }
            save_parking(lots)
            return "Success: Car parked"
    return "Error: No space available"


def remove_car(license_plate):    
    lots = load_parking()
    for lot in lots:
        if lots[lot]["car"] and lots[lot]["car"].get("license") == license_plate:
            lots[lot]["status"] = "free"
            lots[lot]["car"] = None
            save_parking(lots)
            return "Success: Car removed"
    return "Error: Not found"

def calculate_fee(license_plate):
    lots = load_parking()
    for lot in lots:
        if lots[lot]["car"] and lots[lot]["car"].get("license") == license_plate:
            entry_time = datetime.fromisoformat(lots[lot]["car"]["entry_time"])
            duration = datetime.now() - entry_time
            hours = duration.total_seconds() / 3600
            rate = 10 if lots[lot]["vip"] else 5
            return round(hours * rate, 2)
    return "Error: Car not found"

def clear_all_lots():
    lots = load_parking()
    for lot in lots:
        lots[lot]["status"] = "free"
        lots[lot]["car"] = None
    save_parking(lots)
    return "All lots cleared"