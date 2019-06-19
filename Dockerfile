FROM python:3
LABEL maintainer Andre Felipe "andre.silva5284@hotmail.com"

COPY . /app
WORKDIR /app
RUN pip install -r requirements
CMD ["/bin/bash", "-c", "python start.py"]