from flask import Flask, request
import requests
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

@app.route('/bot', methods=['POST'])
def bot():
    incoming_msg = request.form['Body'].lower()  # Retrieve message body from Twilio request
    resp = MessagingResponse()
    msg = resp.message()
    responded = False

    if 'quote' in incoming_msg:
        # Return a quote
        r = requests.get('https://api.quotable.io/random')
        if r.status_code == 200:
            data = r.json()
            quote = f'{data["content"]} ({data["author"]})'
        else:
            quote = 'I could not retrieve a quote at this time, sorry.'
        msg.body(quote)
        responded = True

    elif 'cat' in incoming_msg:
        # Return a cat pic
        msg.media('https://cataas.com/cat')
        responded = True

    elif 'language' in incoming_msg:
        # Send interactive message for language preference
        msg.body("Please choose your language preference:")
        msg.add_button('Hindi', 'hindi')
        msg.add_button('English', 'english')
        responded = True

    elif 'hindi' in incoming_msg:
        msg.body("You have selected Hindi.")
        responded = True

    elif 'english' in incoming_msg:
        msg.body("You have selected English.")
        responded = True

    if not responded:
        msg.body('I only know about famous quotes, cats, and language preferences, sorry!')

    return str(resp)

if __name__ == '__main__':
    app.run(debug=True)  # Run Flask app in debug mode for easier debugging
