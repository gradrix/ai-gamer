# Use the official Python base image for Python 3.11
FROM python:3.11

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements.txt file to the container
COPY ./game_server/requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code to the container
COPY ./game_server ./game_server
COPY ./common ./common

# Expose the gRPC server's port
EXPOSE 8080

# Specify the command to run your application
CMD [ "python", "game_server/start-server.py" ]