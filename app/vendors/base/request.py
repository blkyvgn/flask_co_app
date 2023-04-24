from flask import Flask, Request
from werkzeug.datastructures import ImmutableOrderedMultiDict
from app.vendors.utils.validate import validate


class AppRequest(Request):
    # validation data from forms is is not form-wtf
    parameter_storage_class = ImmutableOrderedMultiDict
    validate = validate()