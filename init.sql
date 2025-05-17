CREATE USER django_user WITH PASSWORD 'django_password';
ALTER USER django_user WITH SUPERUSER;
CREATE DATABASE django_db;
GRANT ALL PRIVILEGES ON DATABASE django_db TO django_user; 