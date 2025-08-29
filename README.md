# Garage Management System (GMS) API

A robust Garage Management System API built with FastAPI, SQLAlchemy, and PostgreSQL, featuring role-based access control (RBAC) for secure and flexible permission management. This API allows you to manage customers, vehicles, services, work orders, mechanics, and invoices efficiently.

## Table of Contents
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Getting Started](#getting-started)
- [Environment Variables](#environment-variables)
- [Database Setup & Seeding](#database-setup--seeding)
- [API Endpoints](#api-endpoints)
- [RBAC & Permissions](#rbac--permissions)
- [File Uploads](#file-uploads)
- [Project Structure](#project-structure)
- [Example Requests](#example-requests)
- [Swagger/OpenAPI Representation](#swaggeropenapi-representation)
- [License](#license)

## Features

- ✅ JWT-based authentication with access and refresh tokens
- 🔐 Role-based access control (superadmin, admin, staff, mechanic, customer)
- 👥 User group management for flexible permissions
- 🛠️ CRUD endpoints for:
  - Customers
  - Vehicles
  - Services
  - Work Orders / Jobs
  - Mechanics
  - Invoices / Payments
  - Appointments / Scheduling
- 🔒 Permissions API to manage which groups can access each endpoint
- 📤 Upload customer and vehicle images
- 📚 Fully documented with Swagger UI

## Tech Stack

- **Backend**: FastAPI
- **ORM**: SQLAlchemy
- **Database**: PostgreSQL
- **Authentication**: JWT
- **Python Version**: 3.10+
- **Package Management**: pip / virtualenv

## Getting Started

1. Clone the repository:
   ```bash
   git clone <repo-url>
   cd garage-management-system
   ```

2. Create a virtual environment and activate it:
   ```bash
   # Linux/Mac
   python -m venv venv
   source venv/bin/activate
   
   # Windows
   python -m venv venv
   .\venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure the `.env` file (see example below).

## Environment Variables

Create a `.env` file in the root directory with the following variables:

```env
# Database Configuration
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=garage
POSTGRES_HOST=localhost
POSTGRES_PORT=5432

# JWT Configuration
JWT_SECRET_KEY=supersecretkey_change_me
ACCESS_TOKEN_EXPIRE_MINUTES=60
REFRESH_TOKEN_EXPIRE_MINUTES=10080

# API Configuration
API_PREFIX=/api/v1

# File Uploads
UPLOAD_DIR=uploads
CUSTOMER_UPLOAD_SUBDIR=customers
ITEM_UPLOAD_SUBDIR=items
```

## Database Setup & Seeding

1. Ensure PostgreSQL is running and the database specified in your `.env` file exists.

2. Run the seed script to create default users, groups, and permissions:
   ```bash
   python -m app.seed
   ```
   This will create:
   - Default roles (superadmin, admin, staff, mechanic, customer)
   - Initial admin user
   - Basic permission sets

## API Endpoints

- **Authentication** (`/api/v1/auth/`)
  - Register new users
  - Login with JWT tokens
  - Refresh access tokens

- **Customers** (`/api/v1/customers/`)
  - Create, read, update, delete customers
  - Search and filter customers
  - Upload customer documents/images

- **Vehicles** (`/api/v1/vehicles/`)
  - Manage vehicle information
  - Track vehicle service history
  - Upload vehicle images

- **Services** (`/api/v1/services/`)
  - Define service types and pricing
  - Track service history
  - Manage service packages

- **Work Orders** (`/api/v1/work-orders/`)
  - Create and track service jobs
  - Assign mechanics
  - Update job status

- **Mechanics** (`/api/v1/mechanics/`)
  - Manage mechanic profiles
  - Track assignments
  - View work history

- **Invoices** (`/api/v1/invoices/`)
  - Generate and manage invoices
  - Process payments
  - Track payment history

- **Appointments** (`/api/v1/appointments/`)
  - Schedule service appointments
  - Send reminders
  - Manage calendar

- **Permissions** (`/api/v1/permissions/`)
  - Manage endpoint access
  - Configure role-based permissions
  - Audit access controls

Access the interactive API documentation at `/docs` (Swagger UI) or `/redoc` for ReDoc format.

## RBAC & Permissions

### User Roles
- **Superadmin**: Full system access
- **Admin**: Manage users and settings
- **Staff**: Access to most features
- **Mechanic**: Limited to work orders and assigned tasks
- **Customer**: View own data and make appointments

### Key Features
- Users can belong to multiple groups
- Granular permission control per endpoint
- Superadmin bypasses all restrictions
- Dynamic permission management via API
- Audit logging for permission changes

## File Uploads

Upload and manage files in structured directories:

```
uploads/
├── customers/
│   ├── {customer_id}/
│   │   ├── profile.jpg
│   │   └── documents/
└── items/
    └── {item_id}/
        └── images/
```

### Configuration
- Set base paths in `.env` or `config.py`
- Supported file types: images (JPG, PNG), documents (PDF, DOCX)
- File size limits: 10MB per file by default

## Project Structure

```
garage-management-system/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application
│   ├── config.py            # Configuration settings
│   ├── db/                  # Database configuration
│   │   ├── __init__.py
│   │   ├── session.py
│   │   └── base.py
│   ├── models/              # SQLAlchemy models
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── customer.py
│   │   └── ...
│   ├── schemas/             # Pydantic models
│   ├── api/                 # API routes
│   ├── core/                # Core functionality
│   └── seed.py              # Database seeding
├── uploads/                 # File uploads
├── requirements.txt         # Python dependencies
├── .env                    # Environment variables
└── README.md

## Example Requests

### Create a Service
```http
POST /api/v1/services/
Authorization: Bearer <ACCESS_TOKEN>
Content-Type: application/json

{
  "name": "Oil Change (Synthetic)",
  "description": "Full synthetic oil change with filter replacement",
  "price": 49.99,
  "duration_minutes": 45
}
```

### Register a New User
```http
POST /api/v1/auth/register
Content-Type: application/json

{
  "username": "john_doe",
  "password": "strongpassword",
  "email": "john@example.com",
  "groups": ["staff", "mechanic"]
}
```

### Assign Permission to Endpoint
```http
POST /api/v1/permissions/
Authorization: Bearer <ADMIN_TOKEN>
Content-Type: application/json

{
  "module": "service",
  "endpoint_name": "create-service",
  "allowed_groups": "admin,superadmin,staff"
}
```

## API Documentation

Access the interactive API documentation at:
- Swagger UI: `/docs`
- ReDoc: `/redoc`

### Available Endpoints

#### Authentication
- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - Login with credentials
- `GET /api/v1/auth/me` - Get current user info
- `POST /api/v1/auth/refresh` - Refresh access token

#### Customers
- `GET /api/v1/customers/` - List all customers
- `POST /api/v1/customers/` - Create new customer
- `GET /api/v1/customers/{id}` - Get customer details
- `PUT /api/v1/customers/{id}` - Update customer
- `DELETE /api/v1/customers/{id}` - Delete customer

#### Other Resources
Similar CRUD endpoints are available for:
- Vehicles
- Services
- Work Orders
- Mechanics
## License

MIT License

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.