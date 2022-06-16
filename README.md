## Update Phone Call Database script
# This script is triggered when a webhook is received

- The script takes in data from the JSON message sent from the webhook refines data and then stores data into a MySQL Database
- The Webhook listener is set up in a Flask application and listens for webhooks sent from Aircall
- The Webhook is fired from Aircall everytime a phone call is ended
- Aircall sends a JSON message with call information to a specified URL, once the message is authenticated this scipt is then fired 

# Note: Cloudways is the database helper that connects the server to the database

