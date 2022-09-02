FROM ubuntu



COPY app2.py .
COPY config.yaml .

RUN apt-get update -y
RUN apt install -y python3
RUN apt-get install -y python3-pip
RUN pip install gunicorn
RUN pip install flask
RUN pip install pandas
RUN pip install azure-storage-blob
RUN pip install pyyaml
RUN pip install sklearn

EXPOSE 5000

ENTRYPOINT ["gunicorn"]
CMD ["-w","4","-b",":5000","--timeout","600","app2:app"]

