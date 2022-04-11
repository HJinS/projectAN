FROM nginx:latest

COPY docker-nginx/proxy_params /etc/nginx/
COPY docker-nginx/nginx.conf /etc/nginx/nginx.conf
COPY docker-nginx/an /etc/nginx/sites-enabled/

CMD ["nginx", "-g", "daemon off;"]