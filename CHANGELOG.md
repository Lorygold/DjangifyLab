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