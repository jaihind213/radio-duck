# Use an official Python runtime as a parent image
FROM python:3.10-alpine

USER 0
RUN mkdir -p /radio-duck
WORKDIR /radio-duck

# Copy the current directory contents into the container at /app
COPY . /radio-duck/
COPY default.ini /radio-duck/default.ini

# Install any needed packages specified in requirements.txt
RUN apk add --virtual .make-deps musl-dev g++ libpq-dev libffi-dev && pip install --no-cache-dir -r requirements.txt && apk del g++

# Make port 80 available to the world outside this container
EXPOSE 8000

# Run server.py when the container launches
CMD ["python", "/radio-duck/server.py"]

VOLUME /radio-duck/pond