import typer
import base64
import os
import json
import pyperclip
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.backends import default_backend
from pathlib import Path
import sys

app = typer.Typer(help="Janus")

PASSWORD_FILE = Path.cwd() / "passwords.enc"


def encrypt_text(plaintext, master_key):
    salt = os.urandom(16)
    kdf = Scrypt(salt=salt, length=32, n=2**14, r=8, p=1, backend=default_backend())
    key = kdf.derive(master_key.encode())
    nonce = os.urandom(12)
    aesgcm = AESGCM(key)
    ciphertext = aesgcm.encrypt(nonce, plaintext.encode(), None)
    encrypted_data = salt + nonce + ciphertext
    return base64.b64encode(encrypted_data).decode("utf-8")


def decrypt_text(encrypted_data, master_key):
    data = base64.b64decode(encrypted_data.encode("utf-8"))
    salt, nonce, ciphertext = data[:16], data[16:28], data[28:]
    kdf = Scrypt(salt=salt, length=32, n=2**14, r=8, p=1, backend=default_backend())
    key = kdf.derive(master_key.encode())
    aesgcm = AESGCM(key)
    try:
        plaintext = aesgcm.decrypt(nonce, ciphertext, None)
    except:
        print("Access Denied.")
        sys.exit()
    return plaintext.decode("utf-8")


def load_passwords(master_key):
    if PASSWORD_FILE.exists():
        encrypted_data = PASSWORD_FILE.read_text()
        decrypted_data = decrypt_text(encrypted_data, master_key)
        return json.loads(decrypted_data)
    return {}


def save_passwords(passwords, master_key):
    plaintext = json.dumps(passwords)
    encrypted_data = encrypt_text(plaintext, master_key)
    PASSWORD_FILE.write_text(encrypted_data)


@app.command()
def add(
    service: str = typer.Argument(..., help="Service name"),
    username: str = typer.Argument(..., help="Username for the service"),
    key: str = typer.Option(
        ..., prompt=True, hide_input=True, help="Master encryption key"
    ),
):
    """Add a new password for a service."""
    password = typer.prompt("Password", hide_input=True)
    passwords = load_passwords(key)
    passwords[service] = {"username": username, "password": password}
    save_passwords(passwords, key)
    typer.echo(f"Password for {service} added.")


@app.command()
def update(
    service: str = typer.Argument(..., help="Service name"),
    username: str = typer.Argument(..., help="Username for the service"),
    key: str = typer.Option(
        ..., prompt=True, hide_input=True, help="Master encryption key"
    ),
):
    """Update the password for an existing service."""
    password = typer.prompt("New Password", hide_input=True)
    passwords = load_passwords(key)
    if service in passwords:
        passwords[service] = {"username": username, "password": password}
        save_passwords(passwords, key)
        typer.echo(f"Password for {service} updated.")
    else:
        typer.echo(f"Service {service} not found.")


@app.command()
def delete(
    service: str = typer.Argument(..., help="Service name"),
    key: str = typer.Option(
        ..., prompt=True, hide_input=True, help="Master encryption key"
    ),
):
    """Delete the password for a service."""
    passwords = load_passwords(key)
    if service in passwords:
        del passwords[service]
        save_passwords(passwords, key)
        typer.echo(f"Password for {service} deleted.")
    else:
        typer.echo(f"Service {service} not found.")


@app.command()
def get(
    service: str = typer.Argument(..., help="Service name"),
    key: str = typer.Option(
        ..., prompt=True, hide_input=True, help="Master encryption key"
    ),
):
    """Retrieve the password for a service."""
    passwords = load_passwords(key)
    if service in passwords:
        username = passwords[service]["username"]
        password = passwords[service]["password"]
        pyperclip.copy(password)
        typer.echo(
            f"Username for {service} is {username}. Password copied to clipboard."
        )
    else:
        typer.echo(f"Service {service} not found.")


@app.command()
def list(
    key: str = typer.Option(
        ..., prompt=True, hide_input=True, help="Master encryption key"
    )
):
    """List all available services."""
    passwords = load_passwords(key)
    if passwords:
        typer.echo("Available services:")
        for service in passwords.keys():
            typer.echo(f"- {service}")
    else:
        typer.echo("No services found.")


if __name__ == "__main__":
    app()
