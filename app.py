from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app(test_config=None):
    app = Flask(__name__)
    if test_config:
        app.config.update(test_config)
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    with app.app_context():
        db.create_all()

    from models import Task

    @app.route('/tasks', methods=['GET'])
    def get_tasks():
        tasks = Task.query.all()
        return jsonify([t.to_dict() for t in tasks]), 200

    @app.route('/tasks', methods=['POST'])
    def create_task():
        data = request.get_json()
        if not data or 'title' not in data:
            return jsonify({'error': 'Title is required'}), 400
        task = Task(title=data['title'])
        db.session.add(task)
        db.session.commit()
        return jsonify(task.to_dict()), 201

    @app.route('/tasks/<int:task_id>', methods=['PUT'])
    def update_task(task_id):
        task = db.session.get(Task, task_id)
        if not task:
            return jsonify({'error': 'Not found'}), 404
        data = request.get_json()
        if 'title' in data:
            task.title = data['title']
        if 'done' in data:
            task.done = data['done']
        db.session.commit()
        return jsonify(task.to_dict()), 200

    @app.route('/tasks/<int:task_id>', methods=['DELETE'])
    def delete_task(task_id):
        task = db.session.get(Task, task_id)
        if not task:
            return jsonify({'error': 'Not found'}), 404
        db.session.delete(task)
        db.session.commit()
        return jsonify({'message': 'Task deleted'}), 200

    return app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)