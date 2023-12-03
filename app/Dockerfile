FROM python:3.10.1

USER root
RUN apt-get update
RUN apt-get install -y git curl python3-pip python3-dev python3-venv nano
RUN python3 -m pip install --upgrade pip setuptools wheel build
RUN pip3 --no-cache-dir install --upgrade virtualenv
RUN python3 -m venv venv

RUN mkdir mycode
COPY app mycode
RUN ls -l

WORKDIR mycode

RUN . /venv/bin/activate && python3 --version && python3 -m pip install --upgrade pip setuptools wheel build nano && \
    pip install -r /mycode/requirements.txt && export $(xargs < database.conf) && export FLASK_APP=/mycode/app.py
    
CMD . /venv/bin/activate && python3 app.py
