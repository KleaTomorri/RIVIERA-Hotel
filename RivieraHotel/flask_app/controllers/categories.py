from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask import request
from werkzeug.utils import secure_filename
import os
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
from flask_app.models.user import User
from flask_app.models.category import Category
from flask_app.models.category import Service
from flask_app.models.review import Review




UPLOAD_FOLDER = 'flask_app/static/categoryimages'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS




@app.route('/')
def home():
    categories = Category.get_all()
    reviews=Review.get_all()
    services=Service.get_all()
    user = None   
    
    if 'user_id' in session:
        user_id = session['user_id']
        data = {
            'id': user_id
        }
        user = User.get_user_by_id(data)
    return render_template('index5.html', categories=categories, user=user, reviews=reviews, services=services)


@app.route('/reviews/new', methods=['GET', 'POST'])
def add_reviews():
    if request.method == 'GET':
        if 'user_id' not in session:
            return redirect('/')
        return render_template('addReview.html')
    
    elif request.method == 'POST':
        if 'user_id' not in session:
            return redirect('/')
        comment = request.form.get('comment')
        data = {
            'comment': comment,
            'user_id': session['user_id']
        }
        Review.create(data)
        flash('Review added successfully', 'success')
        return redirect('/')  # Redirect to the same page to clear the form

            

@app.route('/delete/comment/<int:id>')
def deleteComment(id):
    if 'user_id' not in session:
        return redirect('/login')

    data = {'id': id}
    comment = Review.get_comment_by_id(data)

    if comment and comment['user_id'] == session['user_id']:
        Review.delete_comment(data)

    return redirect(request.referrer)



@app.route('/categories/new')
def addEvent():
    if 'user_id' not in session:
        return redirect('/')
    
    user_id = session['user_id']
    data = {
        'id': user_id
    }
    user = User.get_user_by_id(data)
    
    if user and user['role'] == 'admin':
        return render_template('addCategory.html')
    return redirect('/')


@app.route('/categories/new', methods=['GET', 'POST'])
def add_events():
    if request.method == 'GET':
        if 'user_id' not in session:
            return redirect('/')
        user = User.get_user_by_id({'id': session['user_id']})
        if user['role'] == 'admin':
            return render_template('addCategory.html')
        return redirect('/')
    elif request.method == 'POST':
        if 'user_id' not in session:
            return redirect('/')
        user = User.get_user_by_id({'id': session['user_id']})
        if user['role'] == 'admin':
            name = request.form.get('name')
            description = request.form.get('description')
            price = request.form.get('price')
            if 'image_path' in request.files:
                file = request.files['image_path']
                if file.filename != '' and allowed_file(file.filename):
                    image_path = secure_filename(file.filename)
                    file.save(os.path.join(UPLOAD_FOLDER, image_path))
                    data = {
                        'name': name,
                        'description': description,
                        'price': price,
                        'image_path': image_path,
                        'user_id': session['user_id']
                        
                    }
                    try:
                        result = Category.create(data)
                        if result:
                            flash('Cetegory added successfully!', 'success')
                        else:
                            flash('Failed to add event. Please try again later.', 'error')
                    except Exception as e:
                        flash(f'Error occurred: {str(e)}', 'error')
                        app.logger.error(f'Error adding event: {str(e)}')
                    return redirect('/')
                else:
                    flash('Invalid file format', 'error')
                    return redirect(request.url)
            else:
                flash('No file part', 'error')
                return redirect(request.url)
        return redirect('/')


# 

@app.route('/category/<int:id>')
def view_category(id):
    category = Category.get_categories_by_id({'id': id})
    user = None
    if 'user_id' in session:
        user = User.get_user_by_id({'id': session['user_id']})

    # Retrieve features for the category
    features = Category.get_features_by_category_id(id)

    return render_template('room-details.html', category=category, user=user, features=features)


@app.route('/category/edit/<int:id>')
def edit_category(id):
    if 'user_id' not in session:
        return redirect('/')
    data={
        'id':id
    }
    category= Category.get_categories_by_id(data)
    if category and category['user_id']== session['user_id']:
        return render_template('editCategory.html', category=category)
    return redirect('/category/<int:id>')




@app.route('/category/update/<int:id>', methods=['POST'])
def update_category(id):
    if 'user_id' not in session:
        return redirect('/')

    category = Category.get_categories_by_id({'id': id})
    if category and category['user_id'] == session['user_id']:
        name = request.form['name']
        description = request.form['description']
        price = request.form['price']
        image_path = category['image_path']  # Get the existing image path

        # Handle file upload for the category image
        if 'photo' in request.files:
            file = request.files['photo']
            if file.filename != '' and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                image_path = filename  # Update image path if a new file is uploaded
            else:
                flash('Invalid file format', 'error')
                return redirect(request.url)

        # Update the category in the database with the new data including image_path
        Category.update({'id': id, 'name': name, 'description': description, 'price': price, 'image_path': image_path})
        return redirect('/category/' + str(id))

    return redirect('/')











@app.route('/category/delete/<int:id>')
def delete_event(id):
    if 'user_id' not in session:
        return redirect('/')
    data={
        'id': id
    }
    category= Category.get_categories_by_id(data)
    if category['user_id']== session['user_id']:
        Category.deleteCategory(data)
    return redirect('/')













#FEATURES


# @app.route('/features/new/<int:id>', methods=['GET', 'POST'])
# def add_feature(id):
#     data = {
#         'id': id
#     }
#     if request.method == 'GET':
#         user = User.get_user_by_id(session['user_id'])
#         if 'user_id' not in session:
#             return redirect('/')

#         category = Category.get_categories_by_id(data)
#         if not category:
#             flash('Invalid event ID', 'error')
#             return redirect('/')
        
#         return render_template('addFeatures.html', category=category, user=user)
    
#     elif request.method == 'POST':
#         user = User.get_user_by_id(session['user_id'])
#         if 'user_id' not in session:
#             return redirect('/')
        
        
#         name = request.form['name']
        
        
#         category = Category.get_categories_by_id(data)
#         if not category:
#             flash('Invalid event ID', 'error')
#             return redirect(request.referrer)
        
        
#         data1 = {
#             'name': name,
            
#             'category_id': id,
#             'user_id': session['user_id']
#         }
        
#         Category.insert_features(data1)
        
#         flash('Feature added successfully!', 'success')
#         return redirect('/')
    
    
@app.route('/features/new/<int:id>', methods=['GET', 'POST'])
def add_feature(id):
    if 'user_id' not in session:
        return redirect('/login')

    category = Category.get_categories_by_id({'id': id})
    if not category:
        flash('Invalid category ID', 'error')
        return redirect('/')

    if request.method == 'GET':
        user = User.get_user_by_id(session['user_id'])
        features = Category.get_features_by_category_id(id)
        return render_template('addFeatures.html', category=category, user=user, features=features)

    elif request.method == 'POST':
        user = User.get_user_by_id(session['user_id'])
        if 'user_id' not in session:
            return redirect('/')

        name = request.form.get('name')
        if not name:
            flash('Name is required', 'error')
            return redirect(request.url)

        data = {
            'name': name,
            'category_id': id,
            'user_id': session['user_id']
        }

        Category.insert_features(data)
        flash('Feature added successfully!', 'success')

        # Redirect to the room details page after adding a feature
        return redirect('/')

    # Return a default response in case the request method is not GET or POST
    return redirect('/')


   

    




#SERVICES

@app.route('/services/new')
def addService():
    if 'user_id' not in session:
        return redirect('/')
    
    user_id = session['user_id']
    data = {
        'id': user_id
    }
    user = User.get_user_by_id(data)
    
    if user and user['role'] == 'admin':
        return render_template('addService.html')
    return redirect('/')


@app.route('/services/new', methods=['GET', 'POST'])
def add_services():
    if request.method == 'GET':
        if 'user_id' not in session:
            return redirect('/')
        user = User.get_user_by_id({'id': session['user_id']})
        if user['role'] == 'admin':
            return render_template('addService.html')
        return redirect('/')
    elif request.method == 'POST':
        if 'user_id' not in session:
            return redirect('/')
        user = User.get_user_by_id({'id': session['user_id']})
        if user['role'] == 'admin':
            name = request.form.get('name')
            description = request.form.get('description')
           
            if 'services_photo' in request.files:
                file = request.files['services_photo']
                if file.filename != '' and allowed_file(file.filename):
                    services_photo = secure_filename(file.filename)
                    file.save(os.path.join(UPLOAD_FOLDER, services_photo))
                    data = {
                        'name': name,
                        'description': description,
                        'services_photo': services_photo,
                        'user_id': session['user_id']
                        
                    }
                    try:
                        result = Service.create(data)
                        if result:
                            flash('Cetegory added successfully!', 'success')
                        else:
                            flash('Failed to add event. Please try again later.', 'error')
                    except Exception as e:
                        flash(f'Error occurred: {str(e)}', 'error')
                        app.logger.error(f'Error adding event: {str(e)}')
                    return redirect('/')
                else:
                    flash('Invalid file format', 'error')
                    return redirect(request.url)
            else:
                flash('No file part', 'error')
                return redirect(request.url)
        return redirect('/')





