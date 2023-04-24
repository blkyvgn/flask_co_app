from app.extensions import sock

@sock.route('/echo')
def echo(ws):
	print('---- ws ----')
	while True:
		print('---- while ----')
		data = ws.receive()
		ws.send(data)