from flask import Flask, render_template, request, redirect, url_for
import json
from datetime import datetime

app = Flask(__name__)

class Vehicle:
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
        data = json.load(file)
    return data

def save_parking(data):
    with open("parking.txt", "w") as file:
        json.dump(data, file, indent=4)

@app.route('/')
def index():
    message = request.args.get('message')
    error = request.args.get('error')
    return render_template('index.html', message=message, error=error)

@app.route('/enter', methods=['GET', 'POST'])
def enter():
    if request.method == 'POST':
        new_car = Vehicle(
            request.form['license'],
            request.form['brand'],
            request.form['model'],
            request.form['color']
        )
        car_data = new_car.to_dict()
        
        vip = request.form.get('vip') == 'yes'
        empty_lots = load_parking()
        

        for lot in empty_lots:
            if empty_lots[lot]["car"] and empty_lots[lot]["car"].get("license") == car_data["license"]:
                return redirect(url_for('enter', error='Car with this license plate is already parked'))
        
        for lot in empty_lots:
            if empty_lots[lot]["status"] == "free" and empty_lots[lot]["vip"] == vip:
                empty_lots[lot]["status"] = "occupied"
                empty_lots[lot]["car"] = car_data
                save_parking(empty_lots)
                return redirect(url_for('index', message='Car parked successfully'))
        return redirect(url_for('enter', error='No parking space available'))
    error = request.args.get('error')
    return render_template('enter.html', error=error)

@app.route('/remove', methods=['GET', 'POST'])
def remove():
    if request.method == 'POST':
        license_to_remove = request.form['license']
        empty_lots = load_parking()
        for lot in empty_lots:
            if empty_lots[lot]["car"] and empty_lots[lot]["car"].get("license") == license_to_remove:
                empty_lots[lot]["status"] = "free"
                empty_lots[lot]["car"] = None
                save_parking(empty_lots)
                return redirect(url_for('index', message='Car removed successfully'))
        return redirect(url_for('remove', error='Car not found'))
    error = request.args.get('error')
    return render_template('remove.html', error=error)

@app.route('/view')
def view():
    empty_lots = load_parking()
    return render_template('view.html', lots=empty_lots)

@app.route('/clear')
def clear():
    empty_lots = load_parking()
    for lot in empty_lots:
        empty_lots[lot]["status"] = "free"
        empty_lots[lot]["car"] = None
    save_parking(empty_lots)
    return redirect(url_for('index', message='All lots cleared'))

@app.route('/calculator', methods=['GET', 'POST'])
def calculator():
    if request.method == 'POST':
        license = request.form['license']
        empty_lots = load_parking()
        for lot in empty_lots:
            if empty_lots[lot]["car"] and empty_lots[lot]["car"].get("license") == license:
                entry_time_str = empty_lots[lot]["car"]["entry_time"]
                entry_time = datetime.fromisoformat(entry_time_str)
                now = datetime.now()
                duration = now - entry_time
                hours = duration.total_seconds() / 3600
                billable_hours = max(0, hours)
                rate = 10 if empty_lots[lot]["vip"] else 5
                fee = billable_hours * rate
                return render_template('calculator.html', license=license, hours=round(hours, 2), billable_hours=round(billable_hours, 2), fee=round(fee, 2), rate=rate)
        return render_template('calculator.html', error='Car not found')
    return render_template('calculator.html')

if __name__ == '__main__':
    app.run(debug=True)
        
    
    