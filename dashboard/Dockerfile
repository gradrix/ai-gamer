# Use the official Python base image for Python 3.11
FROM python:3.11

# Set the working directory inside the container
WORKDIR /app

# Install system dependencies for matplotlib
RUN apt-get update && apt-get install -y \
    build-essential \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements.txt file to the container
COPY ./dashboard/requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the dashboard server
COPY ./dashboard_server.py .

# Expose the dashboard port
EXPOSE 5000

# Specify the command to run your application
CMD [ "python", "dashboard_server.py" ]