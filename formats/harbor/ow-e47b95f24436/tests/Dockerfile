FROM opsdesk-workforce-sample:3.2.0
USER root
COPY . /tests/
RUN mkdir -p /srv/data/private/references && cp /tests/reference.json /srv/data/private/references/ow-e47b95f24436.json && chmod -R a+rX /srv/data/private
