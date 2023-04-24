from flask import Flask
from .request import AppRequest

class AppFlask(Flask):
    request_class = AppRequest