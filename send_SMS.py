import os, vonage
from dotenv import load_dotenv
from os.path import join, dirname




# dotenv_path = join(dirname(__file__), "../.env")
# load_dotenv(dotenv_path)

VONAGE_API_KEY = ("d8b5ed18")
VONAGE_API_SECRET = ("mcMGYJoWTE6C8Rjx")
VONAGE_BRAND_NAME = ("South Canteen")
TO_NUMBER = (6590288065)


client = vonage.Client(key=VONAGE_API_KEY, secret=VONAGE_API_SECRET)

responseData = client.sms.send_message(
    {
        "from" : VONAGE_BRAND_NAME,
        "to" : TO_NUMBER,
        "text" : "Your OTP is: xxxxxx"
    }

)

if responseData["messages"][0]["status"] == "0":
    print("Message sent successfully.")

else:
    print(f"Message failed with error: {responseData['messages'][0]['error-text']}")