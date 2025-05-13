import os
import logging
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

load_dotenv()
app = Flask(__name__)

# WebClient instantiates a client that can call API methods
# When using Bolt, you can use either `app.client` or the `client` passed to listeners.
client = WebClient(token=os.environ.get("SLACK_BOT_TOKEN"))
logger = logging.getLogger(__name__)


# GET endpoint for health check
@app.route('/status', methods=['GET'])
def status():
    return jsonify({"status": "API is running"}), 200

# POST endpoint to receive a challenge and echo it back
@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    print(data)
    channel_id = data.get('event').get('channel')
    message_ts = data.get('event').get('ts')

    # --- endpoint verification ---

    # Check if 'challenge' key exists

    # if not data or 'challenge' not in data:
    #     return jsonify({"error": "'challenge' field is missing"}), 200
    #
    # challenge_value = data['challenge']
    # return jsonify({"challenge": challenge_value}), 200

    try:
        # Call the chat.postMessage method using the WebClient
        # The client passes the token you included in initialization
        result = client.chat_postMessage(
            channel=channel_id,
            thread_ts=message_ts,
            text="Hello again :wave:"
            # You could also use a blocks[] array to send richer content
        )

        print(result)

    except SlackApiError as e:
        print(f"Error: {e}")

    return jsonify({"status": "success"}), 200

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5050)
