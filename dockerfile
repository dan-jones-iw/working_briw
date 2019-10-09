FROM python:latest

COPY ./ /BrIW
WORKDIR ./BrIW

RUN pip3 install -r ./requirements.txt

EXPOSE 8008

ENTRYPOINT ["python3", "-m", "dynamic_website.flask"]"
