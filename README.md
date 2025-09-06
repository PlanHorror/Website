# Algorka Tech Club Website

A comprehensive Django-based website for the Algorka Tech Club, featuring project showcases, educational courses, news articles, and member management with multilingual support (English, Vietnamese, Japanese).

## 🚀 Features

- **Multi-language Support**: English, Vietnamese, and Japanese translations
- **User Management**: Custom user authentication with avatar support
- **Content Management**:
  - Project showcase with categorization
  - Educational courses organized by modules
  - News articles with dynamic content
  - Comment system
- **Admin Dashboard**: Comprehensive member dashboard for content management
- **Responsive Design**: Mobile-friendly interface using Bootstrap
- **Media Management**: Image and video support
- **Translation Management**: Built-in translation interface using Django Rosetta

## 🛠 Tech Stack

- **Backend**: Django 5.1.5
- **Database**: PostgreSQL (Production) / SQLite (Development)
- **Frontend**: Bootstrap 5, HTML5, CSS3, JavaScript
- **Deployment**: Docker & Docker Compose
- **Web Server**: Nginx (Production)
- **WSGI Server**: Gunicorn (Production)

## 📋 Prerequisites

- Python 3.11+
- Docker & Docker Compose
- PostgreSQL (for production)

## ⚙️ Installation & Setup

### Local Development

1. **Clone the repository**

   ```bash
   git clone <repository-url>
   cd Website
   ```

2. **Create virtual environment**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirement.txt
   ```

4. **Environment Configuration**
   Create a `.env` file in the root directory (see `.env.template` below)

5. **Database Setup**

   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   python manage.py collectstatic
   ```

6. **Compile Translations**

   ```bash
   python manage.py compilemessages
   ```

7. **Run Development Server**
   ```bash
   python manage.py runserver
   ```

### Production Deployment with Docker

1. **Clone and configure**

   ```bash
   git clone <repository-url>
   cd Website
   cp .env.template .env
   # Edit .env with your production values
   ```

2. **Build and Deploy**

   ```bash
   docker compose up --build -d
   ```

3. **Initialize Database**

   ```bash
   docker compose exec web python manage.py migrate
   docker compose exec web python manage.py createsuperuser
   ```

4. **Access the application**
   - Website: http://localhost
   - Admin: http://localhost/admin
   - Member Dashboard: http://localhost/members

## 📁 Project Structure

```
Website/
├── app/                    # Main application (public pages)
├── members/               # Member management & dashboard
├── website/               # Django project settings
├── templates/             # HTML templates
│   ├── app/              # Public templates
│   └── member/           # Member dashboard templates
├── static/               # Static files (CSS, JS, images)
├── media/                # User uploaded files
├── locale/               # Translation files
│   ├── en/               # English translations
│   ├── vi/               # Vietnamese translations
│   └── ja/               # Japanese translations
├── docker-compose.yml    # Docker configuration
├── dockerfile           # Docker image definition
├── nginx.conf           # Nginx configuration
├── requirement.txt      # Python dependencies
├── .env.template        # Environment variables template
└── manage.py            # Django management script
```

## 🌐 Core Applications

### App (Public Interface)

- **Home Page**: Hero section with video background
- **Projects**: Showcase of tech projects with filtering
- **Courses**: Educational materials organized by modules
- **News**: Latest updates and articles
- **Contact**: Collaboration and feedback forms

### Members (Admin Dashboard)

- **Dashboard**: Analytics and overview
- **Project Management**: Create, edit, translate projects
- **Course Management**: Manage educational content
- **News Management**: Create and manage articles
- **Translation Tools**: Multilingual content management
- **User Profile**: Account settings and statistics

## 🌍 Internationalization

The website supports three languages:

- **English** (`en`) - Default language
- **Vietnamese** (`vi`)
- **Japanese** (`ja`)

### Managing Translations

1. **Extract translatable strings**

   ```bash
   python manage.py makemessages -l vi -l ja
   ```

2. **Compile translations**

   ```bash
   python manage.py compilemessages
   ```

3. **Web-based translation** (Rosetta)
   Access `/rosetta/` in your browser for easy translation management

## 🗄️ Database Models

- **CustomUser**: Extended user model with avatar and profile info
- **Project**: Tech projects with multilingual support
- **Course**: Educational courses organized by modules
- **News**: News articles with dynamic content structure
- **ProjectLabel/NewsLabel**: Categorization system
- **Module**: Course organization system
- **Comment**: User interaction system

## 🔧 Configuration

### Environment Variables (.env.template)

```env
# Debug Settings (True for development, False for production)
DEBUG=False

# Allowed Hosts (comma-separated list of domains/IPs)
ALLOWED_HOSTS=localhost,127.0.0.1,yourdomain.com

# Database Configuration (PostgreSQL connection string)
DATABASE_URL=postgresql://username:password@host:port/database_name


# Example for local PostgreSQL:
# DATABASE_URL=postgresql://postgres:password@localhost:5432/algorka_db
```

### Required Environment Variables

- **DEBUG**: Set to `False` for production, `True` for development
- **ALLOWED_HOSTS**: Comma-separated list of allowed domains/IPs
- **DATABASE_URL**: Complete PostgreSQL connection string with credentials

## 🐳 Docker Configuration

The project includes production-ready Docker configuration:

- **Web Container**: Django application with Gunicorn
- **Nginx Container**: Reverse proxy and static file serving

### Docker Commands

```bash
# Build and start containers
docker compose up --build -d

# View logs
docker compose logs web
docker compose logs nginx

# Execute commands in container
docker compose exec web python manage.py migrate
docker compose exec web python manage.py collectstatic

# Stop containers
docker compose down

# Remove volumes (careful!)
docker compose down -v
```

## 🔒 Security Features

- CSRF protection enabled
- User authentication and authorization
- Secure file upload handling
- SQL injection protection through Django ORM
- XSS protection through template escaping

## 🎨 Frontend Features

- **Responsive Design**: Mobile-first approach
- **Bootstrap 5**: Modern UI components
- **Custom CSS**: Unique styling for tech club theme
- **JavaScript**: Interactive features and AJAX functionality
- **Select2**: Enhanced dropdown selections
- **Chart.js**: Dashboard analytics visualization

## 📊 Admin Dashboard Features

- **Analytics Dashboard**: Project, course, and user statistics
- **Content Management**: Full CRUD operations
- **Translation Interface**: Easy multilingual content management
- **User Management**: Profile and permission management
- **Media Management**: File upload and organization

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Team

**Algorka Tech Club** - Students from the Faculty of Advanced Technology and Engineering at Vietnam Japan University

## 📞 Contact

- Website: [algorka.com](http://algorka.com)
- Email: admin@algorka.com
- GitHub: [github.com/algorka](https://github.com/algorka)

## 🚀 Deployment Notes

### Production Checklist

- [ ] Set `DEBUG=False` in environment variables
- [ ] Configure proper `ALLOWED_HOSTS` with your domain
- [ ] Set up SSL/HTTPS certificates
- [ ] Configure proper `DATABASE_URL` with production credentials
- [ ] Set up backup strategy for media files and database
- [ ] Configure monitoring and logging
- [ ] Set up domain and DNS records

### Maintenance

- Regular database backups
- Monitor disk space for media files
- Keep dependencies updated
- Monitor application logs
- Regular security updates

---

**Built with ❤️ by the Algorka Tech Club**
