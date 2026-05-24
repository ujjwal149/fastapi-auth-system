# FastAPI Backend Learning Project

This repository contains my learning journey with FastAPI, PostgreSQL, psycopg2, and SQLAlchemy.

## Technologies Used

* Python
* FastAPI
* PostgreSQL
* SQLAlchemy
* psycopg2
* Pydantic
* Uvicorn

---

## 📁 Project Structure

```bash
app/
│
├── main.py
├── database.py
├── models.py
├── schemas.py
└── routers/
```

---

## Features Implemented

* Database connection with PostgreSQL
* User creation API
* CRUD operations
* SQLAlchemy ORM integration
* Response models using Pydantic
* Environment variable setup

---

## 🔧 Installation

### Clone repository

```bash
git clone <repository-url>
cd fastAPI
```

### Create virtual environment

```bash
python -m venv venv
```

### Activate virtual environment

#### Windows

```bash
venv\Scripts\activate
```

#### Linux / Mac

```bash
source venv/bin/activate
```

---

## Install dependencies

```bash
pip install -r requirements.txt
```

---

## ▶️ Run FastAPI server

```bash
uvicorn app.main:app --reload
```

---

##  API Documentation

Swagger UI:

```bash
http://127.0.0.1:8000/docs
```

Redoc:

```bash
http://127.0.0.1:8000/redoc
```

---

##  Learning Goals

This project is focused on:

* Backend development
* REST API design
* Database integration
* ORM usage
* Clean project architecture
* Git & GitHub workflow

---

##  Author

Ujjwal Kumar
