# Build control file with current RabbitMQ consumers 
# Connection strings are passed as arguments at runtime or can be set in the code

import requests, os, sys
from requests.auth import HTTPBasicAuth

# Set your own consumer list into this array
RMQ_NAMES = ["consumer01","consumer02","consumer03"]

def get_number_of_consumers(queue_name):
    # Replace these values with your own
    host_ip = f"{argv[1]}"
    api_port = "15672"
    login = f"{argv[2]}"
    password = f"{argv[3]}"

    file1 = "Prod_RMQ_01.txt"

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

