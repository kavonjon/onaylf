FROM nginx:1.25

RUN rm /etc/nginx/conf.d/default.conf
COPY ./local.conf /etc/nginx/conf.d/
COPY ./cert/onaylf_samnoblemuseum_ou_edu.crt /etc/nginx/ssl/