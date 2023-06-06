FROM registry.redhat.io/ubi9/python-39@sha256:40a58935b9c22664927b22bf256f53a3d744ddb7316f3af18061099e199526ee
EXPOSE 5000
COPY . /app
WORKDIR /app
#RUN /usr/local/bin/python -m pip install --upgrade pip
#RUN pip install quickfix-1.15.1-cp39-cp39-linux_x86_64.whl
#RUN echo "deb http://ftp.debian.org/debian sid main" >> /etc/apt/sources.list
#RUN apt-get update
#RUN apt-get -t sid -y install libc6 libc6-dev libc6-dbg
#RUN apt install -y gcc
RUN pip install -r requirements.txt --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host=files.pythonhosted.org
ENV FLASK_APP /app/app.py
#RUN flask db migrate
#RUN flask db upgrade
CMD ["flask", "run", "--host", "0.0.0.0"]

