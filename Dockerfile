FROM python:3.9.7
EXPOSE 5000
COPY . /app
WORKDIR /app
RUN /usr/local/bin/python -m pip install --upgrade pip
RUN pip install quickfix-1.15.1-cp39-cp39-linux_x86_64.whl
RUN pip install -r requirements.txt --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host=files.pythonhosted.org
ENV FLASK_APP /app/app.py
CMD ["flask", "run", "--host", "0.0.0.0"]
