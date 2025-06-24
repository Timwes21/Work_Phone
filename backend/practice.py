from twilio.rest import Client
import os
from dotenv import load_dotenv
load_dotenv()
from action_graph import graph
            
            
# account_sid = os.environ['ACCOUNT_SID']
# auth_token = os.environ['AUTH_TOKEN']
# twilio_phn_nmbr = os.environ['NUMBER']
# my_phn_nmbr = "+17726210972"
# client = Client(account_sid, auth_token)


# def send_message(body):
#     message = client.messages.create(
#         body=body,
#         from_=twilio_phn_nmbr,  # your Twilio phone number
#         to=my_phn_nmbr      # recipient's phone number
#     )
#     return message.status    
    

convo = [
    {"caller": "hello"},
    {"AI": "Hello i am tims ai assistant how may i help you"},
    {"caller": "Yes i would like to scehdule a callback for tomorow"},
    {"AI": "Ok what is your name"},
    {"caller": "My name is jerry"},
    {"AI", "Ok your callback is scheduled for tomorow, Jerry"},
]

result = graph.invoke({"convo": convo, "caller_id": "+17726210972"})

print(result)

