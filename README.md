# dwelly
Simple yet functional and friendly property management system for family hotel or apartment owners

## Local installation
- create folder to store project files
- create media folder to store user-uploaded content
- clone this repo (src folder should appear together with LICENSE and README.md files)
- create virtual environment, activate it and install packages from requirements.txt file
- create Postgres database and fix database credentials in src.config.settings.local-dev.py
- do not forget to perform database migration and create superuser
- install Redis or any other message broker you prefer

## Local launch
- launch redis using "redis-server" command in console
- launch Celery:
  - start new console
  - move to project folder
  - activate virtual environment
  - move to src
  - launch Celery: celery -A config worker
  - launch Django: python manage.py runserver --settings=config.settings.local-dev
  - enjoy :)