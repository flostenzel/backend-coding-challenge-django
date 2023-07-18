
# Backend Coding Challenge

This is a django backend for a note-taking app.

## Feature Overview

    1. Users can add, delete and modify their notes
    2. Users can see a list of all their notes
    3. Users can filter their notes via tags
    4. Users must be logged in, in order to view/add/delete/etc. their notes
    5. Search contents of notes with keywords
    6. Notes can be either public or private: Public notes can be viewed without authentication, however they cannot be modified
    7. User management API to create new users

## Getting Started

To get started with the project, follow these steps:

    1. Clone the project repository to your local machine.
    2. Create a virtual environment in python 3.11 for the project and activate it.
    3. Install the required packages by running the command `pip install -r requirements.txt`.
    4. Go to the main app folder `cd app`
    5. Set up the database by running the command `python manage.py migrate`.
    6. Start server: `python manage.py runserver`
    7. Run tests with `python manage.py test`

## API Reference

While server is running go to `http://localhost:8000/docs/` or `http://localhost:8000/playground/`

## TODO

    1. Get back to PM to make sure how search features are supposed to work (Union of tags vs. intersection of tags)
    2. Add docstrings/comments to all views, models, functions ..
    3. Read and implement coding style of thermondo (eg. usage query params vs filter_backends)
    4. Add test_model, test_serializer, ..
    5. Introduce strict typing
