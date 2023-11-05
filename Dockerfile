# Use an official Python runtime as a parent image
FROM python:3.10-alpine

USER 0
RUN mkdir -p /radio-duck
WORKDIR /radio-duck

# Copy the current directory contents into the container at /app
COPY . /radio-duck/
COPY default.ini /radio-duck/default.ini
# Install any needed packages specified in requirements.txt
#RUN apk add --no-cache --virtual .make-deps musl-dev g++ libpq-dev libffi-dev && pip install --no-cache-dir -r requirements.txt
#reduce size by removing g++ after u are done.
#RUN apk update && apk add --no-cache --virtual .compiler_dep g++ && apk add --no-cache musl-dev libpq-dev libffi-dev  && pip install --no-cache-dir -r requirements.txt && apk del .compiler_dep
RUN apk update && apk add --no-cache --virtual .compiler_dep g++ && apk add --no-cache musl-dev libpq-dev libffi-dev  && pip install --no-cache-dir -r requirements.txt && apk del .compiler_dep

#RUN echo http://dl-cdn.alpinelinux.org/alpine/edge/main >> /etc/apk/repositories
#RUN apk update && apk add --no-cache zlib-dev==1.3-r2  #->for docker CRITICAL CVE-2023-45853
# Make port 8000 available to the world outside this container
EXPOSE 8000

# Run server.py when the container launches
CMD ["python", "/radio-duck/server.py"]

VOLUME /radio-duck/pond