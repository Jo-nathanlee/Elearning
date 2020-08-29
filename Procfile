web: gunicorn --pythonpath elearning elearning.wsgi
worker: daphne elearning.asgi:application --port $PORT --bind 0.0.0.0