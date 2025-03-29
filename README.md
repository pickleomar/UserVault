# USERVAULT - Flask Web Application


UserVault is a web application built with Python using Flask that implements a secure authentication system and user management. The project follows the MVC (Model-View-Controller) architecture to clearly separate responsibilities, making the application easier to maintain and extend.

## Features

- **Secure Authentication**  
  User registration, login, and session management with secure storage of user credentials.

- **MVC Architecture**  
  Clear separation between data handling (Models), business logic (Controllers), and presentation (Views).

- **SQLAlchemy Integration**  
  Uses an ORM to manage CRUD operations on the database without writing raw SQL.

- **Password Management**  
  Hashing and verification of passwords using Werkzeug to ensure credential security.

- **Dynamic Templates**  
  Utilizes Jinja2 to generate dynamic HTML pages based on backend data.

## Prerequisites

- **Python 3.7+**
- **pip** (Python package manager)

## Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/pickleomar/UserVault.git
   cd UserVault
   ``` 

2. **Create and activate a virtual environment**
  ```bash
  python -m venv venv
  source venv/bin/activate
   ```
3.**Initialize the .env file **
```bash
  cp .env.exemple .env 
```
4. **Install the dependencies**
```bash
   pip install -r requirements.txt
```
5.**Initialize database**

  ```bash
    #Linux/MAcOS
     export FLASK_APP=app.py  #Entry point
    #Windows
    $env:FLASK_APP = "app.py"
   flask db init
   flask db migrate
   flask db upgrade
```
6.**Usage**
-Run the application:
```bash
   python run.py
or
   flask run
```

