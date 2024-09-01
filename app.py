# -*- coding: utf-8 -*-
import logging

from predict import load_prediction_model, predict_severity_matrix
from scripts import tabledef
from scripts import forms
from scripts import helpers
from flask import Flask, redirect, url_for, render_template, request, session, jsonify
import json
import sys
import os

app = Flask(__name__)
app.secret_key = os.urandom(12)  # Generic key for dev purposes only
logging.basicConfig(stream=sys.stdout, level=logging.INFO)
load_prediction_model()

# Heroku
#from flask_heroku import Heroku
#heroku = Heroku(app)

# ======== Routing =========================================================== #
# -------- Login ------------------------------------------------------------- #
@app.route('/', methods=['GET', 'POST'])
def login():
    if not session.get('logged_in'):
        form = forms.LoginForm(request.form)
        if request.method == 'POST':
            username = request.form['username'].lower()
            password = request.form['password']
            if form.validate():
                if helpers.credentials_valid(username, password):
                    session['logged_in'] = True
                    session['username'] = username
                    return json.dumps({'status': 'Login successful'})
                return json.dumps({'status': 'Invalid user/pass'})
            return json.dumps({'status': 'Both fields required'})
        return render_template('login.html', form=form)
    google_maps_api_key = os.getenv('GOOGLE_MAPS_API_KEY')
    return render_template('bycatch_tracker.html', api_key=google_maps_api_key)


@app.route("/logout")
def logout():
    # session['logged_in'] = False
    return redirect(url_for('login'))


# -------- Signup ---------------------------------------------------------- #
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if not session.get('logged_in'):
        form = forms.LoginForm(request.form)
        if request.method == 'POST':
            username = request.form['username'].lower()
            password = helpers.hash_password(request.form['password'])
            email = request.form['email']
            if form.validate():
                if not helpers.username_taken(username):
                    helpers.add_user(username, password, email)
                    session['logged_in'] = True
                    session['username'] = username
                    return json.dumps({'status': 'Signup successful'})
                return json.dumps({'status': 'Username taken'})
            return json.dumps({'status': 'User/Pass required'})
        return render_template('login.html', form=form)
    return redirect(url_for('login'))


# -------- Settings ---------------------------------------------------------- #
@app.route('/settings', methods=['GET', 'POST'])
def settings():
    if session.get('logged_in'):
        if request.method == 'POST':
            password = request.form['password']
            if password != "":
                password = helpers.hash_password(password)
            email = request.form['email']
            helpers.change_user(password=password, email=email)
            return json.dumps({'status': 'Saved'})
        user = helpers.get_user()
        return render_template('settings.html', user=user)
    return redirect(url_for('login'))


# -------- Bycatch Tracker ---------------------------------------------------------- #
@app.route('/bycatch_tracker', methods=['GET', 'POST'])
def bycatch_tracker():
    if session.get('logged_in'):
        google_maps_api_key = os.getenv('GOOGLE_MAPS_API_KEY')
        return render_template('bycatch_tracker.html', api_key=google_maps_api_key)
    return redirect(url_for('login'))


@app.route('/predict', methods=['POST'])
def predict():
    if session.get('logged_in'):
        data = request.get_json()
        longitude = data.get("longitude")
        latitude = data.get("latitude")
        app.logger.info(f"Endpoint /location hit with Longitude: {longitude}, Latitude: {latitude}")

        severity_matrix = predict_severity_matrix(longitude, latitude).tolist()
        return jsonify(prediction=severity_matrix)

    app.logger.info("Predict Endpoint Attempt: Unauthorized")
    response = jsonify({"message": "Unauthorized: User is not logged in."})
    response.status_code = 401
    return response


# ======== Main ============================================================== #
if __name__ == "__main__":
    app.run(debug=True, use_reloader=True, host="0.0.0.0")
