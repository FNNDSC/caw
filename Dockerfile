FROM python:3.10.2-alpine

WORKDIR /usr/local/src
COPY . .
RUN pip --no-cache-dir install -r requirements.txt \
    && pip --no-cache-dir install .

# btw, caw --install-completion doesn't work on alpine
# because sh does not support subcommand completion.

CMD ["caw"]
