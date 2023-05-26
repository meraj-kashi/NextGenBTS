#!/bin/sh

vault login token=$VAULT_TOKEN

vault secrets enable -path=NextGenBTS/userLogin kv-v2
vault kv put NextGenBTS/userLogin/admin username=admin password=secretpassword