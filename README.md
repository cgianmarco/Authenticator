## Local API Startup

To start the API locally, follow these steps:

1. Clone the project and navigate to the project folder.

2. Run the following command to build and start the API:

    ```
    docker-compose up --build
    ```

# API Documentation

## Register User
Endpoint: `/v1/register`

Method: `POST`

Registers a new user.

Request Body:
```json
{
    "email": "string",
    "password": "string",
    "enable_tfa": "boolean (optional, default is false)"
}
```

Response:

```json
{
    "success": true,
    "message": "User registered successfully."
}
```



## Login
Endpoint: `/v1/login`

Method: `POST`

Logs in a user.

Request Body:
```json
{
    "username": "string",
    "password": "string"
}
```


Response:

If enable_tfa is NOT enabled on registration

```json
{
    "token": "string"
}
```
If enable_tfa is enabled on registration

```json
{
    "success": true,
    "message": "An OTP has been sent to your email. Please provide the OTP using /validate_otp to login."
}
```

## Validate OTP
Endpoint: `/v1/validate_otp`

Method: `POST`

Validates a one-time password (OTP).

Request Body:
```json
{
    "email": "string",
    "otp": "string"
}
```

Response:

```json
{
    "token": "string"
}
```


## Get Users
Endpoint: `/v1/users`

Method: `GET`

Retrieves all users (only for testing purposes).

Response:

```json
{
    "users": [
        {
            "id": "integer",
            "email": "string",
            "_password": "string",
            "enable_tfa": "boolean",
            "secret_key": "string"
        },
        ...
    ]
}
```

## Error Cases

### Invalid Credentials Body
If the credentials are not invalid, the API will respond with a `401 Unauthorized` status code and the following response:

```json
{
    "success": false,
    "message": "Invalid credentials."
}
```

### Validation Error Body
If the request body is missing or invalid, the API will respond with a `400 Bad Request` status code and the following response:

```json
{
    "success": false,
    "message": "Validation error. Check the request payload."
}
```

### User Registration Failed
If the user is already registered, the API will respond with a `409 Conflict` status code and the following response:

```json
{
    "success": false,
    "message": "User already exists."
}
```

### Rate Limit Exceeded
If the user exceeds the rate limit for API requests, the API will respond with a `429 Too Many Requests` status code and the following response:

```json
{
    "success": false,
    "message": "Rate limit exceeded. Please try again later."
}
```

### Internal Server Error
If there is an error while processing the request, the API will respond with a `500 Internal Server Error` status code and the following response:

```json
{
    "success": false,
    "message": "Internal server error"
}
```
