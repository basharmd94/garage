Garage Management System (GMS) API

A robust Garage Management System API built with FastAPI, SQLAlchemy, and PostgreSQL, featuring role-based access control (RBAC) for secure and flexible permission management. This API allows you to manage customers, vehicles, services, work orders, mechanics, and invoices efficiently.

Table of Contents

Features

Tech Stack

Getting Started

Environment Variables

Database Setup & Seeding

API Endpoints

RBAC & Permissions

File Uploads

Project Structure

Example Requests

Swagger/OpenAPI Representation

License

Features

JWT-based authentication with access and refresh tokens

Role-based access control (superadmin, admin, staff, mechanic, customer)

User group management for flexible permissions

CRUD endpoints for Customers, Vehicles, Services, Work Orders / Jobs, Mechanics, Invoices / Payments, Appointments / Scheduling

Permissions API to manage which groups can access each endpoint

Upload customer and vehicle images

Fully documented with Swagger UI

Tech Stack

Backend: FastAPI

ORM: SQLAlchemy

Database: PostgreSQL

Authentication: JWT

Python Version: 3.10+

Package Management: pip / virtualenv

Getting Started

Clone the repository:
git clone <repo-url>
cd garage-management-system

Create a virtual environment and activate it:
python -m venv venv
Linux / Mac: source venv/bin/activate
Windows: venv\Scripts\activate

Install dependencies:
pip install -r requirements.txt

Configure the .env file (example below).

Environment Variables (.env)

POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=garaze
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
JWT_SECRET_KEY=supersecretkey_change_me
ACCESS_TOKEN_EXPIRE_MINUTES=60
REFRESH_TOKEN_EXPIRE_MINUTES=10080
API_PREFIX=/api/v1
UPLOAD_DIR=uploads
CUSTOMER_UPLOAD_SUBDIR=customers
ITEM_UPLOAD_SUBDIR=items

Database Setup & Seeding

Ensure PostgreSQL is running and database garaze exists.

Run the seed script to create default users, groups, and permissions:
python -m app.seed

API Endpoints

/api/v1/auth/ → Register, login, refresh tokens

/api/v1/customers/ → CRUD customers

/api/v1/vehicles/ → CRUD vehicles

/api/v1/services/ → CRUD services

/api/v1/work-orders/ → CRUD work orders

/api/v1/mechanics/ → CRUD mechanics

/api/v1/invoices/ → CRUD invoices

/api/v1/appointments/ → CRUD appointments

/api/v1/permissions/ → Manage endpoint access for groups

Full OpenAPI documentation available at /docs (Swagger UI).

RBAC & Permissions

Each user has a role: superadmin, admin, staff, mechanic, customer

Each user can belong to one or more groups

Every API endpoint can define which groups are allowed to access it

Superadmin bypasses all restrictions automatically

Permissions can be managed dynamically via the /api/v1/permissions/ API

File Uploads

Customer and vehicle images can be uploaded to structured directories:
uploads/
   ├─ customers/
   └─ items/

Configure file paths via .env or config.py

Project Structure

garage-management-system/
   ├─ app/
   │   ├─ init.py
   │   ├─ main.py
   │   ├─ config.py
   │   ├─ db/
   │      ├─ init.py
   │      ├─ session.py
   │      └─ base.py
   │   ├─ models/
   │      ├─ init.py
   │      ├─ user.py
   │      ├─ customer.py
   │      ├─ vehicle.py
   │      ├─ service.py
   │      ├─ work_order.py
   │      ├─ mechanic.py
   │      ├─ invoice.py
   │      └─ permission.py
   │   ├─ schemas/
   │   ├─ api/
   │   ├─ core/
   │   └─ seed.py
   ├─ uploads/
   ├─ requirements.txt
   ├─ .env
   ├─ .gitignore
   └─ README.md

Example Requests

Create a Service: POST /api/v1/services/ Authorization: Bearer <ACCESS_TOKEN>
{ "name": "Oil Change (Synthetic)", "description": "Full synthetic oil change with filter replacement", "price": 49.99, "duration_minutes": 45 }

Register a User: POST /api/v1/auth/register
{ "username": "john_doe", "password": "strongpassword", "email": "john@example.com
", "groups": ["staff", "mechanic"] }

Assign Permission to Endpoint: POST /api/v1/permissions/
{ "module": "service", "endpoint_name": "create-service", "allowed_groups": "admin,superadmin,staff" }

Swagger/OpenAPI Representation

Auth
   ├─ POST /api/v1/auth/register
   ├─ POST /api/v1/auth/login
   └─ GET /api/v1/auth/me

Customers
   ├─ POST /api/v1/customers/
   ├─ GET /api/v1/customers/
   ├─ GET /api/v1/customers/{id}
   ├─ PUT /api/v1/customers/{id}
   └─ DELETE /api/v1/customers/{id}

Vehicles, Services, Permissions, Work Orders, Mechanics, Invoices, Appointments
   └─ Similar CRUD endpoints

License

MIT License © 2025 Garage Management System

This version keeps Markdown formatting, headings, lists, bold text, and inline code, but all content is in one continuous block for easy copy-pasting.

I can also make a compact Postman-ready JSON file with all CRUD endpoints next so you can import it immediately.

Do you want me to do that?

You said:
make this single markdown text editor .. your instruction got seperated. all markdown will be single screen
ChatGPT said:

Ah! Now I fully understand. You want all Markdown content in a single, continuous text block, formatted as Markdown, without any code fences or sections that break the editor view. Everything should be copy-pasteable in one go and visible in a single editor window.

Here’s a fully continuous Markdown version:

Garage Management System (GMS) API

A robust Garage Management System API built with FastAPI, SQLAlchemy, and PostgreSQL, featuring role-based access control (RBAC) for secure and flexible permission management. This API allows you to manage customers, vehicles, services, work orders, mechanics, and invoices efficiently.

Table of Contents

Features

Tech Stack

Getting Started

Environment Variables

Database Setup & Seeding

API Endpoints

RBAC & Permissions

File Uploads

Project Structure

Example Requests

Swagger/OpenAPI Representation

License

Features

JWT-based authentication with access and refresh tokens

Role-based access control (superadmin, admin, staff, mechanic, customer)

User group management for flexible permissions

CRUD endpoints for Customers, Vehicles, Services, Work Orders / Jobs, Mechanics, Invoices / Payments, Appointments / Scheduling

Permissions API to manage which groups can access each endpoint

Upload customer and vehicle images

Fully documented with Swagger UI

Tech Stack

Backend: FastAPI

ORM: SQLAlchemy

Database: PostgreSQL

Authentication: JWT

Python Version: 3.10+

Package Management: pip / virtualenv

Getting Started

Clone the repository: git clone <repo-url> and cd garage-management-system

Create a virtual environment and activate it: python -m venv venv (Linux / Mac: source venv/bin/activate, Windows: venv\Scripts\activate)

Install dependencies: pip install -r requirements.txt

Configure the .env file (example below)

Environment Variables (.env)

POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=garaze
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
JWT_SECRET_KEY=supersecretkey_change_me
ACCESS_TOKEN_EXPIRE_MINUTES=60
REFRESH_TOKEN_EXPIRE_MINUTES=10080
API_PREFIX=/api/v1
UPLOAD_DIR=uploads
CUSTOMER_UPLOAD_SUBDIR=customers
ITEM_UPLOAD_SUBDIR=items

Database Setup & Seeding

Ensure PostgreSQL is running and database garaze exists.

Run the seed script to create default users, groups, and permissions: python -m app.seed

API Endpoints

/api/v1/auth/ → Register, login, refresh tokens

/api/v1/customers/ → CRUD customers

/api/v1/vehicles/ → CRUD vehicles

/api/v1/services/ → CRUD services

/api/v1/work-orders/ → CRUD work orders

/api/v1/mechanics/ → CRUD mechanics

/api/v1/invoices/ → CRUD invoices

/api/v1/appointments/ → CRUD appointments

/api/v1/permissions/ → Manage endpoint access for groups

Full OpenAPI documentation available at /docs (Swagger UI)

RBAC & Permissions

Each user has a role: superadmin, admin, staff, mechanic, customer

Each user can belong to one or more groups

Every API endpoint can define which groups are allowed to access it

Superadmin bypasses all restrictions automatically

Permissions can be managed dynamically via the /api/v1/permissions/ API

File Uploads

Customer and vehicle images can be uploaded to structured directories:
uploads/
   ├─ customers/
   └─ items/

Configure file paths via .env or config.py

Project Structure

garage-management-system/
   ├─ app/
   │   ├─ init.py
   │   ├─ main.py
   │   ├─ config.py
   │   ├─ db/
   │      ├─ init.py
   │      ├─ session.py
   │      └─ base.py
   │   ├─ models/
   │      ├─ init.py
   │      ├─ user.py
   │      ├─ customer.py
   │      ├─ vehicle.py
   │      ├─ service.py
   │      ├─ work_order.py
   │      ├─ mechanic.py
   │      ├─ invoice.py
   │      └─ permission.py
   │   ├─ schemas/
   │   ├─ api/
   │   ├─ core/
   │   └─ seed.py
   ├─ uploads/
   ├─ requirements.txt
   ├─ .env
   ├─ .gitignore
   └─ README.md

Example Requests

Create a Service: POST /api/v1/services/ Authorization: Bearer <ACCESS_TOKEN>
{ "name": "Oil Change (Synthetic)", "description": "Full synthetic oil change with filter replacement", "price": 49.99, "duration_minutes": 45 }

Register a User: POST /api/v1/auth/register
{ "username": "john_doe", "password": "strongpassword", "email": "john@example.com
", "groups": ["staff", "mechanic"] }

Assign Permission to Endpoint: POST /api/v1/permissions/
{ "module": "service", "endpoint_name": "create-service", "allowed_groups": "admin,superadmin,staff" }

Swagger/OpenAPI Representation

Auth: POST /api/v1/auth/register, POST /api/v1/auth/login, GET /api/v1/auth/me
Customers: POST /api/v1/customers/, GET /api/v1/customers/, GET /api/v1/customers/{id}, PUT /api/v1/customers/{id}, DELETE /api/v1/customers/{id}
Vehicles, Services, Permissions, Work Orders, Mechanics, Invoices, Appointments: Similar CRUD endpoints

License

MIT License © 2025 Garage Management System