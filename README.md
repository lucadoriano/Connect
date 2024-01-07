# Connect
<p align="center">
  <img alt="logo" src="https://github.com/lucadoriano/Connect/blob/main/src/app/static/img/logo.png" style="width: 377.5px; height: 57px;">
</p>
<p align="center">
  <img alt="GitHub License" src="https://img.shields.io/github/license/lucadoriano/Connect">
</p>
"Connect" is a university project developed for the courses of Web Technologies (TW6), Software Engineering and Human-Computer Interaction (A001195) and Computer Networks (RCLRC9) at the University of Naples Parthenope.

## About
Connect is a comprehensive online learning platform designed to facilitate seamless interactions between students and tutors. Through the platform, users can engage in real-time video calls, share notes, and exchange private messages, creating a collaborative and interactive learning environment.



## Technologies Used
### Frontend
- **HTML**
- **JavaScript**
- **CSS (Bootstrap)**
### Backend
- **Python (Flask)**
- **Custom Signaling Server:** - Developed a custom signaling server from scratch using the `socket` library in Python. Please note that this signaling server is part of my Computer Networks project and may not be suitable for production purposes, as it is a custom implementation and may not cover all the RFC 6455 protocol specifications. It is a work in progress, and improvements may still be needed.
### Deployment and Infrastructure
- **Docker**
### Real-Time Communication
- **WebRTC (Web Real-Time Communication)**

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.12: [Download Python](https://www.python.org/downloads/)
- Docker: [Install Docker](https://docs.docker.com/get-docker/)
- Docker Compose: [Install Docker Compose](https://docs.docker.com/compose/install/)

## Installation
If you choose to run the project using Docker Compose, you could choose skip steps: 3, 4 and 5 since you might not run the code locally.
1. Clone the repository:

   ```bash
   git clone https://github.com/lucadoriano/Connect.git
2. Navigate to the project directory:

   ```bash
   cd Connect
3. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
4. Activate the virtual environment:

    * Windows:

      ```bash
      .\venv\Scripts\activate
    * Linux/MacOS:

      ```bash
      source .venv/bin/activate
5. Install Python dependencies (located in Docker folder):

    ```bash
    cd docker/app
    pip install -r requirements.txt

## Running the Project
### Using Docker Compose
1. Make sure Docker is running on your machine.
2. Navigate to the deploy folder:

    ```bash
    cd deploy
3. Build and start the containers (it will build automatically):

    ```bash
    docker-compose up -d
4. Access the project at http://127.0.0.1/

 
5.  If you get this error "`no python application found, check your startup logs for errors`",
    simply restart the docker-compose by doing

    ```bash
     docker-compose restart

#### Stop the project
* To stop the project and its containers, run:

    ```bash
    docker-compose down
