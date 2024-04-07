from openai import OpenAI
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
from dotenv import load_dotenv
import os
import sys

load_dotenv()
twilio_phone_number = "whatsapp:+14155238886"
api_key = os.getenv("OPENAI_API_KEY")
account_sid = os.getenv("TWILIO_ACCOUNT_SID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")



app = Flask(__name__)

# Create a Twilio client object with your account SID and auth token
client = Client(account_sid, auth_token)
openaiClient=OpenAI(api_key=api_key)
# Default message on the home page.
@app.route('/')
def home():
    return 'All the best brother !'



# Handle incoming messages
@app.route('/incoming', methods=['POST'])
def handle_incoming_message():
    try:
        incoming_message = request.form['Body']
        whatsapp_phone_number=request.form["From"]
        # Pass the history list to ChatGPT with message indicating it's previous user messages
        prompt = "correct the grammar and spellings in the below text keep the vocab simple and maintain indian tone:\n" + incoming_message
        try:
            response = openaiClient.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "system", "content": "You are a helpful assistant."},
{"role": "user", "content": prompt}],
                max_tokens=600,
                n=1,
                stop=None,
                temperature=0.7
            ).choices[0].message.content
        except Exception as e:
            print("failed")
            print(e)
        print(response)
        
        # Create a Twilio MessagingResponse object
        twilio_response = MessagingResponse()

        # Add the response to the Twilio MessagingResponse object
        twilio_response.message(response)

        # Send the response back to the user
        try:
            message = client.messages.create(
                body=response,
                from_=twilio_phone_number,
                to=whatsapp_phone_number
            )
        except Exception as e:
            print("failed to sent")
            print(e)


        # Print the message SID
        print("Message SID:", message.sid)

        # Return the Twilio MessagingResponse object
        # return str(twilio_response)
    except:
        pass
    return 'OK',200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)