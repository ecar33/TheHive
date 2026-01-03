# TheHive (Flask Message Board) – Local Run Guide (Docker Artifact)

TheHive is a Flask-based message board app with user authentication and persistent storage via SQLite. The project is containerized with Docker and includes a GitHub Actions CI pipeline that runs tests + linting and exports a Docker image artifact for reproducible runs.

## What’s Included

### Application
- Flask app (app factory pattern: `create_app()`)
- User authentication (session-based via Flask-Login)
- SQLite persistence (database file stored on disk)
- Blueprints for modular routes (auth/main/message)
- Basic security practices (CSRF protection via extension + input validation)

### CI Pipeline (GitHub Actions)
On push to `main/master`, CI:
- uses a pinned Python runtime
- installs dependencies
- runs unit tests
- runs Ruff linting
- builds a Docker image
- exports the image as an artifact (`docker save`)

## Run Using the Latest CI Artifact (Recommended)

### 1) Download the latest Docker image artifact
From GitHub Actions, download the artifact file (example): `thehive-image.tar`

Place it in the project directory.

### 2) Load the image into your local Docker image store
```bash
docker load -i thehive-image.tar
```

Confirm the image exists:
```bash
docker image ls | grep thehive
```

> Note: The image name/tag depends on how it was built. If it’s `thehive:ci`, the commands below will work as-is.

### 3) Create a local data directory (for persistent SQLite storage)
```bash
mkdir -p data
```

### 4) Initialize the database (one-time, safe to re-run if idempotent)
This runs the Flask CLI init command inside a disposable container, but writes the DB to your local `./data` folder via a volume mount.

```bash
docker run --rm \
  -v "$PWD/data:/app/data" \
  -e SQLALCHEMY_DATABASE_URI=sqlite:////app/data/app.db \
  thehive:ci flask initdb
```

### 5) Run the web app (Gunicorn inside the container)
```bash
docker run --rm \
  -p 8000:8000 \
  -v "$PWD/data:/app/data" \
  -e SQLALCHEMY_DATABASE_URI=sqlite:////app/data/app.db \
  thehive:ci
```

Open: http://localhost:8000

## Alternative: Build Locally Instead of Using CI Artifact
```bash
docker build --no-cache -t thehive:ci .
mkdir -p data

docker run --rm \
  -v "$PWD/data:/app/data" \
  -e SQLALCHEMY_DATABASE_URI=sqlite:////app/data/app.db \
  thehive:ci flask initdb

docker run --rm \
  -p 8000:8000 \
  -v "$PWD/data:/app/data" \
  -e SQLALCHEMY_DATABASE_URI=sqlite:////app/data/app.db \
  thehive:ci
```