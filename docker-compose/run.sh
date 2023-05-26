#!/bin/bash

docker-compose up -d

sleep 10

docker build -t nextgenbts_vault_config ../secret/config/
docker run --rm --network=docker-compose_nextgennetwork nextgenbts_vault_config