FROM python:3.9
COPY requirements.txt /Bot_home/requirements.txt
WORKDIR /Bot_home
RUN pip install -r requirements.txt
COPY .  /Bot_home
CMD ["python", "app.py"]