#!/bin/sh
echo DEBUG=1 >> .env
echo SQL_ENGINE=django.db.backends.postgresql >> .env
echo SECRET_KEY=$SECRET_KEY >> .env
echo WEB_IMAGE=$IMAGE:web-app  >> .env
echo DB_IMAGE=$IMAGE:database >> .env
echo REDIS_IMAGE=$IMAGE:redis  >> .env
echo WORKER_IMAGE=$IMAGE:worker  >> .env
echo WORKER_IMAGE2=$IMAGE:worker2  >> .env
echo NGINX_IMAGE=$IMAGE:nginx  >> .env
echo CI_REGISTRY_USER=$CI_REGISTRY_USER   >> .env
echo CI_JOB_TOKEN=$CI_JOB_TOKEN  >> .env
echo CI_REGISTRY=$CI_REGISTRY  >> .env
echo IMAGE=$CI_REGISTRY/$CI_PROJECT_NAMESPACE/$CI_PROJECT_NAME >> .env