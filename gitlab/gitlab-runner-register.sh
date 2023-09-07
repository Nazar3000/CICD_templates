#!/bin/sh

export $(cat .env.gitlab | xargs)
registration_token=$REGISTRATION_TOKEN
url=$CI_SERVER_URL


docker exec -it gitlab-runner1 \
  gitlab-runner register \
    --non-interactive \
    --registration-token ${registration_token} \
    --locked=false \
    --description docker.compose \
    --url ${url} \
    --executor docker \
    --docker-image docker/compose:1.29.2 \
    --docker-volumes "/var/run/docker.sock:/var/run/docker.sock" \
    --docker-network-mode gitlab-network
