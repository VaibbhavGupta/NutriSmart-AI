# Use the official Python lightweight image.
FROM python:3.11-slim

# Allow statements and log messages to immediately appear in the Cloud Run logs
ENV PYTHONUNBUFFERED True

# Set the working directory to /app
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy local code to the container image.
COPY . ./

# Run the web service on container startup using gunicorn webserver.
# The `app:app` refers to the module `app.py` and the Flask instance `app`.
# Cloud Run sets the PORT environment variable. If not set, it defaults to 8080.
ENV PORT=8080
EXPOSE $PORT

CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 app:app
