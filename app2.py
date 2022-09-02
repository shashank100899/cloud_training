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
    with open("config.yaml" , "r+") as yaml_file:
        logging_fun("loaded the config file which have the azure connection string and container name")
        return yaml.load(yaml_file,Loader=yaml.FullLoader)

def models_from_azure(data):
    config = load_config()
    housing_data = pd.read_csv(data)
    predicted_dict = {}
    container_client = ContainerClient.from_connection_string(config["azure_storage_connection_string"],config["container_name"])

    logging_fun("Created the Container client")

    if os.path.exists("models/"):
        pass
    else:
        os.mkdir("models")

    for i in container_client.list_blobs():
        with open("models/"+str(i.name),"wb+") as f:
            logging_fun("loaded the model pickel files from the azure storage acccount")
            f.write(container_client.download_blob(i.name).readall())

    for i in os.listdir("models/"):
        model = pickle.load(open("models/"+i,"rb"))
        predicted =  model.predict(housing_data)
        predicted_dict[str(i)] = list(predicted)
    return predicted_dict

app = Flask(__name__)

@app.route("/home")
def home():
    return '''<h1>Please go to the "predicted" route to see the predicted house prices</h1> 
    <h1>Thank you !</h1>'''

@app.route("/predicted",methods=["GET","POST"])
def read_data():
    logging_fun("Recevied a file for prediction and the file is sent by postman application")
    request_file = request.files['file']
    return models_from_azure(request_file)

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port=5000)
