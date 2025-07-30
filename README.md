# DjangifyLab
Django App Explorer. Test any Django app package with zero setup. Just plug, migrate, run.

**A clean and isolated sandbox to test Django app packages before integrating it into a real-world or production Django project.**

## Why you need DjangifyLab
When you develop a Django reusable app — for microservices integrations (such as authentication, alerting, monitoring...) or for entire standalone apps — you often test it inside an existing Django project. However, this approach can hide critical issues:

- The host project may already contain **dependencies that your app requires**, masking missing packages from `install_requires` in the setup.cfg Django app file.
- Your local environment may be **dirty or pre-configured**, leading to false assumptions that your app works in isolation.
- Without sandboxing, it's easy to **forget required dependencies** or overlook configuration steps when packaging the app.
- In a production deployment, **conflicting versions or missing environment variables** can cause unexpected runtime errors.

DjangifyLab provides:

- A clean Django project where you can install and test your `.tar.gz` reusable app.
- Full control over environment variables and configuration via `.env`.
- A consistent way to simulate deployment with docker containers.
- A place to define **external configuration files** (e.g. JSON, YAML) required by your app.

This helps ensure your reusable app is **self-contained, fully functional, and truly reusable** in any Django environment.


## Quickstart

1. DjangifyLab first setup
Follow these steps to install setup DjangifyLab (just for the first time):

- Clone the repository:
```bash
git clone https://github.com/Lorygold/DjangifyLab.git
cd DjangifyLab
```
- Create and activate the virtual environment:
```bash
python -m venv djangifylab-venv
source djangifylab-venv/bin/activate
```
- Install the DjangifyLab requirements:
```bash
pip install -r requirements.txt
```
- Create your admin Django superuser to access to the Django admin page (store your credentials):
```bash
python manage.py createsuperuser
```

2. Install your Django App to test
```bash
source djangifylab-venv/bin/activate
python install_app.py example-apps/your_app.tar.gz
```

Then, manually add your app to `INSTALLED_APPS` in `djangifylab_project/settings.py`:

```python
INSTALLED_APPS = [
    ...
    "your_app_name",
]
```

3. (Optional) Edit the `.env` file for Custom Environment Variables
If your app requires specific environment variables, edit the .env file in the project root:

These will be loaded automatically by the Django settings.


4. (Optional) Add App-Specific Configuration Files

If your app depends on external config files (e.g., JSON, YAML), place them inside `DjangifyLab/config_files/your_app_name/`

And in the `.env` file: `MY_APP_CONFIG_PATH=/full/path/to/DjangifyLab/config_files/your_app_name`

5. (Optional) Start Required Services with Docker

If your app relies on services like PostgreSQL, MongoDB, Redis, etc., you can start them via Docker:

```bash
docker compose -f docker/docker-compose.database.yml up -d postgres
```

6. Run the app and Launch your management commands

First of all, apply the migrations, then you can run the django server and the mangements commands available in your app:

```bash
python manage.py migrate
python manage.py runserver
python manage.py mgmt_command_name_of_you_app
```

Your app is now ready to be tested in a clean, production-like environment.

## Example
Switching to the `example-buffalogs-app` branch, you can see an example of a real django app like BuffaLogs (my open-source project thesis)
