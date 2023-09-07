#!/bin/sh

ssh -o StrictHostKeyChecking=no -T root@$SERVER_IP << 'ENDSSH'
  cd app
  export $(cat .env | xargs)
  docker login -u $CI_REGISTRY_USER -p $CI_JOB_TOKEN $CI_REGISTRY
  docker image rm $(docker image ls -f dangling=true -q)
  docker pull $IMAGE:web-app
  docker pull $IMAGE:database
  docker pull $IMAGE:redis
  docker pull $IMAGE:worker
  docker pull $IMAGE:worker2
  docker pull $IMAGE:nginx
  docker-compose -f docker-compose.prod.yml up -d
ENDSSH