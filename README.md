
# FastAPI Web Application with MySQL and Docker

This is a web application built using FastAPI, SQLAlchemy, and MySQL, following the MVC design pattern. The application is containerized using Docker and supports database migrations with Alembic.

## Features

- User signup and login with JWT token authentication
- Create, retrieve, and delete posts
- Token-based authentication for protected endpoints
- Database migrations with Alembic
- Dockerized setup for easy deployment

## Prerequisites

- Docker
- Docker Compose

## Installation

1. **Clone the repository:**

    ```sh
    git clone https://github.com/your-username/your-repo-name.git
    cd your-repo-name
    ```

2. **Build and start the containers:**

    ```sh
    docker-compose up --build
    ```

3. **Apply database migrations:**

    ```sh
    docker-compose run app alembic upgrade head
    ```

## Configuration

Configuration is managed through environment variables. The following environment variables are used:

- `DATABASE_URL`: The URL for the database connection.
- `SECRET_KEY`: The secret key for JWT token generation.
- `ALGORITHM`: The algorithm used for JWT token encoding.

These variables are set in the `docker-compose.yml` file.

## Usage

Once the containers are running, the application will be accessible at `http://localhost:80`.

### Endpoints

- **Signup:** `POST /auth/signup`
  - Request Body: `{ "email": "user@example.com", "password": "password" }`
  - Response: `{ "id": 1, "email": "user@example.com" }`

- **Login:** `POST /auth/login`
  - Request Body: `{ "email": "user@example.com", "password": "password" }`
  - Response: `{ "access_token": "token", "token_type": "bearer" }`

- **Add Post:** `POST /posts/addpost`
  - Request Body: `{ "text": "This is a post" }`
  - Headers: `Authorization: Bearer token`
  - Response: `{ "id": 1, "text": "This is a post", "user_id": 1 }`

- **Get Posts:** `GET /posts/posts`
  - Headers: `Authorization: Bearer token`
  - Response: `[{ "id": 1, "text": "This is a post", "user_id": 1 }]`

- **Delete Post:** `DELETE /posts/deletepost/{post_id}`
  - Headers: `Authorization: Bearer token`
  - Response: `{ "detail": "Post deleted" }`

## Project Structure

```
/my_fastapi_app
|-- Dockerfile
|-- docker-compose.yml
|-- app
|   |-- __init__.py
|   |-- main.py
|   |-- config.py
|   |-- models
|   |   |-- __init__.py
|   |   |-- user.py
|   |   `-- post.py
|   |-- schemas
|   |   |-- __init__.py
|   |   |-- user.py
|   |   `-- post.py
|   |-- services
|   |   |-- __init__.py
|   |   |-- auth.py
|   |   `-- post.py
|   `-- routes
|       |-- __init__.py
|       |-- auth.py
|       `-- post.py
|-- alembic
|   |-- env.py
|   |-- README
|   |-- script.py.mako
|   `-- versions
|-- alembic.ini
|-- requirements.txt
```


## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any changes.

## License

This project is licensed under the MIT License.
