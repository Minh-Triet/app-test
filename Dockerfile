FROM python:3.9.7
EXPOSE 5000
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host=files.pythonhosted.org
ENV FLASK_APP /app/app.py
RUN flask db init
RUN flask db migrate
RUN flask db upgrade
CMD ["flask", "run", "--host", "0.0.0.0"]
