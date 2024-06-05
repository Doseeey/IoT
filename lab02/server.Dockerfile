FROM python:3.8

WORKDIR /app

RUN pip install flask requests numpy

COPY . /app

ENTRYPOINT [ "python" ]
CMD [ "server.py" ]