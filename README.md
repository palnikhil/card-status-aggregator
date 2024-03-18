# Card Status Service

## Introduction

Card Status Service is an internal API developedto provide the current status of a user's card by consolidating data from multiple partner companies. It's designed to aid support agents by offering quick access to card information.

## Technologies

- Python 3.12
- FastAPI for API development
- PostgreSQL for persistent data storage
- SQLAlchemy for database ORM
- Docker for containerization
- Docker Compose for orchestration

## Project Structure

```plaintext
card-status-service/
│
├── app/                    # Main application code
│   ├── models/             # Data models
│   │   └── card_status_model.py # Model for card status
│   ├── services/           # Business logic services
│   │   └── db/             # Database interaction services
│   │       └── card_status_db_service.py # Service for card status operations
│   ├── api.py              # API endpoints
│   └── dependencies.py     # Dependency definitions for the API
│
├── zywadb/                 # Database module
│   ├── db_service.py       # Database service for lower-level operations
│   └── session_manager.py  # Session management for DB operations
│
├── common/docker/          # Docker configurations
│   ├── postgres/           # PostgreSQL container setup
│   │   ├── data/           # Data volume for PostgreSQL
│   │   └── init_scripts/   # Initialization scripts for the database
│   └── docker-compose.yml  # Docker Compose configuration
│
├── data/                   # Data directory for CSV files and ETL
    ├── csv_files/          # Folder containing raw CSV data
    ├── etl_pipeline.py     # Script for ETL process
    └── config.py           # ETL configuration settings
```
## Approach
The API utilizes a robust ETL pipeline (etl_pipeline.py) that processes the CSV files received from partner companies, normalizing the data and populating the PostgreSQL database. 
The app contains the web API built with FastAPI, which serves the endpoint /get_card_status/{card_id} to retrieve card status by card ID.

## Why Python and Docker?
Python was chosen for its excellent support for data processing tasks and simplicity in writing web services. Docker encapsulates the service's environment, ensuring consistency across development, testing, and production setups.

## Installation & Running
Ensure Docker installed on your system. Docker Desktop should be running.
```plaintext
cd common/docker
docker-compose --profile card-status-service up --build
```
After the DB has started. Please run the etl pipeline to feed the database with all the Data from the partner companies.
```plaintext
cd data
pip install -r requirements.txt
python etl_pipeline.py
```
## API Usage
To retrieve a card's status, send a GET request to /get_card_status with the user's card ID as a path parameter.

Example
```plaintext
GET http://localhost:8080/get_card_status/ZYW7631
```
Response
```plaintext
{
    "id": 5,
    "card_id": "ZYW7631",
    "user_contact": "545576586",
    "timestamp": "2023-11-14T12:34:56",
    "status": "Delivered",
    "comment": "DELIVERED"
}
```
## Architectural Decisions
The use of Docker ensures consistent environments across development, testing, and production.
Database operations are abstracted using SQLAlchemy's ORM for ease of querying and manipulation.
A separate database module (zywadb) improves modularity and separation of concerns.

## Possible Improvements
ETL process to feed the data should be a cron job with proper exception handling mechanism. Maybe, we can try watchdog to feed the data as soon as it is put into a bucket or storage.
Currently the ETL process SQL query is prone to SQL injection. That should be made more secure
API endpoints should be secured
