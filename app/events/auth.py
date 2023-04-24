from app.extensions import logger
from flask.signals import Namespace 

auth = Namespace()

# Signals List
signin_signal = auth.signal('signin-signal') 
signup_signal = auth.signal('signup-signal') 
signout_signal = auth.signal('signout-signal')

@signin_signal.connect
def user_signin(sender, **kwargs):
	''' User Log In Event '''
	logger.info(f'USER: {kwargs["username"]}: SIGN-IN.')

@signup_signal.connect
def user_signup(sender, **kwargs):
	''' User Register Event '''
	logger.info(f'USER: {kwargs["username"]}: SIGN-UP.')

@signout_signal.connect
def user_signout(sender, **kwargs): 
	''' User Log Out Event '''
	logger.info(f'USER: {kwargs["username"]}: SIGN-OUT.')