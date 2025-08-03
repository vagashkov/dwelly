# dwelly
Simple yet functional and friendly property management system for family hotel or apartment owners

## Local deployment
### Installation
- create folder to store project files
- create media folder to store user-uploaded content
- clone this repo (src folder should appear together with LICENSE and README.md files)
- create virtual environment, activate it and install packages from requirements.txt file
- create Postgres database and fix database credentials in src.config.settings.local-dev.py
- do not forget to perform database migration and create superuser
- install Redis or any other message broker you prefer

### Launch
- launch redis using "redis-server" command in console
- launch Celery:
  - start new console
  - move to project folder
  - activate virtual environment
  - move to src
  - launch Celery: celery -A config worker
  - launch Django: python manage.py runserver --settings=config.settings.local-dev


## Docker deployment
- ensure that your Docker Desktop is up and running;
- navigate to src directory;
- create images and start containers: docker-compose -f docker-compose-dev.yml up -d --build;
- open src-web container terminal;
- perform migration and create superuser;
- proceed to standard Django landing page (https://127.0.0.1:8000)