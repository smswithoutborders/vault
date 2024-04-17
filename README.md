# The Vault

### API References

- [Version 1](/docs/api_v1.md)

### Configurations

#### Environment Variables

The following environment variables are used for configuration:

```
export MYSQL_HOST="your_mysql_host"
export MYSQL_USER="your_mysql_user"
export MYSQL_PASSWORD="your_mysql_password"
export MYSQL_DB_NAME="your_mysql_db_name"
export SQLITE_FILE="your_sqlite_file_path"
export TWILIO_ACCOUNT_SID="your_twilio_account_sid"
export TWILIO_AUTH_TOKEN="your_twilio_auth_token"
export TWILIO_PHONE_NUMBER="your_twilio_phone_number"
export CUSTOM_OWNERSHIP_API_KEY="your_custom_ownership_api_key"
export CUSTOM_OWNERSHIP_API_URL="your_custom_ownership_api_url"
```

### Usage

**Create virtual environment:**

```bash
python3 -m venv venv
```

**Install packages:**

```bash
pip install -r requirements.txt
```

**Run the Flask application:**

```bash
flask run --debug
```
