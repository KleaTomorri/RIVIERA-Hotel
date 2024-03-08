from flask_app import app
from flask import render_template, redirect, request, session, url_for, flash

from flask_app.models.table import Reservation

@app.route('/book_table', methods=['GET', 'POST'])
def book_table():
    if request.method == 'POST':
        data = {
            'date': request.form['date'],
            'time': request.form['time'],
            'firstName': request.form['firstName'],
            'lastName': request.form['lastName'],
            'emaiL': request.form['emaiL']  # Changed from emaiL to email
        }
        Reservation.create_table(data)
        flash("Reservation created successfully!", "success")
        return redirect(request.referrer)
    return render_template('table.html')





@app.route('/reservation_success')
def reservation_success():
    return render_template('reservation_success.html')