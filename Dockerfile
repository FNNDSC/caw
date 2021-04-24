FROM python:3-alpine

WORKDIR /usr/local/src
COPY . .
RUN pip --no-cache-dir install -r requirements.txt \
    && pip --no-cache-dir install . \
    && caw --install-completion

CMD ["caw"]
