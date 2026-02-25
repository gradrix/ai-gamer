# Use the official Python base image for Python 3.11
FROM python:3.11

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements.txt file to the container
COPY ./random_client/requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code to the container
COPY ./random_client ./random_client
COPY ./common ./common

# Expose the gRPC server's port
EXPOSE 8080

# Create a startup script to handle environment variable expansion
RUN echo '#!/bin/bash\npython random_client/start-random-client.py "${PLAYER_NAME:-RandomBot}"' > /app/start.sh && chmod +x /app/start.sh

# Specify the command to run your application
CMD ["/app/start.sh"]