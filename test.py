import json
import logging as lg
import os
import pickle
import time

import pandas as pd
import yaml
from azure.storage.blob import ContainerClient

from flask import Flask, jsonify, request


def logging_fun(message):
    lg.basicConfig(filename="appliaction_log.txt",
                    format='%(asctime)s %(message)s',
                    filemode='w')
    lg.info(message)


def load_config():
    with open("config_listofdata.yaml" , "r+") as yaml_file:
        logging_fun("loaded the config file which have the azure connection string and container name")
        return yaml.load(yaml_file,Loader=yaml.FullLoader)

def list_data():
    config = load_config()
    container_client = ContainerClient.from_connection_string(config["azure_storage_connection_string"],config["container_name"])

    logging_fun("Created the Container client")

    d = {"container_name" : config["container_name"] , "list_of_files" : []}
    for i in container_client.list_blobs():
        d["list_of_files"].append(i.name)


    return d

app = Flask(__name__)


@app.route('/')
def Resource():
    return list_data()


if __name__=="__main__":
    app.run(debug=True) 


