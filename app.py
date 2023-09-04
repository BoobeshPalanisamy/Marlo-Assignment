from flask_paginate import Pagination
from bson import ObjectId
from flask import Flask, jsonify, redirect, render_template, request
from flask_pymongo import PyMongo
import pandas as pd
from flask_paginate import Pagination

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb+srv://pmboobesh:a5pIqiYiNwRwnGUB@cluster0.hbtw8lt.mongodb.net/test"
mongo = PyMongo(app)

# Print a message when the MongoDB connection is established
with app.app_context():
    print("MongoDB connected")


@app.route('/')
@app.route('/home')
def home():
    return render_template('Home.html')


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/product')
def product():
    return render_template('product.html')


@app.route('/uploadCSV')
def uploadCSV():
    return render_template('uploadCSV.html')


@app.route('/productsrev')
def display_products():
    products = mongo.db.products.find()
    return render_template('productsrev.html', products=products)


# Registration API


@app.route('/register', methods=['POST'])
def register():
    user_data = request.get_json()

    if user_data:
        first_name = user_data.get('first_name')
        last_name = user_data.get('last_name')
        password = user_data.get('password')

        if first_name and last_name and password:
            user_doc = {
                'first_name': first_name,
                'last_name': last_name,
                'password': password
            }

            mongo.db.users.insert_one(user_doc)

            return jsonify({'message': 'User registered successfully'}), 201
        else:
            return jsonify({'error': 'Missing required fields'}), 400
    else:
        return jsonify({'error': 'No data provided in the request'}), 400


# Login API
@app.route('/loginAPI', methods=['POST'])
def loginAPI():
    login_data = request.get_json()

    if login_data:
        username = login_data.get('username')
        password = login_data.get('password')

        if username and password:
            user = mongo.db.users.find_one(
                {'first_name': username, 'password': password})

            if user:
                return jsonify({'message': 'Login successful'}), 200
            else:
                return jsonify({'error': 'Invalid username or password'}), 401
        else:
            return jsonify({'error': 'Missing required fields'}), 400
    else:
        return jsonify({'error': 'No data provided in the request'}), 400


# ProductUpload API(CSV upload)
@app.route('/upload', methods=['POST'])
def upload_csv():
    if 'csv_file' not in request.files:
        return redirect(request.url)

    file = request.files['csv_file']

    if file.filename == '':
        return redirect(request.url)

    if file:
        df = pd.read_csv(file)

        data = df.to_dict(orient='records')

        mongo.db.products.insert_many(data)

        return "CSV file uploaded and data saved to MongoDB successfully."

# Products Review and Rating API


@app.route('/submit_review', methods=['POST'])
def submit_review():
    data = request.get_json()
    product_id = data.get('productId')
    rating = data.get('rating')
    review_text = data.get('review')

    try:
        result = mongo.db.products.update_one(
            {'_id': ObjectId(product_id)},
            {'$push': {'reviews': {'rating': rating, 'review_text': review_text}}}
        )
        if result.modified_count == 1:
            return jsonify({'success': True})
        else:
            return jsonify({'success': False, 'message': 'Failed to submit review.'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

# Products View Pagination API


@app.route('/products_by_rating', methods=['GET'])
def products_by_rating():
    products_collection = mongo.db.products
    try:
        # Get query parameters for pagination
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 5))

        # Calculate skip value based on page and per_page
        skip = (page - 1) * per_page

        # Query the database with pagination
        products = list(products_collection.find(
            {}).skip(skip).limit(per_page))

        for product in products:
            reviews = product.get('reviews', [])
            if reviews:
                total_rating = 0
                for review in reviews:
                    try:
                        rating = float(review['rating'])
                        total_rating += rating
                    except (ValueError, TypeError):
                        pass

                if total_rating > 0:
                    average_rating = total_rating / len(reviews)
                else:
                    average_rating = 0
            else:
                average_rating = 0
            product['average_rating'] = average_rating

        # Count the total number of products (needed for pagination)
        total_products = products_collection.count_documents({})

        # Create a Pagination object
        pagination = Pagination(
            page=page, per_page=per_page, total=total_products)

        sorted_products = sorted(
            products, key=lambda x: x['average_rating'], reverse=True)

        return render_template('viewProduct.html', products=sorted_products, pagination=pagination)

    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
