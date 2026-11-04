FROM opsdesk-workforce-sample:3.2.0
USER root
COPY . /tests/
RUN mkdir -p /srv/data/private/references && cp /tests/reference.json /srv/data/private/references/ow-0dcf43a361e2.json && chmod -R a+rX /srv/data/private
