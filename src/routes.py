import sys
from src import app
from flask_toastr import Toastr
from .static.raffle_gen import driver
from flask import render_template, request, flash, redirect, url_for, session

toastr = Toastr(app)
app.secret_key = "extremely_secure"


@app.route("/", methods=["GET", "POST"])
def form():        
    if request.method == "POST":
        input_name = request.form.get("input-name")
        num_spots = request.form.get("num-spots")
        called_spots = request.form.get("called-spots")
        range_called_spots = request.form.get("range-called-spots")

        # need to set default args and catch exception(s) if empty
        session["driver_results"] = driver(input_name, total_num_spots=int(num_spots),
                                           called_spots=int(called_spots)
                                           )

        flash("Request submitted successfully", "success")
        return redirect(url_for("results"), code=307)

    return render_template("index.html")


@app.route("/results", methods=["GET", "POST"])
def results():   
    driver_results = session.get("driver_results")
    return render_template("index.html", raw_values=driver_results)


@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html")


@app.errorhandler(500)
def internal_error(error):
    return render_template("500.html")
