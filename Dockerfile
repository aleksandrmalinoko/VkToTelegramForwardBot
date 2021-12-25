FROM python:3.7
COPY .  /Bot_home
WORKDIR /Bot_home
RUN pip install -r requirements.txt
EXPOSE  8000
CMD ["python", "app.py"]