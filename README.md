# De-Duke

De-Duke is a modern full-stack real estate platform connecting property seekers with hosts. It features a Flutter-based mobile application and a robust Django backend deployed on AWS.

## Features

*   **Property Listings**: Support for Commercial (Sales/Lease) and Shortlet (Rent) properties.
*   **Geospatial Search**: Find properties near you using advanced PostGIS location queries.
*   **Identity Verification**: Secure host verification using government IDs (NIN, BVN, Passport).
*   **Real-time Chat**: Instant messaging between buyers and sellers via AWS AppSync.
*   **Secure Payments**: Integrated Paystack checkout for safe transactions.

## Tech Stack

### Frontend
*   **Framework**: Flutter (Mobile)

### Backend
*   **Framework**: Django Rest Framework (DRF)
*   **Database**: PostgreSQL (with PostGIS)
*   **Real-time**: AWS AppSync EventApi
*   **Task Queue**: Celery with Redis

### Infrastructure (AWS)
*   **IaC**: AWS Cloud Development Kit (CDK)
*   **Compute**: EC2 Auto Scaling Groups
*   **Networking**: Application Load Balancer (ALB)
*   **Storage**: S3 (Media), RDS (Database)
*   **Security**: Secrets Manager, IAM

## Local Development Setup

The project uses Docker Compose for local development.

### Prerequisites
*   Docker & Docker Compose
*   Python 3.12+
*   Make (optional, for convenience commands)

### Getting Started

1.  **Clone the repository**:
    ```bash
    git clone <repository-url>
    cd de-duke
    ```

2.  **Environment Variables**:
    Create a `.env.dev` file in `de_duke/apis/drf/backend/` based on the example.

3.  **Run with Docker**:
    Navigate to the drf directory and start the services.
    ```bash
    cd de_duke/apis/drf
    docker compose -f compose.dev.yaml up --build -d
    ```

4.  **Access the API**:
    The API will be available at `http://localhost:8000/`.

## Deployment

Deployment is managed via AWS CDK.

1.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

2.  **Deploy Stack**:
    ```bash
    cdk deploy --profile <your-aws-profile>
    ```
