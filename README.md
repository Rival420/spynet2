# Spynet Network Scanner

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Architecture](#architecture)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Configuration](#configuration)

## Introduction

**Spynet** is a comprehensive network scanning tool designed to map your network thoroughly. It leverages Python and Docker to provide a modular and scalable solution for scanning networks, detecting live hosts, open ports, and presenting the results through a web interface. This tool is ideal for security professionals and network administrators who need to gain insights into their network infrastructure.

## Features

- **Network Scanning**: Efficiently scans for live hosts and open ports on specified network ranges.
- **Database Integration**: Stores scan results in a PostgreSQL database for persistent storage and easy retrieval.
- **Web Interface**: Displays scan results via a simple web GUI built with Flask and Nginx.
- **API Access**: Provides RESTful API endpoints for accessing scan results programmatically.
- **Docker Support**: Runs seamlessly in a Docker environment, allowing easy deployment and management.
- **Modular Design**: Clean and modular codebase for easy customization and feature extensions.

## Architecture

The Spynet tool is organized into three main components:

1. **Scanner**: A Python-based service that scans the network, detects live hosts and open ports, and stores results in the database.
2. **API**: A Flask-based service that provides RESTful endpoints for accessing scan results.
3. **Web Interface**: An Nginx and Flask-based service for displaying results in a web browser.

The project structure looks like this:

```
spynet/
├── api/
│   ├── app.py
│   ├── Dockerfile
│   ├── requirements.txt
│   └── models.py
├── scanner/
│   ├── db.py
│   ├── Dockerfile
│   ├── models.py
│   ├── network.py
│   ├── requirements.txt
│   ├── scanner.py
│   ├── utils.py
│   └── wait-for-it.sh
├── web/
│   ├── Dockerfile
│   ├── index.html
│   └── nginx.conf
└── docker-compose.yml
```

## Prerequisites

Before you begin, ensure you have the following installed:

- **Docker**: To run the application in a containerized environment.
- **Docker Compose**: For orchestrating multi-container Docker applications.
- **Git**: For cloning the repository and version control.

## Installation

Follow these steps to get your instance of Spynet up and running:

1. **Clone the Repository**

   ```bash
   git clone git@github.com:yourusername/spynet.git
   cd spynet
   ```

2. **Build and Run the Docker Containers**

   ```bash
   docker-compose up --build
   ```

   This command will build the Docker images and start all services (scanner, API, web, and database).

3. **Verify the Setup**

   - Access the web interface at `http://localhost:80`.
   - The API is accessible at `http://localhost:5000`.

## Usage

1. **Network Scanning**

   The scanner service will automatically start scanning the specified network range and populate the database with results. By default, it scans the local network range.

2. **View Results**

   - Open your web browser and go to `http://localhost`.
   - The web interface will display a list of detected hosts and open ports.

3. **Access API**

   Use the following curl command to access the scan results via API:

   ```bash
   curl http://localhost:5000/api/hosts
   ```

## API Endpoints

Here are some useful API endpoints provided by the Spynet tool:

- **GET** `/api/hosts`: Retrieve a list of all scanned hosts and their open ports.
- **GET** `/api/hosts/<ip>`: Get detailed information about a specific host.
- **POST** `/api/scan`: Trigger a new network scan (optional, if implemented).

## Configuration

Configuration options for the scanner can be modified in the `scanner.py` script:

- **IP Range**: Specify the target IP or IP range for scanning.
- **Port Range**: Define the range of ports to scan.
- **Concurrency**: Adjust the maximum number of concurrent port scans.

Database connection settings can be modified in `db.py`.

### Environment Variables

- **DATABASE_URL**: URL for connecting to the PostgreSQL database.

