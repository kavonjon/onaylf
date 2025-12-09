# ONAYLF Fair Management System

A comprehensive web application for managing educational fairs focused on indigenous language and cultural education. The ONAYLF (Oklahoma Native American Youth Language Fair) Management System handles student registration, submission management, and fair administration through a user-friendly Django-based interface.

## Features

- **User Management**: Role-based access control with admin, moderator, and user roles
- **Student Registration**: Comprehensive student profile and submission management
- **Fair Administration**: Create and manage multiple fairs with customizable categories, with one active fair
- **Submission Tracking**: Track and evaluate student submissions across categories
- **Organization Management**: Manage schools and programs with flexible organization options
- **PDF Generation**: Generate certificates and reports
- **Excel Export**: Export data for analysis and record-keeping

## Quick Start

### For Development (Local Setup)

Requirements:
- Python 3.10+ (Django 5.2 LTS requires Python 3.10 or higher)
- PostgreSQL 14+

### For Production (Docker)

Requirements:
- Docker
- Docker Compose

## Development Setup

For local development, you'll set up a Python virtual environment and use PostgreSQL as the database.

### 1. Clone the Repository

```bash
git clone https://github.com/[username]/onaylf.git
cd onaylf
```

### 2. Set Up Python Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project root:

```bash
cp .env.example .env
```

Edit the `.env` file with development settings:

```env
# Django Settings
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
CSRF_TRUSTED_ORIGINS=http://localhost:8000

# PostgreSQL Database (for local development)
POSTGRES_DB=onaylf
POSTGRES_USER=onaylf_user
POSTGRES_PASSWORD=your-password-here
DBHOST=localhost
DBPORT=5432
DJANGO_SETTINGS_MODULE=onaylf.settings
WORDS="word1,word2,etc"
```

### 5. Set Up PostgreSQL Database

Install and start PostgreSQL if not already installed:

**macOS (using Homebrew):**
```bash
brew install postgresql
brew services start postgresql
```

**Ubuntu/Debian:**
```bash
sudo apt-get install postgresql postgresql-contrib
sudo systemctl start postgresql
```

**Windows:**
Download and install from [postgresql.org](https://www.postgresql.org/download/windows/)

Create the database and user:

```bash
# Connect to PostgreSQL
psql postgres

# In the PostgreSQL prompt, run:
CREATE DATABASE onaylf;
CREATE USER onaylf_user WITH PASSWORD 'your-password-here';
GRANT ALL PRIVILEGES ON DATABASE onaylf TO onaylf_user;
\q
```

### 6. Set Up the Database Schema

Navigate to the app directory and run migrations:

```bash
cd app
python manage.py migrate
```

### 7. Create a Superuser

```bash
python manage.py createsuperuser
```

Follow the prompts to create an admin account.

### 8. Collect Static Files

```bash
python manage.py collectstatic --no-input
```

### 9. Run the Development Server

```bash
python manage.py runserver
```

The application will be available at `http://localhost:8000`

### 10. Access the Admin Interface

Navigate to `http://localhost:8000/admin` and log in with your superuser credentials.

## Production Deployment

### Docker Compose (Recommended)

For production deployment, the application uses Docker containers with PostgreSQL database and Nginx reverse proxy. All dependencies, migrations, and static file collection are handled automatically by the Docker setup.

#### Prerequisites

- Docker
- Docker Compose
- (Recommended) Nginx Proxy Manager for SSL/domain management
- (Optional) A domain name for production use

#### 1. Clone the Repository

```bash
git clone https://github.com/[username]/onaylf.git
cd onaylf
```

#### 2. Configure Environment Variables

Create a `.env` file in the project root:

```bash
cp .env.example .env
```

Edit the `.env` file with production settings:

```env
# Django Settings
SECRET_KEY=your-production-secret-key-here
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
CSRF_TRUSTED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com

# PostgreSQL Database
POSTGRES_DB=onaylf
POSTGRES_USER=onaylf_user
POSTGRES_PASSWORD=strong-password-here
DBHOST=onaylf_db
DBPORT=5432
DJANGO_SETTINGS_MODULE=onaylf.settings

# Email Configuration (Required for password resets)
EMAIL_HOST="smtp-relay.brevo.com"
EMAIL_HOST_USER="id@smtp-brevo.com"
EMAIL_HOST_PASSWORD='password'
DEFAULT_FROM_EMAIL='onaylf.noreply@gmail.com'
ADMINS=[('name', 'email@gmail.com')]

# Logging
DJANGO_LOG_LEVEL="INFO"

# Custom Settings
WORDS="word1,word2,etc"
```

**Important Notes:**
- Generate a strong `SECRET_KEY` for production
- Set `DEBUG=False` for security
- Use `DBHOST=onaylf_db` (this is the Docker container name)
- Configure your actual domain names
- Use strong passwords
- **Network Configuration:** The application uses the `nginxproxymanager_default` Docker network to communicate with Nginx Proxy Manager. If Nginx Proxy Manager is not installed, you'll need to create this network manually: `docker network create nginxproxymanager_default`

#### 3. First Time Setup

Choose one of the following paths depending on whether you have an existing database backup:

**Option A: Restore from Existing Database Backup**

If you have a database backup file (e.g., from a previous installation):

1. Place your backup file in the `backup` directory and name it `backup.sql`:

```bash
# Copy your backup file to the backup directory
cp /path/to/your/backup.sql ./backup/backup.sql
```

2. Start the containers:

```bash
docker-compose up -d --build
```

The `init-db.sh` script will automatically detect the backup file and restore it on first run when the database is empty. After restoring, you can log in with your existing admin credentials.

**Option B: Start Fresh (No Backup)**

If this is a new installation without a backup:

1. Make sure the `backup` directory is empty or does not contain a `backup.sql` file:

```bash
# Remove any existing backup.sql if present
rm -f ./backup/backup.sql
```

2. Start the containers:

```bash
docker-compose up -d --build
```

3. Create a superuser account:

```bash
docker exec -it onaylf_django python manage.py createsuperuser
```

Follow the prompts to create an admin account.

**What Happens During Startup:**

When you run `docker-compose up -d --build`, the system will:
- Build the Docker images
- Start three containers:
  - `onaylf_django`: Django application server (Gunicorn)
  - `onaylf_postgres`: PostgreSQL database
  - `onaylf_nginx`: Nginx reverse proxy
- Automatically run database migrations
- Automatically collect static files
- Restore from `backup/backup.sql` if present and database is empty

#### 4. Set Up Nginx Proxy Manager (Required for Production)

The application is designed to work behind Nginx Proxy Manager, which handles SSL certificates, domain routing, and acts as a reverse proxy. Nginx Proxy Manager runs in a separate Docker container outside of this repository.

**Prerequisites:**
- A domain name pointing to your server
- Nginx Proxy Manager installed and running (see below if not already set up)

**If Nginx Proxy Manager is not already installed:**

1. Create a separate directory for Nginx Proxy Manager:

```bash
mkdir -p ~/nginxproxymanager
cd ~/nginxproxymanager
```

2. Create a `docker-compose.yml` file with the following content:

```yaml
services:
  app:
    image: 'jc21/nginx-proxy-manager:latest'
    restart: unless-stopped
    ports:
      - '80:80'
      - '81:81'
      - '443:443'
    volumes:
      - ./data:/data
      - ./letsencrypt:/etc/letsencrypt

networks:
  default:
    external: true
    name: nginxproxymanager_default
```

3. Start Nginx Proxy Manager:

```bash
docker-compose up -d --build
```

4. Access the Nginx Proxy Manager admin interface at `http://your-server-ip:81`
   - Default login: `admin@example.com` / `changeme`
   - You'll be prompted to change these credentials on first login

**Configure Nginx Proxy Manager for ONAYLF:**

1. In the Nginx Proxy Manager admin panel (port 81), click "Proxy Hosts" → "Add Proxy Host"

2. Configure the proxy host:
   - **Details Tab:**
     - Domain Names: `yourdomain.com` (e.g., `onaylf.example.com`)
     - Scheme: `http`
     - Forward Hostname/IP: `onaylf_nginx`
     - Forward Port: `8181`
     - Enable "Cache Assets"
     - Enable "Block Common Exploits"
     - Enable "Websockets Support"
   
   - **SSL Tab:**
     - SSL Certificate: Select "Request a new SSL Certificate"
     - Enable "Force SSL"
     - Enable "HTTP/2 Support"
     - Email Address: Your email for Let's Encrypt notifications
     - Agree to Let's Encrypt Terms of Service

3. Save the configuration

4. The application will now be accessible at `https://yourdomain.com`

**Security Note:**
- After configuration, block external access to port 81 using your firewall
- Only open port 81 when you need to make changes to Nginx Proxy Manager
- Keep ports 80 and 443 open for web traffic

#### 5. Access the Application

The application will be available at `https://yourdomain.com` (via Nginx Proxy Manager).

For local testing without Nginx Proxy Manager, you can access it directly at `http://localhost:8181`.

#### What Happens Automatically

The Docker setup handles all dependencies and setup automatically:
- Python environment and all packages installed
- PostgreSQL database created and configured
- Database migrations run automatically on startup
- Static files collected automatically
- Gunicorn server configured and started
- Nginx reverse proxy configured

You don't need to manually install Python, PostgreSQL, or any dependencies for production deployment.

## Project Structure

```
onaylf/
├── app/                        # Django project root
│   ├── manage.py              # Django management script
│   ├── onaylf/                # Project settings
│   │   ├── settings.py        # Django settings
│   │   ├── urls.py            # URL routing
│   │   └── wsgi.py            # WSGI application
│   ├── submissions/           # Submissions app
│   │   ├── models.py          # Fair, Student, Submission models
│   │   ├── views.py           # View logic
│   │   └── forms.py           # Django forms
│   ├── users/                 # User management app
│   │   ├── models.py          # Custom User model
│   │   └── views.py           # Authentication views
│   ├── templates/             # HTML templates
│   └── static/                # Static files (CSS, JS, images)
├── docker-compose.yml         # Docker Compose configuration
├── Dockerfile                 # Production Docker image
├── Dockerfile.render          # Render.com deployment
├── requirements.txt           # Python dependencies
├── nginx/                     # Nginx configuration
├── docs/                      # Documentation
└── README.md                  # This file
```

## Key Management Commands

### Database

```bash
# Run migrations
python manage.py migrate

# Create migrations after model changes
python manage.py makemigrations

# Reset database (development only)
python manage.py flush
```

### User Management

```bash
# Create superuser
python manage.py createsuperuser

# Change user password
python manage.py changepassword username
```

### Static Files

```bash
# Collect static files
python manage.py collectstatic

# Clear static files
python manage.py collectstatic --clear
```

### Development

```bash
# Run development server
python manage.py runserver

# Run on specific port
python manage.py runserver 0.0.0.0:8080

# Open Django shell
python manage.py shell
```

## Configuration Options

### Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `SECRET_KEY` | Django secret key | Yes | - |
| `DEBUG` | Enable debug mode | No | `False` |
| `ALLOWED_HOSTS` | Comma-separated list of allowed hosts | Yes | - |
| `CSRF_TRUSTED_ORIGINS` | Comma-separated list of trusted origins | Yes | - |
| `POSTGRES_DB` | PostgreSQL database name | Yes | - |
| `POSTGRES_USER` | PostgreSQL username | Yes | - |
| `POSTGRES_PASSWORD` | PostgreSQL password | Yes | - |
| `DBHOST` | PostgreSQL host | Yes | - |
| `DBPORT` | PostgreSQL port | Yes | `5432` |
| `DJANGO_SETTINGS_MODULE` | Django settings module path | Yes | `onaylf.settings` |
| `EMAIL_HOST` | SMTP server hostname | Yes | - |
| `EMAIL_HOST_USER` | SMTP authentication username | Yes | - |
| `EMAIL_HOST_PASSWORD` | SMTP authentication password | Yes | - |
| `DEFAULT_FROM_EMAIL` | Default "from" address for emails | Yes | - |
| `ADMINS` | List of admin emails as Python list string | Yes | - |
| `DJANGO_LOG_LEVEL` | Django logging level | No | `INFO` |
| `WORDS` | Comma-separated list of words (custom setting) | No | - |

## Testing

Run the test suite:

```bash
cd app
python manage.py test
```

Run tests for a specific app:

```bash
python manage.py test submissions
python manage.py test users
```

## Backup and Restore

### PostgreSQL Backup (Docker)

```bash
# Backup database
docker exec onaylf_postgres pg_dump -U onaylf_user onaylf > backup.sql

# Restore database
docker exec -i onaylf_postgres psql -U onaylf_user onaylf < backup.sql
```

### PostgreSQL Backup (Local Development)

```bash
# Backup database
pg_dump -U onaylf_user onaylf > backup.sql

# Restore database
psql -U onaylf_user onaylf < backup.sql
```

## Troubleshooting

### Common Issues

**Nginx Proxy Manager Connection Issues**
- Verify both applications are on the `nginxproxymanager_default` network
- Check that proxy host uses `onaylf_nginx` as the forward hostname (not localhost)
- Ensure forward port is set to `8181`
- Test direct access at `http://localhost:8181` to verify the app is running
- Check Nginx Proxy Manager logs: `docker logs nginx-proxy-manager`

**SSL/HTTPS Issues**
- Verify domain DNS points to your server
- Ensure ports 80 and 443 are open in firewall
- Check Let's Encrypt rate limits (max 5 certificates per domain per week)
- Verify SSL is enabled in Nginx Proxy Manager proxy host configuration

**Database Connection Error**
- Verify PostgreSQL is running: `docker ps | grep onaylf_postgres`
- Check database credentials in `.env`
- Ensure `DBHOST=onaylf_db` for Docker deployments
- Check database logs: `docker logs onaylf_postgres`

**Static Files Not Loading**
- Run `python manage.py collectstatic`
- Check `STATIC_ROOT` and `STATIC_URL` in settings
- Verify Nginx configuration for production
- Restart containers: `docker-compose restart`

**Permission Denied Errors**
- Check file permissions on media and static directories
- Ensure PostgreSQL user has proper database permissions

**Docker Issues**
- Check logs: `docker-compose logs -f`
- Verify `nginxproxymanager_default` network exists: `docker network ls`
- Create network if missing: `docker network create nginxproxymanager_default`
- Restart containers: `docker-compose restart`
- Rebuild: `docker-compose up -d --build`

## Documentation

Comprehensive documentation is available in the [docs/documentation.md](docs/documentation.md) file, including:
- Detailed feature descriptions
- User roles and permissions
- Database schema
- API endpoints
- Workflow diagrams

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the GNU Affero General Public License v3.0 - see the [LICENSE](LICENSE) file for details.

## Author

Kavon Hooshiar

## Acknowledgments

- Oklahoma Native American Youth Language Fair organization
- Django Software Foundation
- All contributors to the open-source packages used in this project
