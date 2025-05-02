# IoT Lab Management System

## 🌟 Overview
A robust and scalable web application designed to streamline the management of IoT laboratory components, inventory, and maintenance records. This system provides a comprehensive solution for educational institutions, research labs, and organizations working with IoT devices.

## ✨ Key Features

### Component Management
- 📦 Add, edit, and delete IoT components with detailed specifications
- 🔄 Real-time status tracking (Available, In-Use, Maintenance)
- 🔍 Advanced search functionality with autocomplete
- 📊 Detailed component information and history

### Inventory Management
- 📈 Real-time inventory tracking and monitoring
- 📊 Quantity management with alerts
- 🔄 Status updates and tracking
- 📱 Responsive design for all devices

### Maintenance Tracking
- 📝 Comprehensive maintenance logging
- 📅 Maintenance scheduling and reminders
- 📊 Maintenance history and reports
- 🔔 Status notifications

### User Management
- 🔐 Secure authentication system
- 👥 Role-based access control
- 📊 User activity tracking
- 🔒 Admin dashboard

## 🛠️ Technology Stack

### Backend
- Django 5.1.7
- Python 3.13
- Django REST framework
- SQLite (Lightweight and efficient for development and small-scale production)
- Gunicorn
- Nginx

### Frontend
- Bootstrap 5.3.0
- jQuery 3.6.0
- Bootstrap Icons
- Custom CSS
- AJAX for dynamic updates

### Deployment
- AWS EC2 (Ubuntu)
- Nginx as reverse proxy
- Gunicorn as application server
- SSL/TLS security
- Automated deployment

## 📋 Prerequisites
- Python 3.13 or higher
- pip (Python package manager)
- Virtual environment
- AWS account (for deployment)

## 🚀 Getting Started

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/iotlab.git
   cd iotlab
   ```

2. Create and activate virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up the database:
   ```bash
   python manage.py migrate
   ```

5. Create superuser:
   ```bash
   python manage.py createsuperuser
   ```

6. Run development server:
   ```bash
   python manage.py runserver
   ```

## �� Project Structure

```
iotlab/
├── components/                 # Main application
│   ├── migrations/            # Database migrations
│   ├── templates/             # HTML templates
│   ├── static/                # Static files (CSS, JS, images)
│   ├── models.py              # Database models
│   ├── views.py               # View functions
│   ├── urls.py                # URL patterns
│   └── forms.py               # Form definitions
├── iotlab/                    # Project settings
│   ├── settings.py            # Django settings
│   ├── urls.py                # Main URL configuration
│   └── wsgi.py                # WSGI configuration
└── manage.py                  # Django management script
```

## Usage

1. Access the admin panel at `/admin/` to manage:
   - Components
   - Categories
   - Users
   - Maintenance logs

2. Use the inventory page at `/inventory/` to:
   - View all components
   - Search for specific components
   - Update component status
   - Track quantities

3. Component management:
   - Add new components at `/component/new/`
   - Edit existing components at `/component/<id>/update/`
   - View component details at `/component/<id>/`

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Django Documentation
- Bootstrap Documentation
- AWS Documentation
- All contributors and maintainers

## Support

For support, please open an issue in the GitHub repository or contact the maintainers.

## Roadmap

- [ ] Add API endpoints for mobile app integration
- [ ] Implement barcode/QR code scanning
- [ ] Add data export functionality
- [ ] Implement advanced reporting features
- [ ] Add email notifications for maintenance schedules
- [ ] Multi-language support
- [ ] API documentation
- [ ] Performance optimization
- [ ] Database migration to PostgreSQL (for larger scale deployment) 
