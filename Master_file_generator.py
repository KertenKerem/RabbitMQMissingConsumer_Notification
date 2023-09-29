import requests, os, sys
from requests.auth import HTTPBasicAuth

RMQ_NAMES = ["APIReadQ1","APIReadQ2","APIReadQ3","APIReadQ4","APIReadQDMZ1","APIReadQDMZ2","APIReadQDMZ3","APIReadQDMZ4",
"APIReadQDMZ5","APIReadQDMZ6","AS2APIReadQ1","AS2APIReadQ3","AS2APIReadQ4",
"MiddlewareServiceReadQ1","MiddlewareServiceReadQ2","accounting","amazon","callCenter","documentManager","ebk","email","geocoding",
"imageProcessing","marketPlace","pushnotification","reporting","routing","sms","sorting","tracking",
"turkcell","util","webHook","notification","DirectorReadQ","parcelDelivery"]

def get_number_of_consumers(queue_name):
    # Replace these values with your own
    host_ip = "10.201.1.211"
    api_port = "15672"
    login = "ynk"
    password = "ynk"

    # Construct the API URL
    api_queues = f"http://{host_ip}:{api_port}/api/queues/%2F/{queue_name}"
    res = requests.get(api_queues, auth=HTTPBasicAuth(login, password))
    res_json = res.json()
    consumer_details = res_json["consumer_details"]
    number_of_consumers = len(consumer_details)
    # Print each consumer's details
    IP_List = []
    with open("Prod_RMQ_01.txt", "a") as file:
        for i, consumer in enumerate(consumer_details):
            consIP = consumer['channel_details']['name'].split(":", 1)
            IP_List.append(consIP[0])
            file.write(consIP[0] +"#" + queue_name +"\n")

# Call the function with the desired queue name
for qName in RMQ_NAMES:
    get_number_of_consumers(qName)

file1 = "Prod_RMQ_01.txt"