from flask import Flask, request, jsonify, render_template
import json

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
    item = {
        "itemName": data.get("itemName"),
        "itemDescription": data.get("itemDescription")
    }

    # Save to file (MongoDB later)
    with open('data.json', 'r+') as f:
        current = json.load(f)
        current.append(item)
        f.seek(0)
        json.dump(current, f)

    return jsonify({"message": "Item added"}), 201

if __name__ == '__main__':
    app.run(debug=True)