# Matthew Mauer 01/20/2020
# Applying Flask frame work to build web interface for tool

from flask import Flask, render_template, url_for, request

# create the app
app = Flask(__name__)

# app.config['SECRET KEY'] = 'f195a11857065d27772a6a833a7ca1f3'

# An about page that explains the tool and takes user input for the
# initial query of a media perception map of a subject.
@app.route("/")
@app.route("/about")
def about():
    return render_template('about.html', title='About')

# The tool page. It receives the data from the previous user input, formats it, 
# and uses it and places a query to the GDELT GEO 2.0 API and embed the 
# resulting chloropleth map.
@app.route("/tool", methods=["POST", "GET"])
def tool():
    # Use reguest object to handle data from user input
    sentiment = request.args['sentiment']
    subject = request.args['subject'].replace(' ', '%20')
    if sentiment == 'positive':
        tone = '%20tone>3'
    else:
        tone = '%20tone<3'
    api = "https://api.gdeltproject.org/api/v2/geo/geo?query="
    mode = "&mode=sourcecountry"
    query = api + subject.lower() + tone + mode
    return render_template('toolpage.html', title='Tool', query=query)

if __name__ == "__main__":
    app.run(debug=True)