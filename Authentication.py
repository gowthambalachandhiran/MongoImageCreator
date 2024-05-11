from cryptography.fernet import Fernet
import yaml
from flask import Flask, request
from flask_caching import Cache
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import random

class ConnectingMongoServer:
    def __init__(self, yml_file):
        self.yml_file = yml_file
        
    def read_config(self):
        with open(self.yml_file) as f:
            data = yaml.safe_load(f)
            encrypted_username = data["credentials"]["username"]
            encrypted_password = data["credentials"]["password"]
            return encrypted_username, encrypted_password
        
    @staticmethod
    def __decrypt_credentials(key=b'oNVWCFWs0uH_nvWE4WDXYq1k7RcPaQAWgzh6DeVTLKA='):
        instance = ConnectingMongoServer("config.yaml")
        encrypted_username, encrypted_password = instance.read_config()
        cipher_suite = Fernet(key)
        username = cipher_suite.decrypt(encrypted_username.encode()).decode()
        password = cipher_suite.decrypt(encrypted_password.encode()).decode()
        return username, password
    
    def establish_connection(self, auth=None):
        if auth is None:
            auth = self.__decrypt_credentials()
        uname, pwd = auth
        connection_string = f"mongodb+srv://{uname}:{pwd}@cluster0.pykozdh.mongodb.net/"
        client = MongoClient(str(connection_string), server_api=ServerApi('1'))
        return client