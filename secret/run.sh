docker run -it -d --cap-add=IPC_LOCK -e 'VAULT_DEV_ROOT_TOKEN_ID=myroot' -e 'VAULT_DEV_LISTEN_ADDRESS=0.0.0.0:8200' -p 8300:8200 --name=secret-vault vault

export VAULT_ADDR="http://localhost:8300"
export VAULT_TOKEN="myroot"

vault login token=$VAULT_TOKEN

vault secrets enable -path=NextGenBTS/userLogin kv-v2
vault kv put NextGenBTS/userLogin/admin username=admin password=secretpassword