# Fast API backend app

## Purpose
Template app for a new Fast API backend application, it's applied to
a local SQLite database with no docker dependencies.


## What is included
- JWT Tokening mechanism and basic user management API.
- Application structure:
  - **Migrations** directory for Alembic migration usage
  - **Scripts** for creating the admin user
  - **App/Models** for defining ORM models (using SQLAlchemy)
  - **App/Schemas** for defining Pydantic models
  - **App/Routes** for defining API routes (provides a directory for each version)
  - **App/Services** for python objects for business logic
  - **Dependencies** and **database** for cross utilities and configurations

## How to run
- Add the app directory to PYTHONPATH
- If models have been added, then
  - Run Alembic revisions automatically (eg: `alembic revision --autogenerate`) or manually (eg: `alembic revision`)
  - Perform changes to database (eg: `alembic upgrade head`)
  - Run the initial script `python scripts/initial_user.py` for creating the admin user
    - It uses the DB configuration of the app
  - Run the app