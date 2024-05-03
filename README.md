# Library Operations

## Guide for Building and Running Docker Containers
This document provides step-by-step instructions for running a FastAPI application within Docker containers.

### Step 1: Install Docker
Download and install Docker on your computer. Docker Desktop is available for Windows, macOS, or Linux. You can download Docker Desktop from the Docker website.

### Step 2: Clone the Project

Clone the FastAPI project from GitHub or any source repository, or download the project to your computer.

    git clone <project_git_url>

    cd <project_directory>

###  Step 3: Edit Docker Files
Edit the Dockerfile and docker-compose.yml files in the project. These files specify how the application will run and manage dependencies within Docker containers.

### Step 4: Build Docker Containers
To build the Docker containers, run the following command:

    docker-compose build

This command builds the images for the containers using the Docker files.

### Step 5: Start Docker Containers
To start the containers, run the following command:

    docker-compose up

### Step 6: Access the Application
Once the application has started successfully, you can access it in your browser or API client. 

By default, the application will run at [http://localhost:8000/docs](http://127.0.0.1:8000/docs).

Click the link after starting docker container, you can find the endpoints.

### Step 7: Stop the Containers
To stop the application, run the following command:

    docker-compose down

## Configuring and Using Celery-Beat for Task Scheduling
In project structure, you can find celery configurations in celery.py file under core folder.

###  Configuration of Celery-Beat: 
Celery configurations is in celery.py under core folder. 

### Defining Tasks: 
Tasks are written in tasks.py under the main structure in project folder.

Tasks are marked with the @app.task decorator and contain the code to be executed.

    send_overdue_reminder_email() and generate_checkout_statistic_report()

You can see the schedule in variable
      
        celery_app.conf.beat_schedule 


### Running Tasks:

When you build and run the docker containers. Project automatically build the dependencies and run commands.
You can find in docker-compose.yml file.
