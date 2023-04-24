

def registration_blueprints(base, blueprints): 
	''' Registration blueprints '''
	for blueprint in blueprints:
		base.register_blueprint(blueprint)