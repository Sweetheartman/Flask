# coding:utf-8

from flask_restful import Api
from . import upload_api
from .uploadResourse import UploadImageResource, UploadFilesResource, DownloadResource

api = Api(upload_api)
api.add_resource(UploadImageResource, "/images", endpoint="images")
api.add_resource(UploadFilesResource, "/files", endpoint="files")
api.add_resource(DownloadResource, "/download", endpoint="download")

# "http://127.0.0.1:5000/_uploads/files/20200422251192141.docx"




