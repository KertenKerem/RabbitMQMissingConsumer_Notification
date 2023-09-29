# Connection strings are passed as arguments at runtime or can be set in the code
# You should create first file1 using Master_file_generator.py in the repo

import requests, difflib, os, smtplib, sys, time
from requests.auth import HTTPBasicAuth
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime


RMQ_NAMES = ["consumer01","consumer02","consumer03"]

file1 = "Prod_RMQ_01.txt"
file2 = "output.txt"
fileList = [file1,file2]
now = datetime.now()
dtnow = now.strftime("%d-%m-%Y %H:%M:%S")


def get_number_of_consumers(queue_name):
    # Replace these values with your own
    host_ip = f"{argv[1]}"
    api_port = "15672"
    login = f"{argv[2]}"
    password = f"{argv[3]}"

    # Construct the API URL
    api_queues = f"http://{host_ip}:{api_port}/api/queues/%2F/{queue_name}"
    res = requests.get(api_queues, auth=HTTPBasicAuth(login, password))
    res_json = res.json()
    consumer_details = res_json["consumer_details"]
    number_of_consumers = len(consumer_details)
    # Print each consumer's details
    IP_List = []
    with open(file2, "a") as file:

        for i, consumer in enumerate(consumer_details):
            consIP = consumer['channel_details']['name'].split(":", 1)
            IP_List.append(consIP[0])
            file.write(consIP[0] +"#" + queue_name +"\n")

# Call the function with the desired queue name
for qName in RMQ_NAMES:
    get_number_of_consumers(qName)



def sort_lines_in_file(file_name):
    # Read the file
    with open(file_name, "r") as file:
        lines = file.readlines()

    # Split each line into IP address and service name, and store them in a list of tuples
    ip_service_list = [(line.split("#")[0], line.split("#")[1]) for line in lines]

    # Sort the list
    ip_service_list.sort()

    # Write the sorted list back to the file
    with open(file_name, "w") as file:
        for ip, service in ip_service_list:
            file.write(ip + "#" + service)

# Call the function with the desired file name
for rmqfile in fileList:
    sort_lines_in_file(rmqfile)


def compare_files(file1, file2):
    with open(file1, "r") as f1, open(file2, "r") as f2:
        lines1 = f1.readlines()
        lines2 = f2.readlines()
    diff = difflib.ndiff(lines1, lines2)
    different_lines = []
    for line in diff:
        if line.startswith('-'):
            different_lines.append(line.strip())
    return '\n'.join(different_lines)

different_lines = compare_files(file1, file2)

print(different_lines)


# Send an automated email
sender_email = 'sender@mail.address
receiver_email = 'receipent@mailaddress'
message = MIMEMultipart("alternative")


# Check if the files exist
if different_lines != "":
    print("sıkıntı var")

    lines = different_lines.split("\n")
    for line in lines:
        serverIP = line.split("#")[0]
        consumer_name = line.split("#")[1]
        description = (f"No response can be received from the consumer named {consumer_name} on the {serverIP} server. I request that the necessary checks be carried out.")
        body = f"""
<!DOCTYPE html><html lang="en">
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Simple Alert Page</title>
</head>
<body style="font-family: Arial, Helvetica, sans-serif;background-color: white;padding: 10%;max-width: 640px;">
<div class="container" style="padding: 15px;background-color: #8080802b;border-radius: 10px;max-width: 640px;height: 480px;">
<div class="alert_name" style="font-weight: 800;font-size: x-large;padding: 10px;background-color: red;color: white;border-radius: 10px;max-width: 640px;height: 10%;text-align: center;">Consumer Down</div><br>
<div class="details" style="background-color: #80808069;color: black;padding: 20px;border-radius: 10px;max-width: 640px;height: 70%;margin: 20 auto;text-align: left;">
<table style="padding: 5px;font-size: large;font-family: 'Courier New', Courier, monospace;">
<tr>
<td id="td1" style="vertical-align: text-bottom;min-width: 150px;"><b>Server IP</b></td>
<td class="td2" style="vertical-align: top;">:</td>
<td class="td2" style="vertical-align: top;">{serverIP}</td>
</tr>
<tr>
<td id="td1" style="vertical-align: text-bottom;min-width: 150px;"><b>Consumer Name<b></td>
<td class="td2" style="vertical-align: top;">:</td>
<td class="td2" style="vertical-align: top;">{consumer_name}</td>
</tr>
<tr>
<td id="td1" style="vertical-align: text-bottom;min-width: 150px;"><b>Last Control<b></td>
<td class="td2" style="vertical-align: top;">:</td>
<td class="td2" style="vertical-align: top;">{dtnow}</td>
</tr>
<tr>
<td id="td1" style="vertical-align: text-bottom;min-width: 150px;"><b>Description<b></td>
<td class="td2" style="vertical-align: top;">:</td>
<td class="td2" style="vertical-align: top;">{description}</td>
</tr>
</table>
</div></div></body></html>
"""



#add your smtp relay server address
        print (description)
        message.attach(MIMEText(body, 'html'))
        message['Subject'] = f'[ALERT] CONSUMER DOWN: '+ consumer_name + " / "+ serverIP
        message['From'] = sender_email
        message['To'] = receiver_email
        #Add the email body
        with smtplib.SMTP('your.server.ip.address', 25) as server:
            server.sendmail(sender_email, receiver_email,message.as_string())
            time.sleep(5)

    compare_files(file1, file2)

else:
    print(f"{dtnow} : Everything is OK")

    # Diff the files
    os.remove(file2)
