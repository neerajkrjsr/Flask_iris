from flask import Flask, request, jsonify, render_template
import numpy as np
import pickle

# Create flask app
app = Flask(__name__)
model = pickle.load(open("model.pkl", "rb"))

@app.route("/",methods=['GET'])
def Home():
    return render_template("index.html")

# A decorator used to tell the application which URL is associated function
@app.route('/', methods =["GET", "POST"])
def PredictIrisSpecies():
    if request.method == 'POST':

        # Define global variable
        global float_features
        global features
        
        # Check input received from HTML form is float or not
        float_ok = "false"
        try:        
            float_features = [float(x) for x in request.form.values()]
            features = [np.array(float_features)]
            float_ok = "true"
        except ValueError:
            float_ok = "false"
        
        # Check if all elements in feature list are zeros or not
        non_zero_ok = "false"
        countzero_features = np.count_nonzero(features)
        if (countzero_features > 0):
            non_zero_ok = "true"
        else:
            non_zero_ok = "false"
        

        # Predict the species only for valid input features
        if (float_ok=='true') and (non_zero_ok=="true"):
            prediction = model.predict(features)
            result = "The flower species is {}".format(prediction)
        else:
            result = ""
        
        # Return the predicted value
        return render_template("index.html", Output = result)
    else:
        return render_template('index.html', Output = "")

if __name__ == "__main__":
    app.run(debug=True)