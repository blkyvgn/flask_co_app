
def registration_commands(app, commands): 
	for commands_group in commands:
		app.cli.add_command(commands_group)
