import requests
import boto3
import os
from datetime import date

url = ""
bucket_name = ""
api_name = "" # API name is pretty good here


def get_data():
    url = url

    headers = {
        'accept': "application/json",
        'authorization': f"Bearer {os.environ['xyz']}"
        }

    try:
        response = requests.request("GET", url, headers=headers)
    except Exception as e:
        print(f"Error: {e}")
    return response

def write_to_S3(data):
    try:
        s3 = boto3.resource('s3')
        logs = ""
        for line in data:
            logs += f"{line}\n"

        today = date.today()

        object = s3.Object(
            bucket_name=bucket_name, 
            key=f'{api_name}/{today.strftime("%m/%d/%Y")}/{api_name}.log'
        )

        object.put(Body=logs)
    except Exception as e:
        print(f"Error: {e}")


def lambda_handler(event, context):
    
    r = get_data()
    try:
        write_to_S3(r.json()['results'])
    except Exception as e:
        print(f"Error: {e}")

    return 200
