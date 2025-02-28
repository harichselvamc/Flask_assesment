API Documentation for Template Management System

This is a RESTful API for user authentication and template management using Flask, JWT for authentication, and MongoDB for data storage.

Base URL:
https://flask-assesment.onrender.com

1. Register User
- Endpoint: /register
- Method: POST
- Description: Register a new user.
- Request Body:
  {
    "first_name": "John",
    "last_name": "Doe",
    "email": "john.doe@example.com",
    "password": "password123"
  }
- Response:
  - Success (201):
    {
      "msg": "User registered successfully"
    }
  - Failure (400):
    {
      "msg": "Missing email or password"
    }

2. User Login
- Endpoint: /login
- Method: POST
- Description: Login a user and obtain a JWT token.
- Request Body:
  {
    "email": "john.doe@example.com",
    "password": "password123"
  }
- Response:
  - Success (200):
    {
      "access_token": "JWT_TOKEN"
    }
  - Failure (401):
    {
      "msg": "Invalid email or password"
    }

3. Create Template
- Endpoint: /template
- Method: POST
- Description: Create a new template for the logged-in user.
- Authorization: JWT token required.
- Request Body:
  {
    "template_name": "Welcome Email",
    "subject": "Welcome to Our Service",
    "body": "Hello, {{name}}. Thank you for signing up!"
  }
- Response:
  - Success (201):
    {
      "msg": "Template created",
      "id": "template_id"
    }

4. Get All Templates (User's Templates)
- Endpoint: /template
- Method: GET
- Description: Retrieve all templates for the logged-in user.
- Authorization: JWT token required.
- Response:
  - Success (200):
    [
      {
        "_id": "template_id",
        "template_name": "Welcome Email",
        "subject": "Welcome to Our Service",
        "body": "Hello, {{name}}. Thank you for signing up!"
      }
    ]

5. Get Single Template by ID
- Endpoint: /template/<template_id>
- Method: GET
- Description: Retrieve a single template by its ID.
- Authorization: JWT token required.
- Response:
  - Success (200):
    {
      "_id": "template_id",
      "template_name": "Welcome Email",
      "subject": "Welcome to Our Service",
      "body": "Hello, {{name}}. Thank you for signing up!"
    }
  - Failure (404):
    {
      "msg": "Template not found"
    }

6. Update Single Template
- Endpoint: /template/<template_id>
- Method: PUT
- Description: Update an existing template by its ID.
- Authorization: JWT token required.
- Request Body:
  {
    "template_name": "Updated Welcome Email",
    "subject": "Updated Subject",
    "body": "Updated email body content"
  }
- Response:
  - Success (200):
    {
      "msg": "Template updated"
    }
  - Failure (404):
    {
      "msg": "Template not found or unauthorized"
    }

7. Delete Single Template
- Endpoint: /template/<template_id>
- Method: DELETE
- Description: Delete a template by its ID.
- Authorization: JWT token required.
- Response:
  - Success (200):
    {
      "msg": "Template deleted"
    }
  - Failure (404):
    {
      "msg": "Template not found or unauthorized"
    }

Authentication
To access any of the protected routes (like creating, getting, updating, or deleting templates), you must include a valid JWT token in the Authorization header of your requests.

Example:
Authorization: Bearer <JWT_TOKEN>

Error Codes:
- 400: Bad Request (e.g., missing fields or invalid data)
- 401: Unauthorized (e.g., invalid login credentials)
- 404: Not Found (e.g., template or user not found)
- 500: Internal Server Error
