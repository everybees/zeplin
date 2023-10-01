# Crypto Address API

This project is a FastAPI application to generate and list cryptocurrency addresses. It uses MongoDB as a database.

## Running the Application
Ensure Docker and Docker-Compose are installed and then run:

```sh
docker-compose up --build
```

## API Documentation
The API documentation is available at http://localhost:8000/docs


```md
/project_root
    /app
        /api
            __init__.py
            addresses.py  # For address-related routes
            api.py  # For including all the routers
        /core
            config.py  # Configuration settings
        /db
            __init__.py
            mongodb.py  # MongoDB connection and helpers
        /models
            __init__.py
            addresses.py  # Pydantic models for addresses
        /services
            __init__.py
            crypto_service.py  # For Crypto-related operations
        /tests  # For test cases
        main.py  # Main application entry point
    Dockerfile
    docker-compose.yml
    requirements.txt
```