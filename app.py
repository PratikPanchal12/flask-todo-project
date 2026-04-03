from flask import Flask, request, jsonify, render_template
import json

from pymongo import MongoClient

# MongoDB connection
client = MongoClient('mongodb://localhost:27017/')
db = client['todo_db']
collection = db['todo_collection']

app = Flask(__name__)

# Home route
@app.route('/')
def home():
    return render_template('index.html')

# API route
@app.route('/api', methods=['GET'])
def get_data():
    with open('data.json', 'r') as f:
        data = json.load(f)
    return jsonify(data)

# Backend route (used later)
@app.route('/submittodoitem', methods=['POST'])
def submit_todo():
    data = request.json
    collection.insert_one(data)
    return {"message": "Saved to MongoDB"}

if __name__ == '__main__':
    app.run(debug=True)