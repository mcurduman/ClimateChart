# ClimateChart

ClimateChart is a full-stack application for visualizing and analyzing weather data, featuring user management, secure API access, and a modern web interface.

### For more details you can also read the wiki

## Features

- Weather data retrieval and visualization (charts, tables)
- User registration, authentication, and account management
- API key management for secure access
- Email notifications and verification
- Modular backend architecture (Python, gRPC, MongoDB)
- Modern web client (React, TypeScript)
- Dockerized deployment and Envoy proxy 

## Architecture

- **Server**: Python backend with gRPC APIs, MongoDB integration, and modular services/repositories.
- **Envoy**: Proxy and API gateway for routing, security, and gRPC/JSON translation.
- **Web Client**: React-based frontend for interactive weather data visualization and user operations.

# Project Structure Overview

The ClimateChart project is organized into key components:

- **server/**: Python backend with gRPC APIs, MongoDB integration, and modular architecture (services, repositories, models, interceptors).
- **web-client/**: React and TypeScript frontend for weather data visualization and user management.
- **envoy/**: Envoy proxy configuration for routing and translating gRPC/JSON requests.
- **proto/**: Protocol buffer definitions for API contracts.
- **tests/**: Endpoints unit tests.
- **docker-compose.yml**: Orchestrates multi-service deployment (server, web client, Envoy).
- **README.md**: Project documentation and setup instructions.

# How to Run ClimateChart

## Prerequisites

- Docker and Docker Compose installed
- (Optional) Python and Node.js for local development

## Steps

1. **Clone the repository:**
   ```sh
   git clone https://github.com/mcurduman/ClimateChart.git
   cd ClimateChart
   ```
2. **Build and start all services using Docker Compose:**
   ```sh
   docker-compose up --build
   ```
