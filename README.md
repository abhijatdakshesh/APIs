# User Management API

A Django-based REST API for user management with features like user registration, OTP authentication, document uploads, and metadata management.

## Features

- User Registration with detailed profile
- OTP-based Authentication
- Document Upload (Aadhar, PAN, Police Verification, Empanelment Letter)
- User Metadata Management
- PostgreSQL Database
- Docker Support

## Prerequisites

- Docker and Docker Compose
- Git
- Postman (for API testing)

## Setup Instructions

1. Clone the repository:
```bash
git clone https://github.com/abhijatdakshesh/APIs.git
cd APIs
```

2. Start the Docker containers:
```bash
docker-compose up --build
```

The API will be available at `http://localhost:8000`

## API Endpoints

### 1. User Registration
```http
POST /api/users/register/
Content-Type: application/json

{
    "username": "testuser",
    "first_name": "John",
    "last_name": "Doe",
    "type": "agent",
    "email": "john.doe@example.com",
    "phone_number": "9876543210",
    "date_of_birth": "1990-01-01",
    "aadhar_number": "123456789012",
    "pan_number": "ABCDE1234F",
    "residential_address": "123 Main Street",
    "city": "Mumbai",
    "state": "Maharashtra",
    "pin_code": "400001",
    "total_experience_years": 5,
    "is_currently_working": true,
    "current_agencies": "ABC Agency, XYZ Corp",
    "metadata": {
        "field_recovery_experience_years": 3,
        "specialization_areas": ["Commercial", "Residential"],
        "languages_known": ["English", "Hindi", "Marathi"]
    }
}
```

### 2. Update User Metadata
```http
PUT /api/users/{username}/metadata/
Content-Type: application/json

{
    "field_recovery_experience_years": 4,
    "specialization_areas": ["Commercial", "Residential", "Industrial"],
    "languages_known": ["English", "Hindi", "Marathi", "Gujarati"]
}
```

### 3. Upload Documents
```http
POST /api/users/{username}/documents/
Content-Type: multipart/form-data

- aadhaar_file: [File]
- pan_file: [File]
- police_verification: [File]
- empanelment_letter: [File]
```

### 4. Request OTP
```http
POST /api/users/request-otp/
Content-Type: application/json

{
    "phone_number": "9876543210"
}
```

### 5. Verify OTP
```http
POST /api/users/verify-otp/
Content-Type: application/json

{
    "phone_number": "9876543210",
    "otp": "123456"
}
```

## Testing the APIs

1. **Using Postman:**
   - Import the following collection into Postman:
   ```json
   {
     "info": {
       "name": "User Management API",
       "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
     },
     "item": [
       {
         "name": "Register User",
         "request": {
           "method": "POST",
           "url": "http://localhost:8000/api/users/register/",
           "header": [
             {
               "key": "Content-Type",
               "value": "application/json"
             }
           ],
           "body": {
             "mode": "raw",
             "raw": "{\n    \"username\": \"testuser\",\n    \"first_name\": \"John\",\n    \"last_name\": \"Doe\",\n    \"type\": \"agent\",\n    \"email\": \"john.doe@example.com\",\n    \"phone_number\": \"9876543210\",\n    \"date_of_birth\": \"1990-01-01\",\n    \"aadhar_number\": \"123456789012\",\n    \"pan_number\": \"ABCDE1234F\",\n    \"residential_address\": \"123 Main Street\",\n    \"city\": \"Mumbai\",\n    \"state\": \"Maharashtra\",\n    \"pin_code\": \"400001\",\n    \"total_experience_years\": 5,\n    \"is_currently_working\": true,\n    \"current_agencies\": \"ABC Agency, XYZ Corp\",\n    \"metadata\": {\n        \"field_recovery_experience_years\": 3,\n        \"specialization_areas\": [\"Commercial\", \"Residential\"],\n        \"languages_known\": [\"English\", \"Hindi\", \"Marathi\"]\n    }\n}"
           }
         }
       }
     ]
   }
   ```

2. **Test Flow:**
   1. Register a new user using the registration endpoint
   2. Use the received username to update metadata
   3. Upload documents for the user
   4. Request OTP using the registered phone number
   5. Verify the OTP to complete the authentication

## Error Handling

The API returns appropriate HTTP status codes:
- 200: Success
- 201: Created
- 400: Bad Request
- 404: Not Found
- 500: Internal Server Error

## Database Schema

The main `UserTable` model includes:
- Basic Information (name, contact, etc.)
- Address Information
- Employment Details
- Profiling Information
- Document Uploads
- OTP Authentication

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 