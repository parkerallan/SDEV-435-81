# Echo - Social Media App - SDEV-435-81
## Executive Summary
The Social Media Application is a web-based platform designed for users to create posts and interact with content through comments and likes. Developed using the Django framework, it is a simple yet effective tool for sharing updates and engaging with others.

### Features
- User Registration and Login: Users can sign up, log in, and manage their accounts.
- Post Creation: Users can create and view posts.
- Commenting: Users can leave comments on posts.
- Liking: Users can like and dislike posts.
- Responsive Design: The application is designed to be accessible on both desktop and mobile devices.
- (Aspirational) Profile Management: Users can update their profile information including bios and profile pictures 

### Development Tools
#### Backend:
- Django: Web framework for building the server-side logic.
- SQLite: Relational database system used in development and testing
- PostgreSQL: Relational database system used in production deployments
- Packages such as Gunicorn for the production web server and Whitenoise for serving static files, view requirements.txt for a full list of dependencies

#### Frontend:
- HTML/CSS: This is used to build and style the user interface through Django Templates
- Bootstrap: Front-end CSS framework for rapidly building responsive design.

## System Design
This project, in its current form, is divided into two main apps: Pages and Posts. Each app is responsible for its models, views, URLs, and test cases. 

'Pages' handles user logic, such as registering an account and logging in, and eventually profile functionality, like editing one's profile or viewing others. 

'Posts' handles creating posts, commenting, and liking/disliking posts. This app is centered around the main business logic of viewing and creating interactive posts. 

'social_media_app' is the main driver of this project where users can find the app's configuration in settings.py. This folder also contains URLs (urls.py) and custom forms (forms.py) used throughout both apps in the project.
## Testing Plan
Test coverage for this app is provided through unit tests using Django's TestCase package. Anyone can run the tests from their developer setup or from the repository itself. Tests running in the repository via GitHub actions can be set to run at scheduled intervals as a continuous method of testing.
#### To run the tests from a development setup:
```python 
python manage.py test
```
For faster results and more information, use verbosity and parallel flags:
```python 
python manage.py test -v 2 --parallel 4
```
#### Alternatively, run the tests from the Django CI action on this page [here](https://github.com/parkerallan/SDEV-435-81/actions/workflows/django.yml), next, click the 'Run Workflow' dropdown and the green button to run the tests against the master branch
## Deployment Plan
- Deployments can vary widely based on availability, performance, and scalability needs. I will provide a more general outline for how I run a deployment with the app. I'm using Railway to host both the web server and PostgreSQL database. Platforms like AWS, DigitalOcean, and Heroku work as well.
- In its current form, the app's settings.py file is prepared for production deployments, users will need to create a .env file in the project root to manage variables that will be used with your hosting provider. The environment file should contain variables for the following:
```bash 
ENVIRONMENT=<development-or-production-here>
SECRET_KEY=<your-secret-key-here>
DATABASE_URL=<database-connector-here>
```
- Users can deploy using WSGI or ASGI, however, Gunicorn currently comes with the pip installation for WSGI web server deployment.
- Next, users must run "python manage.py collectstatic" to gather all static assets if any changes have been made to static images already included in the project.
- With your hosting provider of choice, create a PostgreSQL database and save the database connector.
- Next, your provider might ask you to specify the start command for the web server, in this case: "gunicorn social_media_app.wsgi:application".
- Next, add your environment variables. These include the database connector url, project-specific secret key, and environment as "production".
- Depending on the provider, there are features for deployment logging and redeploying with each merge. I recommend both of these
- In the future, profile pictures or static media types saved by users will be hosted via AWS S3 or a similar media hosting service.
- More specific settings can be configured such as setting up ALLOWED_HOSTS, and enforcing security measures like SECURE_SSL_REDIRECT and SECURE_HSTS_SECONDS for HTTPS-only traffic.
## Maintenance Plan
- The maintenance plan involves regular updates and monitoring to ensure application reliability, security, and performance.
- Automated scripts will be set to back up the database and test the integrity of data. 
- Key dependencies, including Django and any third-party packages, will be continually reviewed and updated to mitigate security vulnerabilities or package deprecation.
- Performance will be monitored through database logging and response times. More extenseive analytics tools and alerts will be implemented in the future.
- Unit tests will automatically run at scheduled intervals to test features using existing Django CI GitHub Workflows.
- Having a scheduled maintenance window will allow for downtime if necessary and will likely occur at night with unit test runs.
- The documentation will be continuously updated and maintained to assist with troubleshooting and onboarding for any future team members or collaborators.
## Developer Setup

### Prerequisites
- Python 3.9+ - [Download here](https://www.python.org/downloads/)
- pip - [Package Installer for Python](https://pip.pypa.io/en/stable/installation/)

### Steps
Run the commands to clone the Repository:
```bash
git clone https://github.com/parkerallan/SDEV-435-81.git
cd SDEV-435-81
```
Edit your environment for 'development' on line 20 of settings.py:
```python
ENVIRONMENT = env('ENVIRONMENT', default='development')
```
Edit your environment for all hosts (rather than the prod URL you choose) on line 38 of settings.py:
```python
ALLOWED_HOSTS = ['*']
```
In your terminal run the commands to set up a virtual environment with dependencies:
```python
# Create and activate a virtual environment
python -m venv env
env\Scripts\activate

# Install pip dependencies
pip install -r requirements.txt
```
For admin access, run the following commands for migrating and creating a root user:
```python 
python manage.py migrate
python manage.py createsuperuser
```
Finally, run the application using this command:
```python 
python manage.py runserver
```
## Client Setup
End-users can try a live production build now⬇️ All this is required is registering an account⬇️

[https://sdev-435-81-production.up.railway.app](https://sdev-435-81-production.up.railway.app)

This is for users who just want to test the app and not go through the steps of setting up a developer environment like the above.
