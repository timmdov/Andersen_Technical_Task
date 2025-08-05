# ***Andersen Technical Task***

This project was created to satisfy Andersen Technical Task's requirement which is part of Andersen's recruitment process. The requirements that I was tasked with are listed below in ***Requirements*** section. More details about my project can be found in ***Project Description*** section. The project installation instruction can be found in ***Installation & Set Up*** section.

## ***Requirements***

1. ***Create a User model with the following fields:***
   - First name (first_name) - string, required field;
   - Last name (last_name) - text, optional field;
   - Username (username) - string, required field, unique.
   - Password (password) - string, required field, min 6 symbols.
2. ***Create a Task model with the following fields:***
   - Title (title) - string, required field;
   - Description (description) - text, optional field;
   - Status (status) - selection from predefined values, for example: "New", "In Progress", "Completed".
   - User id (user_id) - int, Foreign key on user table (cascade delete).
3. ***Implement CRUD (Create, Read, Update, Delete) operations for tasks:***
   - Get a list of all tasks;
   - Get a list of all user's tasks;
   - Get information about a specific task;
   - Create a new task;
   - Update task information (can be updated only by owner);
   - Delete a task (can be deleted only by the owner).
4. ***Implement API endpoints for the following actions:***
   - Marking a task as completed;
   - Filtering tasks by status.
5. ***Add user authentication and authorization using JWT. (Only authorized users have access to the service)***
6. ***Implement pagination for the task list.***
7. ***Write unit tests for the API endpoints.***
8. ***Use PostgreSQL as the database to store data. Create the corresponding database configuration in the chosen web framework.***
9. ***Create a README.md file in the project repository with project documentation, including installation instructions, API documentation, and any other relevant information.***
10. ***Create a Git repository for the project on GitHub and regularly commit and push changes.***

## ***Project Description***

For a better understanding of the project, below i listed a brief description for all the components of the my description.

- ***app*** - Root directory.
  - ***api*** - Organizes all applications HTTP endpoints and API routing logic.
    - ***endpoints*** - Contains all endpoints.
      - ***auth.py*** - Defines user authentication endpoints.
      - ***tasks.py*** - Defines tasks endpoints.
    - ***router.py*** - Central router for the API
  - ***core*** - Contains security and configuration utilities utilities.
    - ***config.py*** - Centralizes configuration for the app using env variables.
    - ***dependencies.py*** - Defines common dependencies for FastAPI.
    - ***security.py*** - Implements core security features.
  - ***db*** - Contains the configuration and utilities for connecting to the application's database using SQLAlchemy.
    - ***base.py*** - Defines SQLAlchemy base class for all SQLAlchemy models.
    - ***session.py*** - Configures the db engine and provides a way for the app to interact with db.
  - ***tasks*** - Contain all logic and definitions related to tasks management.
    - ***crud.py*** - Implements the CRUD operations for tasks.
    - ***model.py*** - Defines Tasks SQLAlchemy Model (Task Table in the databse).
    - ***schemas.py*** - Contains Pydantic models/schemas
  - ***users*** - Contains all logic and definitions related to users management.
    - ***crud.py*** - Implements the CRUD operations for users. 
    - ***models.py*** - Defines User SQLAlchemy Model (User Table in the database).
    - ***schemas.py*** - Contains Pydantic models/schemas.
  - ***main.py*** - Serves as an entry point for the FastAPI application and initializes the application. 
- ***scripts***
  - ***__init__db.py*** - Contains scripts for database tables initialization.
- ***tests***
  - ***test_auth.py*** - Contains unit tests for authentication endpoints.
  - ***test_tasks.py*** - Contains unit tests for tasks endpoints.
- ***.env*** - Contains environment variables. 
- ***Dockerfile*** - This file is in order to dockerize/containerize the application for easier project startup.
- ***requirements.txt*** - This file contains all project requirements which have to be installed in order to run this project.  

## Prerequisites

- **Python 3.11+** 
- **PostgreSQL 15+**
- **Git**
- **Docker** (optional, for containerized setup)

## ***Installation & Set Up*** 

The installation and set up instructions are listed below.

### 1. Clone the Repository

```bash
git clone https://github.com/timmdov/Andersen_Technical_Task.git
cd Andersen_Technical_Task
```

### 2. Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Database Setup

```bash
# Install PostgreSQL (if not already installed)
# On macOS with Homebrew:
brew install postgresql
brew services start postgresql

# Ubuntu/Debian:
sudo apt update
sudo apt install postgresql postgresql-contrib
sudo systemctl start postgresql

createdb todoapp

psql -U postgres
CREATE DATABASE todoapp;
\q
```

### 5. Environment Configuration

Create a `.env` file in the root directory:

```bash
python -c "import secrets; print('SECRET_KEY=' + secrets.token_urlsafe(48))"
```

Create `.env` file with the following content:

```env
# Security
SECRET_KEY=your_generated_secret_key_from_above
# Signing Algorithm
ALGORITHM=HS256
# Token expiration (in minutes)
ACCESS_TOKEN_EXPIRE_MINUTES=30
# Database
DATABASE_URL=postgresql://postgres:your_password@localhost:5432/todoapp
```

### 6. Run the Application

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The installation and set up instructions are listed below.

- ***Clone the repository git clone https://github.com/timmdov/Andersen_Technical_Task.git*** 
- ***After cloning the repository, create .env in root directory with the following contents:*** 
  - ***SECRET_KEY=Random String*** 
    - python -c "import secrets; print(secrets.token_urlsafe(48))" 
  - ***ALGORITHM=Signing Algorithm***
    - HS256 was used during testing and development.
  - ***ACCESS_TOKEN_EXPIRE_MINUTES=Your Preferred Expiry Time for the token***
  - ***DATABASE_URL=Your Database URL***
- ***Install requirements: pip install -r requirements.txt***
After the setup above the application can be ran in the main.py.

## Docker Setup 

To run this project using Docker follow the instructions below:

- ***Install Docker, if not already installed***
- ***Build the Docker image = docker build -t my-fastapi-app . (Run in root dir)***
- ***Run the container = docker run --rm -p 8000:8000 my-fastapi-app***
- ***To stop CTRL+C/docker stop <container_id_or_name>***

 Available at: http://localhost:8000


