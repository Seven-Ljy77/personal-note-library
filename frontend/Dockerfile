FROM python:3.13-slim

WORKDIR /services

COPY index/ .
COPY mine/ .
COPY utils.js .

CMD ["python" , "-m" , "http.server" , "8000"]