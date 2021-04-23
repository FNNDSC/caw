FROM python:3-alpine

WORKDIR /usr/local/src
COPY . .
RUN pip --no-cache-dir install .

CMD ["caw"]
