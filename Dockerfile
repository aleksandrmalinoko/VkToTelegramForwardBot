FROM python:3.7
COPY .  /Bot_home
WORKDIR /Bot_home
RUN pip install -r requirements.txt
CMD ["python", "app.py"]