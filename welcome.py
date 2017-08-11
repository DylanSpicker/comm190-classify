import os
from flask import Flask, jsonify, request
from watson_developer_cloud import NaturalLanguageClassifierV1
import random
import csv

natural_language_classifier = NaturalLanguageClassifierV1(
  username='3a7e240e-b28e-46b0-aa6c-6a59310ea203',
  password='EG7xOCiiL8uq')

classifier_id = '359f41x201-nlc-198247'

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

# Define the Random Comment Route
# This route simply selects a comment at random from the 
#   complete CSV of all of the Amazon reviews
@app.route('/random-comment')
def SelectRandomComment():
    # Open the CSV file
    with open('static/Amazon_Reviews_Keurig.csv', 'r') as csvfile:
        # Take the CSV file and turn it into a list
        comments_csv = list(csv.reader(csvfile))    # csv.reader is a built-in ability to nicely read csv files

    # random.randrange generates a random number between the start value (0) and endvalue (length of list)
    rand_element = random.randrange(0, len(comments_csv))

    # Return the random element directly
    # Each line is currently in a list, with a single element, which is why
    #   we return [rand_element][0]; this is a result of casting the entire csv file
    #   to a list. For clarity, try printing comments_csv[10]
    return comments_csv[rand_element][0]


port = os.getenv('PORT', '5000')
if __name__ == "__main__":
	app.run(host='0.0.0.0', port=int(port), debug=True)
