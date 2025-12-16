FROM nginx:1.25

RUN rm /etc/nginx/conf.d/default.conf

# Generate self-signed placeholder certificates
# (Load balancer handles actual SSL termination, these are fallback/passthrough)
RUN mkdir -p /etc/nginx/ssl && \
    openssl req -x509 -nodes -days 3650 -newkey rsa:2048 \
    -keyout /etc/nginx/ssl/nginx.key \
    -out /etc/nginx/ssl/nginx.crt \
    -subj "/C=US/ST=State/L=City/O=Org/CN=localhost"

COPY ./local.conf /etc/nginx/conf.d/