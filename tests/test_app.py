import pytest
from app import create_app, db

@pytest.fixture
def client():
    app = create_app({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
    })
    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.drop_all()

def test_get_tasks_empty(client):
    res = client.get('/tasks')
    assert res.status_code == 200
    assert res.json == []

def test_create_task(client):
    res = client.post('/tasks', json={'title': 'Buy groceries'})
    assert res.status_code == 201
    assert res.json['title'] == 'Buy groceries'
    assert res.json['done'] == False

def test_create_task_no_title(client):
    res = client.post('/tasks', json={})
    assert res.status_code == 400

def test_get_all_tasks(client):
    client.post('/tasks', json={'title': 'Task 1'})
    client.post('/tasks', json={'title': 'Task 2'})
    res = client.get('/tasks')
    assert res.status_code == 200
    assert len(res.json) == 2

def test_update_task_title(client):
    client.post('/tasks', json={'title': 'Old title'})
    res = client.put('/tasks/1', json={'title': 'New title'})
    assert res.status_code == 200
    assert res.json['title'] == 'New title'

def test_update_task_done(client):
    client.post('/tasks', json={'title': 'Study'})
    res = client.put('/tasks/1', json={'done': True})
    assert res.status_code == 200
    assert res.json['done'] == True

def test_delete_task(client):
    client.post('/tasks', json={'title': 'Delete me'})
    res = client.delete('/tasks/1')
    assert res.status_code == 200
    assert res.json['message'] == 'Task deleted'

def test_delete_nonexistent_task(client):
    res = client.delete('/tasks/999')
    assert res.status_code == 404