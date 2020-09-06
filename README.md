# Bangazon Django Backend API

Bangazon is a personal E-Commerce app where users can buy and sell products. Bangazon comes in two parts: a front end React app, and a backend Django REST API. Visit https://github.com/nss-cohort-40/bangazon-ecommerce-client-crunchyfrogs for the front end of this app.

## Technology used

- React framework 
- Django REST framework
- Cloudinary API

## Features

- Users can sell a product 
    - Users can specify if local delivery is available
    - Users can upload a product picture
    - Users can specify the category of a product
    - Users can delete a product after creating a listing
- Users can search for products 
- Users can view products in specific product categories
- Users can view specific details of a product
- Users can view a list of the most recent products 
- Users can view and edit their account data and payment methods
- Users can view their order history
- Users can put products in their shopping cart and remove them
- Users can complete an order by entering a payment type 

## Installation instructions

1. Clone down the repo and `cd` into it
1. Set up your virtual environment:
    `python -m venv bangazonEnv`
1. Activate virtual environment:
    `source ./bangazonEnv/bin/activate`
1. Install dependencies:
    `pip install -r requirements.txt`
1. Run migrations:
    `python manage.py migrate`
1. `python manage.py runserver`
1. Create your application for your API, named `ecommerceapi`

## Bangazon ERD
[Bangazon eCommerce ERD](https://dbdiagram.io/d/5eb4d6d639d18f5553fedfb5)
