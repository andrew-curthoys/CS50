import cs50
import csv

from flask import Flask, jsonify, redirect, render_template, request

# Configure application
app = Flask(__name__)

# Reload templates when they are changed
app.config["TEMPLATES_AUTO_RELOAD"] = True


@app.after_request
def after_request(response):
    """Disable caching"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET"])
def get_index():
    return redirect("/form")


@app.route("/form", methods=["GET"])
def get_form():
    return render_template("form.html")


@app.route("/form", methods=["POST"])
def post_form():
    # getting form inputs
    first_name = request.form.get("firstName")
    gender = request.form.get("gender")
    pizza_preference = request.form.get("pizza")
    pizza_frequency = request.form.get("pizzaTimes")

    # error checking to make sure all parts of the form are filled out
    if not first_name or not gender or not pizza_preference or not pizza_frequency:
        return render_template("error.html", message="Please fill in all fields. Pizza is important.")
    else:
        with open('survey.csv', 'r') as csvfile:
            # check if file has any data in it
            # if it does, we will append to the end of it
            # if not we'll write a header & populate the first line of survey data
            csvfile.seek(0)
            first_char = csvfile.read(1)

        if not first_char:
            with open('survey.csv', 'w') as csvfile:
                # set header names for csv file
                fieldnames = ['first_name', 'gender', 'pizza_preference', 'pizza_frequency']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

                # write header names
                writer.writeheader()

                # write survey data
                writer.writerow({'first_name': first_name, 'gender': gender,
                                 'pizza_preference': pizza_preference, 'pizza_frequency': pizza_frequency})
        else:
            with open('survey.csv', 'a') as csvfile:
                # set header names for csv file
                fieldnames = ['first_name', 'gender', 'pizza_preference', 'pizza_frequency']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

                # append survey data
                writer.writerow({'first_name': first_name, 'gender': gender,
                                 'pizza_preference': pizza_preference, 'pizza_frequency': pizza_frequency})

        return redirect("/sheet")


@app.route("/sheet", methods=["GET"])
def get_sheet():
    with open('survey.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        table_data = list(reader)
    return render_template("table.html", table_data=table_data)