import os
from flask import Flask, jsonify, request
from watson_developer_cloud import NaturalLanguageClassifierV1

natural_language_classifier = NaturalLanguageClassifierV1(
  username='<Your_NLC_Username>',
  password='<Your_NLC_Password>')

classifier_id = '<Your_classifier_ID>'

app = Flask(__name__)

# Define the Homepage Route
# This will simply return the static HTML file
#   which contains the front-end application
@app.route('/')
def Welcome():
    # When the user visits http://hostname.mybluemix.net/ 
    #   return the static file kept at: /static/index.html
    return app.send_static_file('index.html')

# Define the Analyze Route
# This will take the text submitted by the users
#   pass it along to the Watson NLC analysis SDK and 
#   return the results of the call
@app.route('/analyze', methods=['POST', 'GET'])
def AnalyzeRequest():
    # Get the Request Data
    comment_text = request.form['text']

    # Make a classification request
    # Simply call the "classes" method on the "natural_language_classifier" object created at the outset
    classes = natural_language_classifier.classify(classifier_id, comment_text)

    # Return the classes; jsonify simply re-encodes the data in a means
    #   that is easy to parse using the JavaScript file
    return jsonify(classes)

port = os.getenv('PORT', '5000')
if __name__ == "__main__":
	app.run(host='0.0.0.0', port=int(port), debug=True)
