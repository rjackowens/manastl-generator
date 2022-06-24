FROM python:3.10

COPY requirements.txt requirements.txt
RUN pip3 install --trusted-host files.pythonhosted.org \
    --trusted-host pypi.org --trusted-host pypi.python.org -r requirements.txt

COPY . .

EXPOSE 8080:8080

RUN export FLASK_APP=src/__init__.py

CMD [ "python3", "run.py"]
