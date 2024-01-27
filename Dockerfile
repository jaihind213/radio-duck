# Use an official Python runtime as a parent image
ARG DOCKER_DUCKX_IMAGE_VERSION
FROM jaihind213/duckdbx:${DOCKER_DUCKX_IMAGE_VERSION}

USER 0
RUN mkdir -p /radio-duck
WORKDIR /radio-duck

# Copy the current directory contents into the container at /app
COPY . /radio-duck/
COPY default.ini /radio-duck/default.ini
# Install any needed packages specified in requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt

RUN --mount=type=secret,id=duck_sekrets
#RUN rm -f /etc/ssl/certs/ca-bundle.crt && apt update && apt install --reinstall ca-certificates && update-ca-certificates
RUN echo "base docker image version: $DOCKER_DUCKX_IMAGE_VERSION" >> base_docker_image_version

#RUN echo http://dl-cdn.alpinelinux.org/alpine/edge/main >> /etc/apk/repositories
#RUN apk update && apk add --no-cache zlib-dev==1.3-r2  #->for docker CRITICAL CVE-2023-45853
# Make port 8000 available to the world outside this container
EXPOSE 8000

# Run server.py when the container launches
CMD ["python3", "/radio-duck/server.py"]

VOLUME /radio-duck/pond