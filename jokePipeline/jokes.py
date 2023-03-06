import requests
import boto3
from datetime import date

u = "https://v2.jokeapi.dev/joke/Any?safe-mode&amount=10"
bucket_name = "add-bucket-name-here"
api_name = "jokes" # API name is usually pretty good


def get_data():
    url = u

    headers = {
        'accept': "application/json"
        }

    try:
        response = requests.request("GET", u, headers=headers)
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
