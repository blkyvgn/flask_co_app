from app import app, cel, sio


if __name__ == '__main__': 
    # app.run(host='127.0.0.1', port='8000')
    sio.run(app, host='127.0.0.1', port='8000')