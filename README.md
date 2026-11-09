# ✈️ Airline SaaS Core API

A high-performance, multi-tenant REST API for an airline booking platform. Built with Django, Django REST Framework (DRF), MongoDB (MongoEngine), and deployed via AWS Serverless architecture.

## 🚀 Key Features
- **Flight Search & Inventory**: Multi-tenant flight CRUD with compound MongoDB indexes for optimized search.
- **Atomic Bookings**: Prevents overbooking using MongoDB's atomic `$inc` operations during high concurrency.
- **Serverless Loyalty Engine**: Automated points-award system triggered via an isolated event handler (Lambda-ready).
- **Analytics Integration**: Unified endpoint simulating Google Analytics and Facebook Marketing API aggregation.
- **CI/CD**: Automated testing pipeline using GitHub Actions.
- **Cloud-Ready**: Includes AWS SAM templates for deployment to AWS Lambda & API Gateway.

## 🛠️ Tech Stack
- **Framework**: Python 3.12, Django 5.0, Django REST Framework
- **Database**: MongoDB Atlas (via MongoEngine & PyMongo)
- **Documentation**: OpenAPI 3.0 (Swagger UI via drf-spectacular)
- **DevOps**: GitHub Actions, AWS SAM (Serverless)

## ⚙️ Local Setup
1. Clone the repo: `git clone https://github.com/yourusername/airline-saas-core.git`
2. Create virtual env: `python -m venv .venv`
3. Activate: `source .venv/bin/activate` (or `.venv\Scripts\activate` on Windows)
4. Install dependencies: `pip install -r requirements.txt`
5. Set up `.env` based on `.env.example`
6. Run server: `python manage.py runserver`
7. Access Swagger UI at: `http://127.0.0.1:8000/api/docs/`