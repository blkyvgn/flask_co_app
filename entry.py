from app import create_app 
from app.services.celery.celery import celery

app = create_app()
cel = celery

if __name__ == '__main__': 
    app.run(host='127.0.0.1', port='8000')