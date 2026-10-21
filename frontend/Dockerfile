FROM python:3.13-slim

WORKDIR /services

COPY index/     ./index/
COPY mine/      ./mine/
COPY utils.js   .

CMD ["python" , "-m" , "http.server" , "8000"]