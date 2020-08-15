# coding:utf-8

from flask import Blueprint

upload_api = Blueprint("upload", __name__)

from . import urls