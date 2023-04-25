from app.extensions import sock

@sock.route('/echo')
def echo(ws):
	print(ws)
	while True:
		data = ws.receive()
		print('data: ', data)
		ws.send(data)