from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
import random

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Task model
class Task(db.Model):
    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    content = Column(String(500), nullable=True)
    status = Column(String(20), default='pending')
    created_by = Column(String(100), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'status': self.status,
            'created_by': self.created_by,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

# Create the database
with app.app_context():
    db.create_all()

# Get all tasks with optional filters
@app.route('/tasks', methods=['GET'])
def get_tasks():
    status_filter = request.args.get('status')
    created_by = request.args.get('created_by')

    query = Task.query
    if status_filter:
        query = query.filter_by(status=status_filter)
    if created_by:
        query = query.filter_by(created_by=created_by)

    tasks = query.order_by(Task.created_at.asc()).all()
    return jsonify([task.to_dict() for task in tasks])

# Get a single task by ID
@app.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = Task.query.get(task_id)
    if not task:
        return jsonify({'error': 'Task not found'}), 404
    return jsonify(task.to_dict())

# Create a new task
@app.route('/tasks', methods=['POST'])
def create_task():
    data = request.get_json()
    if not data or not data.get('title') or not data.get('created_by'):
        return jsonify({'error': 'Title and created_by are required'}), 400

    new_task = Task(
        title=data['title'],
        content=data.get('content', ''),
        created_by=data['created_by'],
        status='pending'
    )
    db.session.add(new_task)
    db.session.commit()
    return jsonify(new_task.to_dict()), 201

# Update an existing task
@app.route('/tasks/<int:task_id>', methods=['PATCH'])
def update_task(task_id):
    task = Task.query.get(task_id)
    if not task:
        return jsonify({'error': 'Task not found'}), 404

    data = request.get_json()
    if not data:
        return jsonify({'error': 'Invalid JSON'}), 400

    if 'title' in data:
        task.title = data['title']
    if 'content' in data:
        task.content = data['content']
    if 'status' in data:
        task.status = data['status']

    db.session.commit()
    return jsonify(task.to_dict())

<<<<<<< HEAD
=======

>>>>>>> 09d02b0 (Initial)
if __name__ == '__main__':
    app.run(debug=True)
