# Project Name: **Mini Web Project**

## Description
This is a little project that demonstrates how to build a simple web application using Docker and PostgreSQL. The project includes a frontend and a backend, and it uses a PostgreSQL database to store user data.

## Features
- Frontend: A simple HTML page with a form for adding, deleting, and updating user data.
- Backend: A Flask application that interacts with the PostgreSQL database.
- Docker: Containerization using Docker Compose.
- PostgreSQL: Database management system.

## Prerequisites
- Docker
- Docker Compose
- PostgreSQL

## Setup Instructions
1. Clone the repository:
   ```bash
   git clone https://github.com/JoseLorenzana272/mini-web-project.git
   cd mini-web-project
   ```

2. Build and run the Docker containers:
   ```bash
   docker compose up -d
   ```

## Usage Instructions
1. Access the frontend via: [http://localhost](http://localhost)
2. Access the backend API endpoints (just for testing):
   - `/database-test`
   - `/users`
   - `/usernames`

3. To add, delete, or update user data, use API tools like Postman.

## Database Backup and Restore (Just in case the backup.sql file does not appear on the project folder)
### Backup the Database
Run the following command to create a backup of the database (this will bring up the previously created database data):
```bash
docker exec -t database pg_dumpall -U <POSTGRES_USER> > backup.sql
```

### Restore the Database
1. Place the `backup.sql` file in the project directory.
2. Run the restoration script:
   ```bash
   chmod +x ./restoreDB.sh && ./restoreDB.sh
   ```

3. Output:
   ```
   Database restored successfully.
   ```

## Environment Variables
The project uses the following environment variables:
- `POSTGRES_USER`
- `POSTGRES_PASSWORD`
- `POSTGRES_DB`

## Directory Structure
```
/project-root
├── frontend/           # Frontend files
├── backend/            # Backend files
├── init.sql            # Initial database schema and data
├── restore_db.sh       # Database restoration script
├── docker-compose.yml  # Docker configuration
└── README.md           # Project documentation
```

## Contributing
1. Fork the repository.
2. Create a new branch for your feature:
   ```bash
   git checkout -b feature-name
   ```
3. Submit a pull request.

## License
This project is licensed under JoseLorenzana272's License.

