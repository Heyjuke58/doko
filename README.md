## Setup

### NGINX

Create docker image (``some-content-nginx``) from Dockerfile in ``nginx-html`` folder:

```
docker build -t some-content-nginx .
```

If i want to configure nginx manually (e.g. for adding additional static sites) i can add ``COPY nginx.conf /etc/nginx/nginx.conf`` to the Dockerfile to overwrite the nginx config.

Run ``docker-compose up``
