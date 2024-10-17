from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Connect to MongoDB (replace 'mongo' with your MongoDB service name if using Docker Compose)
client = MongoClient("mongodb://mongo:27017/")
db = client["taskdb"]
tasks_collection = db["tasks"]

# CRUD Operations
@app.route('/tasks', methods=['GET'])
def get_tasks():
    tasks = list(tasks_collection.find())
    for task in tasks:
        task['_id'] = str(task['_id'])  # Convert ObjectId to string
    return jsonify(tasks)

@app.route('/tasks', methods=['POST'])
def create_task():
    new_task = request.get_json()
    task_id = tasks_collection.insert_one({
        'title': new_task['title'],
        'description': new_task['description']
    }).inserted_id
    new_task['_id'] = str(task_id)  # Convert ObjectId to string
    return jsonify(new_task), 201

@app.route('/tasks/<string:task_id>', methods=['PUT'])
def update_task(task_id):
    updated_task = request.get_json()
    result = tasks_collection.update_one({'_id': ObjectId(task_id)}, {'$set': updated_task})
    if result.matched_count == 0:
        return jsonify({"error": "Task not found"}), 404
    updated_task['_id'] = task_id
    return jsonify(updated_task)

@app.route('/tasks/<string:task_id>', methods=['DELETE'])
def delete_task(task_id):
    result = tasks_collection.delete_one({'_id': ObjectId(task_id)})
    if result.deleted_count == 0:
        return jsonify({"error": "Task not found"}), 404
    return '', 204

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
