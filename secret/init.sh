#!/bin/bash

export VAULT_ADDR=http://127.0.0.1:8200
export VAULT_SKIP_VERIFY='true'

vault operator init -recovery-shares 1 -recovery-threshold 1 -format=json > /tmp/key.json
VAULT_TOKEN=$(cat /tmp/key.json | jq -r ".root_token")

export VAULT_TOKEN=$VAULT_TOKEN

sleep 10

vault secrets enable -path=kv kv-v2