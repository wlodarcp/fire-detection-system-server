FROM python:3.6

COPY libs.txt SERVER/

RUN pip install -r SERVER/libs.txt

COPY templates/* SERVER/templates/

COPY *.py SERVER/

EXPOSE 8080
EXPOSE 1234

WORKDIR SERVER/

CMD [ "python", "Server.py" ]