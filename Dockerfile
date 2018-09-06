#FROM python:2-alpine

#use gunicorn
#RUN pip install -r requirements.txt

#use flask
#RUN pip install flask
#COPY . /usr/src/app/
#WORKDIR /usr/src/app/

# EXPOSE 5000
# ENTRYPOINT ["/usr/local/bin/gunicorn"]

#CMD ["-w","1","-b","0.0.0.0:5000","--threads","1","app:app","--access-logfile","/dev/stdout","--error-logfile","/dev/stdout"]

FROM python:3.5
ADD . /code
WORKDIR /code
RUN pip install -r requirements.txt

CMD ["python", "app.py"]
