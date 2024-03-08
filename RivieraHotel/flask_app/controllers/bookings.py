from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask import request
from flask import Flask, render_template, request, redirect, url_for

from werkzeug.utils import secure_filename
import os
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
from flask_app.models.user import User
from flask_app.models.category import Category
from flask_app.models.category import Service
from flask_app.models.review import Review
from flask_app.models.booking import Booking



@app.route('/submit_booking', methods=['POST'])
def submit_booking():
    if request.method == 'POST':
        checkin = request.form.get('checkin')
        checkout = request.form.get('checkout')

        # Check room availability by querying the database
        available_rooms = Booking.check_availability(checkin, checkout)

        if available_rooms:
            # Rooms are available, redirect to booking details page
            return redirect(url_for('booking_details', checkin=checkin, checkout=checkout))
        else:
            # No rooms available, render appropriate template
            return render_template('NoRooms.html')
        
        
        


@app.route('/booking_details', methods=['GET', 'POST'])
def booking_details():
    if request.method == 'GET':
        # Handle GET request to display booking details form
        checkin = request.args.get('checkin')
        checkout = request.args.get('checkout')
        
        # Perform any additional logic here, such as retrieving booking details from the database
        
        # Pass the check-in and check-out dates to the template
        return render_template('Book.html', checkin=checkin, checkout=checkout)
    elif request.method == 'POST':
        # Handle POST request to process form submission
        room_category_id = request.form.get('room_category_id')
        return redirect(url_for('booking_details_by_id', room_category_id=room_category_id))





# @app.route('/submit_booking', methods=['POST'])
# def submit_booking():
#     if request.method == 'POST':
#         checkin = request.form.get('checkin')
#         checkout = request.form.get('checkout')

#         # Check room availability by querying the database
#         available_rooms = Booking.check_availability(checkin, checkout)

#         if available_rooms:
#             # Rooms are available, redirect to booking details page
#             return redirect(url_for('booking_details', checkin=checkin, checkout=checkout))
#         else:
#             # No rooms available, render appropriate template
#             return render_template('NoRooms.html')

# @app.route('/booking_details', methods=['GET'])
# def display_booking_details():
#     # Handle GET request to display booking details form
#     checkin = request.args.get('checkin')
#     checkout = request.args.get('checkout')

#     # Perform any additional logic here, such as retrieving booking details from the database

#     # Pass the check-in and check-out dates to the template
#     return render_template('Book.html', checkin=checkin, checkout=checkout)

# @app.route('/process_booking_details', methods=['POST'])
# def process_booking_details():
#     # Handle POST request to process form submission
#     room_category_id = request.form.get('room_category_id')
#     return redirect(url_for('booking_details_by_id', room_category_id=room_category_id))


# @app.route('/booking_details/<int:room_category_id>')
# def booking_details_by_id(room_category_id):
#     room_category = Category.get_room_category_by_id(room_category_id)
#     return render_template('booking_details.html', room_category=room_category)

# @app.route('/booking', methods=['GET'])
# def display_booking_form():
#     # Retrieve categories and their associated rooms from the database
#     categories = Category.get_all_categories_with_rooms()
#     return render_template('booking.html', categories=categories)

# @app.route('/confirmation', methods=['POST'])
# def confirm_booking():
#     # Handle form submission and calculate total price
#     selected_room = request.form.get('selected_room')
#     selected_extras = request.form.getlist('selected_extras')
#     total_price = calculate_total_price(selected_room, selected_extras)
#     return render_template('confirmation.html', total_price=total_price)

# def calculate_total_price(selected_room, selected_extras):
#     # Calculate total price based on selected room and extras
#     pass








