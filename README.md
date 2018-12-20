# Simple API for Flask-based WIKI

### Deployment

1.  Create necessary db user and table
2.  Install dependencies from requirements.txt file
2.  Fill up your enviroment variables OR set defaults
    *  FLASK_DEBUG - standard Flask debug mode
    *  FLASK_DB_URL - url for db server
    *  FLASK_DB_PORT - port for db server
    *  FLASK_DB_NAME - db name
    *  FLASK_DB_USER - db user
    *  FLASK_DB_PASSWORD - password for your user
3.  Make some migration magic. Open your console and type
    * `flask db migrate` - this will create migrations (if you changed some code, if no - you should omit this step)
    * `flask db upgrade` - this will apply existing migrations
4. If you want to run Flask development server you can simply type `flask run`. If you want to upload it somewhere - there are initial config for UWSGI server.
   Just install UWSGI, edit ini-file with settings and run while you inside project directory `uwsgi uwsgi.ini`.
