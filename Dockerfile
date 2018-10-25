# for test
FROM ubuntu:16.04
LABEL maintainer="Azure App Service Container Images <appsvc-images@microsoft.com>"
RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential
#lines customer removed to resolve the issue
RUN apt-get install -y build-essential cmake pkg-config
RUN apt-get install libjpeg8-dev libtiff5-dev libjasper-dev libpng12-dev
RUN apt-get install libavcodec-dev libavformat-dev libswscale-dev libv4l-dev
RUN apt-get install libxvidcore-dev libx264-dev
RUN apt-get install libgtk-3-dev
RUN apt-get install libatlas-base-dev gfortran
RUN apt-get install python2.7-dev python3.5-dev
#lines customer added end
COPY . /app
WORKDIR /app
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
EXPOSE 5000
CMD ["runserver.py"]
