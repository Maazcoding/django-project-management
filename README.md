# Project Management Backend

A Django REST Framework-based backend for managing projects and tasks with JWT authentication.

## Project Structure

The project is organized into three main apps:

- **accounts**: Handles user registration, authentication, and profile management
- **projects**: Manages project CRUD operations with ownership controls
- **tasks**: Manages task CRUD operations linked to projects

## Features

- JWT-based authentication
- User registration and profile management
- Project and task CRUD with ownership validation
- Filtering, searching, and ordering
- Pagination support
- Permission-based access control
- Admin panel configuration

## Setup Instructions

1. Create and activate virtual environment
2. Install dependencies: `pip install -r requirements.txt`
3. Copy `.env.example` to `.env` and update values
4. Run migrations: `python manage.py migrate`
5. Create superuser: `python manage.py createsuperuser`
6. Run server: `python manage.py runserver`

## Running Tests

Execute all tests: `python manage.py test`

## Design Decisions

### Authentication
- Used djangorestframework-simplejwt for JWT token management
- Access tokens expire in 1 hour, refresh tokens in 1 day
- Password validation using Django's built-in validators

### Ownership & Permissions
- Custom IsOwner and IsTaskOwner permissions ensure users can only access their own data
- Querysets filtered by created_by field in all views
- Object-level permissions prevent unauthorized access

### Validation
- Project end date validated against start date
- Task due date validated against current date
- Task project ownership validated to ensure users only create tasks under their own projects
- Required field validation for titles

### Filters
- django-filter used for field-based filtering
- DRF's SearchFilter for text search on title and description
- DRF's OrderingFilter for sorting results
- All configured globally in settings with per-view customization

### Task Completion Logic
- is_completed field automatically set based on status in model's save method
- When status is 'done', is_completed becomes True
- When status changes from 'done', is_completed becomes False

### Pagination
- Global pagination set to 10 items per page
- Uses DRF's PageNumberPagination
- Returns count, next, previous, and results

## Environment Variables

- SECRET_KEY: Django secret key
- DEBUG: Debug mode toggle
- ALLOWED_HOSTS: Comma-separated allowed hosts
