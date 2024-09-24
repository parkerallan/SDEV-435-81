# Echo - Social Media App - SDEV-435-81
## Overview
The Social Media Application is a web-based platform designed to enable users to create posts, and interact with content through comments and likes. It is developed using the Django framework for backend functionalities and utilizes HTML, CSS, and Bootstrap for the front end. This application is a simple yet effective tool for users to share updates and engage with others.

## Features
- User Registration and Login: Users can sign up, log in, and manage their accounts.
- Post Creation: Users can create and view posts.
- Commenting: Users can leave comments on posts.
- Liking: Users can like and dislike posts.
- Responsive Design: The application is designed to be accessible on both desktop and mobile devices.
- Profile Management: Users can update their profile information including bios and profile pictures (Aspirational)

## Development Tools
### Backend:
- Django: Web framework for building the server-side logic.
- SQLite: Relational database system for data storage.

### Frontend:
- HTML/CSS: This is used to build and style the user interface.
- Bootstrap: Front-end framework for responsive design.
Installation

## Prerequisites
- Python 3.8+
- pip

## Setup
Clone the Repository:
```python
git clone https://github.com/parkerallan/SDEV-435-81.git
cd SDEV-435-81
```
Run the application locally:
```python
# Create and activate a virtual environment
python -m venv env
env\Scripts\activate

# Install pip dependencies
pip install -r requirements.txt
```
For admin access, run migrations and create a root user:
```python 
python manage.py migrate
python manage.py createsuperuser
```
Run application:
```python 
python manage.py runserver
```
