FROM python:3.6
LABEL maintainer="silvan.muehlemann@muehlemann-popp.ch"

RUN pip install Flask==0.12.2 requests==2.11.1 neo4j-driver==1.5.0

WORKDIR /app
COPY app /app
EXPOSE 9090
CMD ["python", "app.py"]
