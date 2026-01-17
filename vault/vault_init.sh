#!/bin/sh

export VAULT_ADDR=http://localhost:8200
export VAULT_TOKEN=dev-root-token

vault kv put secret/myapp/config \
  DATABASE_URL="postgres://myapp:myapp_password@postgres:5432/myapp" \
  KEYCLOAK_CLIENT_ID="django-client" \
  KEYCLOAK_CLIENT_SECRET="super-secret-client-secret" \
  KEYCLOAK_REALM="myrealm" \
  KEYCLOAK_BASE_URL="http://keycloak:8080"
