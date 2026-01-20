import os
import hvac


def is_ci():
    return os.getenv("CI", "false").lower() == "true"


def get_vault_client():
    if is_ci():
        return None

    vault_addr = os.getenv("VAULT_ADDR", "http://vault:8200")
    vault_token = os.getenv("VAULT_TOKEN", "dev-root-token")

    client = hvac.Client(
        url=vault_addr,
        token=vault_token,
    )

    if not client.is_authenticated():
        raise RuntimeError("Vault authentication failed")

    return client

def get_secret(path: str):
    if is_ci():
        return None

    try:
        client = get_vault_client()
        secret = client.secrets.kv.v2.read_secret_version(path=path)
        return secret["data"]["data"]
    except Exception as e:
        print(f"⚠️ Vault Error: {e}")
        return None  