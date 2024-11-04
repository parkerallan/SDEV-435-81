# Echo - Social Media App - SDEV-435-81
## Overview
The Social Media Application is a web-based platform designed for users to create posts and interact with content through comments and likes. Developed using the Django framework, it is a simple yet effective tool for sharing updates and engaging with others.

## Features
- User Registration and Login: Users can sign up, log in, and manage their accounts.
- Post Creation: Users can create and view posts.
- Commenting: Users can leave comments on posts.
- Liking: Users can like and dislike posts.
- Responsive Design: The application is designed to be accessible on both desktop and mobile devices.
- (Aspirational) Profile Management: Users can update their profile information including bios and profile pictures 

## Development Tools
### Backend:
- Django: Web framework for building the server-side logic.
- SQLite: Relational database system used in development and testing
- PostgreSQL: Relational database system used in production deployments
- Packages such as Gunicorn for the production web server and Whitenoise for serving static files, view requirements.txt for a full list of dependencies

### Frontend:
- HTML/CSS: This is used to build and style the user interface through Django Templates
- Bootstrap: Front-end CSS framework for rapidly building responsive design.

## Project Architecture 🏛️⚖️
This project, in its current form, is divided into two main apps: Pages and Posts. Each app is responsible for its models, views, URLs, and test cases. 

'Pages' handles user logic, such as registering an account and logging in, and eventually profile functionality, like editing one's profile or viewing others. 

'Posts' handles creating posts, commenting, and liking/disliking posts. This app is centered around the main business logic of viewing and creating interactive posts. 

'social_media_app' is the main driver of this project where users can find the app's configuration in settings.py. This folder also contains URLs (urls.py) and custom forms (forms.py) used throughout both apps in the project.
## Usage ⚙️🚀
### Try out a Production Build ⬇️
TBA

### Local Development Setup

### Prerequisites
- Python 3.9+ - [Download here](https://www.python.org/downloads/)
- pip - [Package Installer for Python](https://pip.pypa.io/en/stable/installation/)

### Setup
Clone the Repository:
```bash
git clone https://github.com/parkerallan/SDEV-435-81.git
cd SDEV-435-81
```
Configure your environment for 'development' on line 20 of settings.py:
```python
ENVIRONMENT = env('ENVIRONMENT', default='development')
```
Setup local environment with dependencies:
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
Finally, run the application:
```python 
python manage.py runserver
```
### Running Test Suite 🔍🧪
Test coverage for this app is provided through unit tests using Django's TestCase package
#### To run the tests from a development setup:
```python 
python manage.py test
```
For faster results and more information, use verbosity and parallel flags:
```python 
python manage.py test -v 2 --parallel 4
```
#### Alternatively, run the tests from the Django CI action on this page [here](https://github.com/parkerallan/SDEV-435-81/actions/workflows/django.yml), next, click the 'Run Workflow' dropdown and the green button to run the tests against the master branch
