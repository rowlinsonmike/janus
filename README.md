<h1 align="center">
  <br>
  <img src="assets/janus.jpg" alt="logo" width="300" height="300" style="border-radius: 50%; width: 300px; height: 300px; object-fit: cover;"/>
  <br>
 Janus
  <br>
</h1>

<h4 align="center">A CLI tool for securely managing your passwords with a local encrypted file.</h4>

<p align="center">
  <a href="#features">Features</a> •
  <a href="#why-choose-this-cli-over-saas-solutions">Why</a> •
  <a href="#install">Install</a> •
  <a href="#usage">Usage</a> •
  <a href="#security">Security</a> •
</p>

## Features

- **Secure Storage**: Passwords are encrypted using AES-256-GCM
- **Local Storage**: All data is stored locally
- **Clipboard Integration**: Passwords are copied to the clipboard when retrieved

## Why Choose This CLI Over SaaS Solutions

- **Privacy**: Your passwords are stored locally.
- **Control**: You have complete control over your data
- **No Subscription Fees**: No monthly fees
- **Simplicity**: A straightforward experience

## Install

1. Ensure you have Python >= 3.8 installed on your system.
2. run pip install command

```bash
pip install https://github.com/rowlinsonmike/janus/raw/refs/heads/main/dist/janus.tar.gz
```

## Usage

### Add a Password

To add a new password for a service:

```bash
janus add <service> <username>
```

You will be prompted to enter the password and the master encryption key.

### Update a Password

To update an existing password:

```bash
janus update <service> <username>
```

You will be prompted to enter the new password and the master encryption key.

### Delete a Password

To delete a password for a service:

```bash
janus delete <service>
```

You will be prompted to enter the master encryption key.

### Retrieve a Password

To retrieve a password for a service:

```bash
janus get <service>
```

The password will be copied to your clipboard. You will be prompted to enter the master encryption key.

### List All Services

To list all available services:

```bash
janus list
```

You will be prompted to enter the master encryption key.

## Security

- Always use a strong master encryption key to protect your passwords.
- Regularly back up your encrypted password file to prevent data loss.
