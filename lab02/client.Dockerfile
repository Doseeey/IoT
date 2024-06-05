FROM python:3.8

COPY . .

RUN pip install requests

ENTRYPOINT [ "python" ]
CMD [ "client.py" ]