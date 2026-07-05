# Base URL
BASELINK=http://127.0.0.1:8000/

# Database
DB_HOST=localhost

DB_NAME=your_database_name

DB_USER=your_database_user

DB_PASS=your_database_password

DB_PORT=5432

# PostgreSQL URL
POSTGRE_SQL_URL=postgresql://username:password@localhost:5432/database_name

# Production Database (Optional)
PRODUCTION_SQL_URL=postgresql://username:password@host:5432/database_name

# JWT Configuration
SECRET_KEY=your_secret_key

REFRESH_SECRET_KEY=your_refresh_secret_key

EMAIL_SECRET_KEY=your_email_secret_key

PASS_SECRET_KEY=your_password_reset_secret_key

ALGORITHM=HS256

TOKEN_EXPIRE_IN_MINUTES=10

REFRESH_EXPIRE_IN_MINUTES=43200

EMAIL_EXPIRATION_TIME=10

PASS_EXPIRATION_TIME=5


# Email Configuration
MAIL_USERNAME=your_email@gmail.com

MAIL_PASSWORD=your_app_password


MAIL_FROM=your_email@gmail.com

MAIL_PORT=587

MAIL_SERVER=smtp.gmail.com


MAIL_STARTTLS=True

MAIL_SSL_TLS=False

MAIL_FROM_NAME=Your Application Name