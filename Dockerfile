FROM ubuntu:22.04
LABEL maintainer="jaihind213@gmail.com"

ARG PYTHON_VERSION=3.10
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8

RUN useradd -m -d /home/radio-duck radio-duck
WORKDIR /home/radio-duck
RUN mkdir "pond"

RUN apt update && apt autoclean && apt install -y software-properties-common && apt update && add-apt-repository ppa:apt-fast/stable -y && add-apt-repository ppa:deadsnakes/ppa && apt update && apt install -y apt-fast
RUN apt-fast -y install linux-libc-dev libssl-dev
#RUN apt-fast -y install gcc git g++ libblis64-3-pthread
RUN apt-fast -y install libblis64-3-pthread

RUN apt-fast update && apt-fast install -y python${PYTHON_VERSION}
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python${PYTHON_VERSION} 1

#for psutil need to do python3.10-dev u need it later when u do '' pip3 install -r requirements-dev.txt''
RUN apt-fast -y install python${PYTHON_VERSION}-dev
RUN apt-fast -y install curl && curl -sS https://bootstrap.pypa.io/get-pip.py | python3 && apt-fast -y remove curl

# Copy the current directory contents into the container at /app
COPY *.py /home/radio-duck
COPY requirements.txt /home/radio-duck
COPY default.ini /home/radio-duck/default.ini
# Install any needed packages specified in requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt

RUN --mount=type=secret,id=duck_sekrets
#RUN rm -f /etc/ssl/certs/ca-bundle.crt && apt update && apt install --reinstall ca-certificates && update-ca-certificates

RUN mkdir "/quack"
RUN echo "import duckdb; duckdb.query('install httpfs; load httpfs; install azure; load azure;');" >> /quack/test.py && echo "" >> /quack/test.py
RUN cd /quack && python3 test.py && cd -

#RUN echo http://dl-cdn.alpinelinux.org/alpine/edge/main >> /etc/apk/repositories
#RUN apk update && apk add --no-cache zlib-dev==1.3-r2  #->for docker CRITICAL CVE-2023-45853
# Make port 8000 available to the world outside this container
EXPOSE 8000

# Run server.py when the container launches
CMD ["python3", "/home/radio-duck/server.py"]

VOLUME /home/radio-duck/pond