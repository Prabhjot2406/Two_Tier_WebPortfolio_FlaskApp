# INTRODUCTION

SQLAlchemy is a powerful Python library for working with databases. You can use it to interact with SQL databases using either:

Core (low-level, like writing SQL)

ORM (Object Relational Mapper – more Pythonic and abstract)

## GETTING STARTED

**Step 1: Install SQLAlchemy**
```BASH
pip install sqlalchemy
```
**Step 2: Connect to a Database**
```bash
***✅ Absolute Path***

An absolute path tells Python exactly where the file is on your system, starting from the root directory.

🔹 Example:

from sqlalchemy import create_engine
engine = create_engine('sqlite:////Users/yourname/databases/mydb.db')

-This path starts from the root / and includes the full path to the database.

-Works regardless of where your Python file is located.

-On Windows, it might look like:

from sqlalchemy import create_engine
engine = create_engine('sqlite:///C:/Users/yourname/databases/mydb.db')
```
```bash
***✅ Relative Path***

A relative path is relative to the current working directory (usually where your Python script runs from).

🔹 Example:

from sqlalchemy import create_engine
engine = create_engine('sqlite:///mydb.db')

-This looks for (or creates) mydb.db in the same folder where your Python script runs.

-If your script is in project/ and you use 'sqlite:///data/mydb.db', it means project/data/mydb.db.

```
***✅ SQLite in-memory database***

from sqlalchemy import create_engine
engine = create_engine('sqlite:///:memory:')

***CODE***
```bash

from sqlalchemy import create_engine
engine = create_engine('sqlite:///:memory:')

```

**Step 3: Define Models (Tables)**

Use declarative_base() to define tables as Python classes.

```bash
from sqlalchemy.orm import declarative_base

from sqlalchemy import Column, Integer, String

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'       # default name is user: not necessary to put this line if __table__ is not define default name would be picked.

    id = Column(Integer, primary_key=True)   # will create initial col 1,2,3
    name = Column(String)                    # following cloumn name
    age = Column(Integer)                    # following cloumn age

```
**Step 4: Create the Tables**

```bash
Base.metadata.create_all(engine)
```
---
------
---
---
---
---
---
---
---
---


# Why Do We Need a Session in SQLAlchemy?

A **session** in SQLAlchemy is like a **middleman** between your Python code and the database.

It handles:
- Making **queries** to fetch data
- Sending **insert/update/delete** operations
- Managing **transactions** (i.e., commits and rollbacks)

Think of it as a **conversation** with the database that you control step-by-step.

---


## ✅ What is a Session?

A session in SQLAlchemy is like a middleman between your Python code and the database.

It handles:

✅ Making queries to fetch data

✅ Sending insert/update/delete operations

✅ Managing transactions (i.e., commits and rollbacks)

Think of it as a conversation with the database that you control step-by-step.


### 🔹 1. Transaction Management
- All changes you make (inserts, updates, deletes) are **not permanent** until you call `.commit()`.
- This lets you:
  - Group changes together
  - Roll back if something fails

### 🔹 2. Efficient Communication
- A session keeps a **cache of objects** you’ve loaded or created.
- This reduces unnecessary SQL queries.

### 🔹 3. Object Tracking
- SQLAlchemy can track Python objects that are mapped to database rows.
- Example: If you change a user's name in Python, SQLAlchemy knows and can sync it with the DB.

### 🔹 4. Safe Execution
- Avoids SQL injection.
- Ensures database consistency (no partial writes).

---

## ✅ Code Example

```bash
from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=engine)

session = Session()   
```
🔹 This is your live session


**Step 5: Create a Session**
```bash
from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=engine)
session = Session()
```
**Step 6: Insert Data**
```bash
user1 = User(name="Alice", age=30)
session.add(user1)
session.commit()

```

**Step 7: Query Data**

```bash
# Get all users
users = session.query(User).all()

for user in users:
    print(user.name, user.age)

```

**✅ Step 8: Update and Delete**

```bash
user = session.query(User).filter_by(name="Alice").first()
user.age = 31
session.commit()
```

```bash
session.delete(user)
session.commit()

```


# 🔗 Using SQLAlchemy with Flask

This guide shows how to integrate **SQLAlchemy** with a **Flask** web application using the `Flask-SQLAlchemy` extension.

---

## ✅ Installation

```bash
pip install flask flask_sqlalchemy
```

```bash 
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Step 1: Create Flask app
app = Flask(__name__)

# Step 2: Configure the database URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'  # relative path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # optional, to disable warning

# Step 3: Initialize SQLAlchemy
db = SQLAlchemy(app)

# Step 4: Define a Model (Table)
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    age = db.Column(db.Integer)

# Step 5: Create tables
with app.app_context():
    db.create_all()

# Step 6: Define routes
@app.route('/')
def home():
    return "Flask with SQLAlchemy is working!"

@app.route('/add')
def add_user():
    new_user = User(name="Alice", age=30)
    db.session.add(new_user)
    db.session.commit()
    return "User added!"

@app.route('/users')
def list_users():
    users = User.query.all()
    return "<br>".join([f"{user.name} ({user.age})" for user in users])

# Step 7: Run the app
if __name__ == '__main__':
    app.run(debug=True)

```



---

# 🔄 SQLAlchemy: With Flask vs Without Flask (Side-by-Side Comparison)

This document compares how to use SQLAlchemy with and without Flask using parallel code examples.

---

## ✅ Basic Setup Comparison

| With Flask (`Flask-SQLAlchemy`)                             | Without Flask (Pure SQLAlchemy)                          |
|-------------------------------------------------------------|-----------------------------------------------------------|
| ```python                                                   | ```python                                                 |
| from flask import Flask                                     | from sqlalchemy import create_engine                      |
| from flask_sqlalchemy import SQLAlchemy                     | from sqlalchemy.orm import declarative_base, sessionmaker |
|                                                             | from sqlalchemy import Column, Integer, String            |
|                                                             |                                                           |
| app = Flask(__name__)                                       | engine = create_engine("sqlite:///database.db")           |
| app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db' | Base = declarative_base()                             |
| app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False        |                                                           |
| db = SQLAlchemy(app)                                        |                                                           |
|                                                             | class User(Base):                                         |
| class User(db.Model):                                       |     __tablename__ = 'user'                                |
|     id = db.Column(db.Integer, primary_key=True)            |     id = Column(Integer, primary_key=True)                |
|     name = db.Column(db.String(100))                        |     name = Column(String(100))                            |
|     age = db.Column(db.Integer)                             |     age = Column(Integer)                                 |
|                                                             |                                                           |
| with app.app_context():                                     | Base.metadata.create_all(engine)                          |
|     db.create_all()                                         |                                                           |
|                                                             | Session = sessionmaker(bind=engine)                       |
|                                                             | session = Session()                                       |
| @app.route('/add')                                          | new_user = User(name="Alice", age=30)                     |
| def add():                                                  | session.add(new_user)                                     |
|     new_user = User(name="Alice", age=30)                   | session.commit()                                          |
|     db.session.add(new_user)                                |                                                           |
|     db.session.commit()                                     |                                                           |
|     return "User added"                                     |                                                           |
| ```                                                         | ```                                                       |

---

## 🧠 Key Differences

| Feature               | Flask-SQLAlchemy                    | Pure SQLAlchemy                      |
|----------------------|-------------------------------------|--------------------------------------|
| Setup                | Simpler with Flask integration      | Manual setup                         |
| Model Definition     | Inherit from `db.Model`             | Inherit from `Base`                  |
| Table Creation       | `db.create_all()`                   | `Base.metadata.create_all(engine)`   |
| Session Management   | `db.session`                        | `sessionmaker(bind=engine)`          |
| Routes               | Handled via `@app.route()`          | No built-in routing                  |
| Web Integration      | Built for web apps                  | Standalone scripts or CLI apps       |

---

## ✅ Summary

- **Flask-SQLAlchemy** is easier and cleaner when building web applications.
- **Pure SQLAlchemy** is ideal for scripts, automation, or when Flask is not used.
- Both approaches give you full power over database operations.

> Use Flask-SQLAlchemy for web apps, and pure SQLAlchemy for scripts or microservices.


---
# 📘 Flask + SQLAlchemy Code Explanation

This document breaks down the example Flask + SQLAlchemy code line by line.

---

## 🔁 Full Example Code

```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Model definition
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    age = db.Column(db.Integer)

# Create database tables
with app.app_context():
    db.create_all()

# Route to check app status
@app.route('/')
def home():
    return "Flask with SQLAlchemy is working!"

# Route to add a user
@app.route('/add')
def add_user():
    new_user = User(name="Alice", age=30)
    db.session.add(new_user)
    db.session.commit()
    return "User added!"

# Route to list users
@app.route('/users')
def list_users():
    users = User.query.all()
    return "<br>".join([f"{user.name} ({user.age})" for user in users])

# Run the app
if __name__ == '__main__':
    app.run(debug=True)



---

# 🐍 SQLAlchemy Without Flask

This guide demonstrates how to use SQLAlchemy without Flask to perform basic database operations.

---

## 📦 Full Python Code

```python
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

# Step 1: Connect to database (creates a new file if it doesn't exist)
engine = create_engine("sqlite:///database.db")

# Step 2: Define the base class for models
Base = declarative_base()

# Step 3: Define a model (a table)
class User(Base):
    __tablename__ = 'user'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    age = Column(Integer)

# Step 4: Create the table(s) in the database
Base.metadata.create_all(engine)

# Step 5: Create a session to interact with the DB
Session = sessionmaker(bind=engine)
session = Session()

# Step 6: Create and add a user
new_user = User(name="Alice", age=30)
session.add(new_user)
session.commit()

# Step 7: Query the database
users = session.query(User).all()
for user in users:
    print(f"Name: {user.name}, Age: {user.age}")
