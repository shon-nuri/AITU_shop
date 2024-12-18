﻿# AITU_shop
AITU Merchandise Webstore
Overview

AITU Merchandise Webstore is a full-stack e-commerce platform built with Django, enhanced by Bootstrap for responsive design, and powered by jQuery and Owl Carousel for dynamic interactivity. The platform allows users to explore, review, and purchase branded AITU merchandise with ease.
Features
Frontend

    Responsive Design: Built using Bootstrap 5 for seamless user experience across devices.
    Dynamic Components:
        Owl Carousel: Showcases featured products and testimonials with smooth transitions.
        jQuery: Adds interactivity for real-time cart updates and modal pop-ups.
    Clean and Modern UI: Includes filters for product categories and quick navigation.

Authentication

    User Login/Registration:
        Standard login and registration system.
        Secure password hashing for user credentials.
    Google Sign-Up:
        Integrated Google OAuth for a fast and secure signup/login experience.

Shopping Cart

    Fully updatable cart using AJAX:
        Add/remove items.
        Increase/decrease product quantity dynamically.
    Cart persists across sessions using cookies for unauthenticated users.

Product Management

    CRUD Features:
        Admins can create, update, delete, and view products through a user-friendly admin interface.
        Product images and details are manageable directly via the Django admin panel.

Payment Integration

    Stripe Payment Gateway:
        Secure and seamless payment processing for credit and debit cards.
        Handles order confirmation and transaction processing.

Reviews and Ratings

    Users can leave product reviews and ratings.
    Average rating displayed on product detail pages.

Shipping Logic

    Automatically determines whether shipping is required based on product type.
    Users can input their shipping address during checkout.

Technologies Used
Backend

    Django Framework: Handles server-side logic, database interactions, and authentication.
    SQLite: Default database for development; easily replaceable with PostgreSQL or MySQL for production.

Frontend

    Bootstrap 5: Responsive design framework for clean UI.
    jQuery: Adds dynamic functionality to forms and cart updates.
    Owl Carousel: Creates carousels for products and testimonials.

Payment

    Stripe API: For secure and reliable payment handling.
