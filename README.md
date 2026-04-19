# Task Management App

A simple REST API built with Flask and SQLite for managing tasks.

## Features
- Create, read, update, delete tasks
- Mark tasks as done

## Run locally
```bash
pip install -r requirements.txt
python app.py
```

## Run tests
```bash
PYTHONPATH=. pytest tests/ -v
```

## Run with Docker
```bash
docker build -t task-manager-app .
docker run -p 5000:5000 task-manager-app
```
