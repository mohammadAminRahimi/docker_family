FROM python:3.8


RUN apt-get update
RUN apt-get install -y --no-install-recommends default-mysql-client


WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install -r requirements.txt


#RUN pip install django-probes
#RUN python project/manage.py wait_for_database
#RUN python project/manage.py migrate
RUN pip install mysql-connector-python==8.0.26

COPY  . .
#EXPOSE 8000
CMD ["python", "project/manage.py", "wait_for_database"]
