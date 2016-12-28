#pylint: disable=W0312,C0111

import json
from flask import Flask, request, Response
from mote import LiveMote

app = Flask(__name__)
mote = None

def get_response(message, title):
	response = {}
	response["version"] = "1.0"
	response["response"] = {}
	response["response"]["outputSpeech"] = {}
	response["response"]["outputSpeech"]["type"] = "PlainText"
	response["response"]["outputSpeech"]["text"] = message
	response["response"]["card"] = {}
	response["response"]["card"]["content"] = message
	response["response"]["card"]["title"] = title
	response["response"]["card"]["type"] = "Simple"
	response["response"]["shouldEndSession"] = True
	response["sessionAttributes"] = {}
	return response

@app.route('/', methods=['POST'])
def post_alexa_request():
	post_data = request.json  # data is empty
	response = None

	if post_data["request"]["intent"]["name"] == "TurnOffIntent":
		response = get_response("Turning off", "OK")
	else:
		response = get_response("OK setting desired colour", "OK")
		slot_colour = post_data["request"]["intent"]["slots"]["Colour"]["value"]
		if not slot_colour in ["red", "green", "blue"]:
			response = get_response("Can only set red, green or blue", "Error")
		else:
			red = 0
			green = 0
			blue = 0

			if slot_colour == "red":
				red = 255
			elif slot_colour == "green":
				green = 255
			elif slot_colour == "blue":
				blue = 255
			mote.set_colour(red, green, blue)
	return Response(json.dumps(response), mimetype='application/json')

if __name__ == '__main__':
	global mote
	mote = LiveMote()
	mote.setup()
	app.run(debug=True, host='0.0.0.0')
