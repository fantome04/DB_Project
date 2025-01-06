Install the dependencies from the requirements.txt file.

In 'config.py' change the following lines accordingly:

    DB_NAME = "db_name"
    DB_USER = "username"
    DB_PASSWORD = "password"
    DB_HOST = "localhost"
    DB_PORT = "port"

Run `python init_db.py`

Run `alembic upgrade head`

To run the server run command `uvicorn app.main:app --reload`

In 'fill_db.py' in the main you can change the n(number of data) to whatever number you want.

You can go to the UI by this link `http://127.0.0.1:8000/frontend/index.html`