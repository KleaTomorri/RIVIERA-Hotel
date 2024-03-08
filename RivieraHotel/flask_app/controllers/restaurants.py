from flask_app import app
from flask import render_template, redirect, request, session, url_for, flash
from flask import request
from werkzeug.utils import secure_filename
import os
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
from flask_app.models.user import User

from flask_app.models.restaurant import Restaurant

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from flask import send_file

from datetime import datetime


@app.route('/restaurant')
def restoraunt():
  
    restaurants=Restaurant.get_all()
    user = None   
    
    if 'user_id' in session:
        user_id = session['user_id']
        data = {
            'id': user_id
        }
        user = User.get_user_by_id(data)
    return render_template('restaurant.html', restaurants=restaurants, user=user)





# routes.py


@app.route('/download_menu/<string:restaurant_name>')
def download_menu(restaurant_name):
    # Generate the PDF file for the menu based on the restaurant name
    # Replace the following line with your code to generate the PDF
    # For demonstration purposes, a placeholder function is used here
    pdf_file_path = generate_menu_pdf(restaurant_name)

    # Send the PDF file as a downloadable attachment
    return send_file(pdf_file_path, as_attachment=True)


# Import the necessary modules


def generate_menu_pdf(restaurant_name):
    # Replace this dictionary with your actual menu data
    menu_data = {
        'restaurant1': ['Item 1', 'Item 2', 'Item 3'],
        'restaurant2': ['Item A', 'Item B', 'Item C'],
        # Add more restaurants and their menu items as needed
    }

    # Retrieve menu items for the specified restaurant name
    menu_items = menu_data.get(restaurant_name, [])

    # Create a PDF canvas
    pdf_file_path = f"menu_{restaurant_name}.pdf"
    c = canvas.Canvas(pdf_file_path, pagesize=letter)

    # Add the menu items to the PDF
    y = 700  # Initial Y coordinate for the first menu item
    for item in menu_items:
        c.drawString(100, y, item)
        y -= 20  # Adjust Y coordinate for the next menu item

    # Save the PDF file
    c.save()

    return pdf_file_path


#BOOK TABLE



# Assuming your Reservation class and other imports are correctly defined...


# @app.route('/book_table', methods=['GET'])
# def book_table():
#     if request.method == 'GET':
#         return render_template('table.html')
        
#     if request.method == 'POST':
#         try:
#             date = request.form['date']
#             time = request.form['time']
#             first_name = request.form['first_name']
#             last_name = request.form['last_name']
#             email = request.form['email']
#             created_at = datetime.now()
#             reservation_data = {
#                 'date': date,
#                 'time': time,
#                 'first_name': first_name,
#                 'last_name': last_name,
#                 'email': email,
#                 'created_at': created_at  # Include the current timestamp
#             }

#             Reservation.create(reservation_data)
#             return redirect(url_for('reservation_success'))
#         except Exception as e:
#             print("Error:", e)
#             flash("An error occurred while processing your reservation. Please try again.")
#             return redirect(url_for('book_table'))


# @app.route('/book_table', methods=['POST'])
# def sent_message():
  
#     data={
#             'date': request.form['date'],
#             'time': request.form['time'],
#             'first_name': request.form['first_name'],
#             'last_name': request.form['last_name'],
#             'email': request.form['email'],
#             'created_at': datetime.now() 
#         }
#     Reservation.create(data)
#     return redirect(request.referrer)




















@app.route('/about')
def about():
    return render_template('about.html')