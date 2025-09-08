from flask import Flask, jsonify, request, render_template, redirect, url_for
from pymongo import MongoClient
import json

app = Flask(__name__)

# MongoDB Atlas connection
client = MongoClient("mongodb+srv://dummy:1234@cluster0.foqdb25.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client.test
collection = db["flask-tutorial"]

@app.route('/submittodoitem', methods=['POST'])
def submit_todo_item():
    itemName = request.form['itemName']
    itemDescription = request.form['itemDescription']
    db.todo_items.insert_one({"itemName": itemName, "itemDescription": itemDescription})
    return "To-Do item submitted successfully"



# -------- Route 1: Read JSON file and return list ----------
@app.route('/api')
def get_data():
    try:
        with open("data.json", "r") as file:
            data = json.load(file)
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# -------- Route 2: Render form ----------
@app.route('/')
def index():
    return render_template("form.html")

# -------- Route 3: Handle form submission ----------
@app.route('/submit', methods=['POST'])
def submit():
    try:
        name = request.form['name']
        email = request.form['email']

        # Insert into MongoDB Atlas
        collection.insert_one({"name": name, "email": email})

        # Redirect to success page
        return redirect(url_for('success'))

    except Exception as e:
        # Render same page with error
        return render_template("form.html", error=str(e))

# -------- Route 4: Success page ----------
@app.route('/success')
def success():
    return "Data submitted successfully"

if __name__ == '__main__':
    app.run(debug=True)
