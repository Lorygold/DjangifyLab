# 1.x.x
## 1.3.0
### Features
* Added the single `entrypoint.py` script to run a single app installation or an app upgrade to test the compatibility between two versions of an app
* Upgraded Django to 5.2.4
* Added the `uprgade-runner` docker service in order to run the upgrade test mode in a container
* Added the `app-installer` docker service in order to run the install mode in a container
* Added the dynamic database selection based on the `.env-driven` modern Django project structures
* Added University exam project report
### Changes
* Set PostgreSQL as default DB
* Added the BuffaLogs 2.8.0 django app as test
## 1.2.0
### Features
* CI/CD: Added the "GitHub Release" step in the deploy workflow with softprops/action-gh-release@v2
## 1.1.2
### Bugfix
* CI/CD: Added the x-access-token in the deploy pipeline to push the tag
## 1.1.1
### Bugfix
* CI/CD: Fixed the deploy workflow
## 1.1.0
### Features
* Handled the multi-installation for more Django Reusable Apps in the example-apps folder (to check apps compatibility)
* DevOps: Added linters (flake8, black and isort) for code quality
* DevOps: Added python tests with pytest
* CI/CD: Integrated the CI pipeline with 2 workflows:
  * `pull_request` - to ensure that python tests, linters, and migrations of the Django apps work before merging the code
  * `deploy` - to create a release tag when a PR from develop to the main branch occurs
### Bugfix
* Fixed the buffalogs-2.6.0 package
* Fixed Buffalogs' environment variables in settings.py