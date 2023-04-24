# flask_co_app
$ mkdir -p public/storage log\
(For local config data: add .env in root directory)

# database
flask db init\
flask db migrate\
flask db upgrade\
flask user create some_mail some_password

# locale
pybabel extract -F babel.cfg -k _l -o app/resources/translations/messages.pot app\
pybabel init -i app/resources/translations/messages.pot -d app/resources/translations -l en\
pybabel compile -d app/resources/translations\
after update translation\
pybabel extract -F babel.cfg -k _l -o app/resources/translations/messages.pot app\
pybabel update -i app/resources/translations/messages.pot -d app/resources/translations\
pybabel compile -d app/resources/translations

# redis
$ redis-server

# celery
celery -A entry.cel worker -l INFO

# test locale mail server
python -m smtpd -c DebuggingServer -n localhost:1025