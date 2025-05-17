## Date: 2025-05-08
### Step 1: Create EC2 set up all the networking variables
- Chose [Tech Stack/Tool] (e.g., Docker + Flask + jenkins)
- Created GitHub repo
- Initialized project structure

### Step 2: Database Setup docker container for postgres
- docker network created 
- docker run -d --name my-postgres --network my_network -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=admin -e POSTGRES_DB=dbuser -v pgdata:/var/lib/postgresql/data -p 5432:5432 postgres
- volume attached to host pc. pgdata:/var/lib/postgresql/data
- for volume mount -v <host_path>:<container_path>
-docker exec -it my-postgres bash
-psql -U postgres -d dbuser
-\dt
-SELECT * FROM "user";


### Flask application container:
- docker run -d --name flask-app --network my_network -e DB_USER=postgres -e DB_PASSWORD=admin -e DB_NAME=dbuser -e DB_HOST=my-postgres -p 5000:5000 flaskapp

### now the docker image size for the flask app is more than a gb. I will use multistaging with distroless for automation and to improve security.

```bash 
# Stage 1 - Builder
FROM python:3.9-slim as builder

WORKDIR /app

COPY . .

# Install pip and virtualenv
RUN pip install --upgrade pip virtualenv

# Create virtual environment and install dependencies
RUN virtualenv /venv && \
    /venv/bin/pip install -r requirements.txt

# Stage 2 - Distroless
FROM gcr.io/distroless/python3-debian12

WORKDIR /app

# Copy virtualenv from builder
COPY --from=builder /venv /venv
COPY --from=builder /app /app

ENV PATH="/venv/bin:$PATH"
ENV PYTHONPATH="/venv/lib/python3.9/site-packages"

EXPOSE 5000

ENTRYPOINT ["python3"]
CMD ["app.py"]
```

###error
```bash
docker logs a0083
Traceback (most recent call last):
  File "/app/app.py", line 17, in <module>
    db = SQLAlchemy(app)
         ^^^^^^^^^^^^^^^
  File "/venv/lib/python3.9/site-packages/flask_sqlalchemy/extension.py", line 278, in __init__
    self.init_app(app)
  File "/venv/lib/python3.9/site-packages/flask_sqlalchemy/extension.py", line 374, in init_app
    engines[key] = self._make_engine(key, options, app)
                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/venv/lib/python3.9/site-packages/flask_sqlalchemy/extension.py", line 665, in _make_engine
    return sa.engine_from_config(options, prefix="")
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/venv/lib/python3.9/site-packages/sqlalchemy/engine/create.py", line 823, in engine_from_config
    return create_engine(url, **options)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<string>", line 2, in create_engine
  File "/venv/lib/python3.9/site-packages/sqlalchemy/util/deprecations.py", line 281, in warned
    return fn(*args, **kwargs)  # type: ignore[no-any-return]
           ^^^^^^^^^^^^^^^^^^^
  File "/venv/lib/python3.9/site-packages/sqlalchemy/engine/create.py", line 602, in create_engine
    dbapi = dbapi_meth(**dbapi_args)
            ^^^^^^^^^^^^^^^^^^^^^^^^
  File "/venv/lib/python3.9/site-packages/sqlalchemy/dialects/postgresql/psycopg2.py", line 696, in import_dbapi
    import psycopg2
  File "/venv/lib/python3.9/site-packages/psycopg2/__init__.py", line 51, in <module>
    from psycopg2._psycopg import (          
```

docker build -f ./Docker_multistage_Distroless -t flask_app_mini .

```bash
docker run -d --name flask-app --network my_network -e DB_USER=postgres -e DB_PASSWORD=admin -e DB_NAME=dbuser -e DB_HOST=my-postgres -p 5001:5000 flaskapp:latest
```

```bash
docker run -d --name my-postgres --network my_network -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=admin -e POSTGRES_DB=dbuser -v pgdata:/var/lib/postgresql/data -p 5432:5432 postgres
```

With above docker file I am using docker multistaging and distroless image to reduce the image size and security of the container as there is no linux file system present in docker container, so there is no way someone can get into that container and make changes. GPT HAS TO ADD MORE DEATILS TO IT.

Now, To automate it so that I don't have to add environment variables to the run docker commands twice to up the pSQL and flask app container.

---
### big time fail to implement multistage and distroless 

### slim image dockerfile working fine.

Dockerfile_mini2

# DOCKER COMPOSE WITHOUT HEALTHCHECK

```bash
version: '3.8'

services:
  db:
    image: postgres
    container_name: my-postgres
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: admin
      POSTGRES_DB: dbuser
    volumes:
      - pgdata:/var/lib/postgresql/data
    ports:
      - "5432:5432"
    networks:
      - my_network

  web:
    image: flaskapp
    container_name: flask-app
    environment:
      DB_USER: postgres
      DB_PASSWORD: admin
      DB_NAME: dbuser
      DB_HOST: my-postgres
    ports:
      - "5000:5000"
    networks:
      - my_network
    depends_on:
      - db

volumes:
  pgdata:

networks:
  my_network:

```

# DOCKER COMPOSE WITH HEALTH CHECK

```bash
version: '3.8'

services:
  db:
    image: postgres
    container_name: my-postgres
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: admin
      POSTGRES_DB: dbuser
    volumes:
      - pgdata:/var/lib/postgresql/data
    ports:
      - "5432:5432"
    networks:
      - my_network
    restart: always
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 10s
      timeout: 5s
      retries: 5
      start_period: 10s

  web:
    image: flaskapp
    container_name: flask-app
    environment:
      DB_USER: postgres
      DB_PASSWORD: admin
      DB_NAME: dbuser
      DB_HOST: my-postgres
    ports:
      - "5000:5000"
    networks:
      - my_network
    depends_on:
      db:
        condition: service_healthy
    restart: always
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:5000"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 10s

volumes:
  pgdata:

networks:
  my_network:


The --remove-orphans flag in the docker compose down command is used to remove containers that were part of a previous Docker Compose setup but are no longer defined in the current docker-compose.yml file.

Explanation:
Orphan containers: These are containers that were created by a previous docker-compose run but are not included in the current docker-compose.yml file. For example, if you removed or renamed a service in the docker-compose.yml file, the container associated with that service would become an "orphan."

--remove-orphans: This option ensures that all orphaned containers are stopped and removed when running docker compose down. It essentially helps clean up leftover containers that are not part of the current Docker Compose project.

Example:
If your docker-compose.yml initially had services for web and db, and you later removed the db service from the file, running docker compose down --remove-orphans would:

Stop and remove the web container (since it’s part of the current compose setup).

Stop and remove the db container, which is no longer part of the updated docker-compose.yml file (thus considered an orphan).

Without --remove-orphans, the db container would persist even though it’s no longer defined in the configuration.

```

### PRE REQUISITES 

- AWS CLI INSTALLED
- AWS LOGIN
- CREATE ECR
- JENKINS CREDINTIALS SETUP FOR AWS
- aws-credentials install plugin in jenkins

  
### JENKINS PIPELINE 

pipeline {
    agent any
    
    environment {
        AWS_REGION = 'us-east-1'
        ECR_REPO = '021891604768.dkr.ecr.us-east-1.amazonaws.com/flaskapp'
        IMAGE_TAG = 'latest'
        IMAGE_NAME = "${ECR_REPO}:${IMAGE_TAG}"
    }

    stages {
        stage('Git Clone') {
            steps {
                echo 'Cloning the repository...'
                git url: "https://github.com/Prabhjot2406/Two_Tier_WebPortfolio_FlaskApp.git", branch: "main"
            }
        }

        stage('Login to AWS ECR') {
            steps {
                withCredentials([[
                    $class: 'AmazonWebServicesCredentialsBinding',
                    credentialsId: 'aws-creds-id',
                    accessKeyVariable: 'AWS_ACCESS_KEY_ID',
                    secretKeyVariable: 'AWS_SECRET_ACCESS_KEY'
                ]]) {
                    sh '''
                        aws ecr get-login-password --region $AWS_REGION | \
                        docker login --username AWS --password-stdin $ECR_REPO
                    '''
                }
            }
        }
        
        stage('Image delete') {
            steps {
                echo 'deleting the existing image'
                sh 'docker rmi -f $IMAGE_NAME'
                sh 'docker ps'
            }
        }

        stage('Pull Image') {
            steps {
                echo 'Pulling the Docker image from ECR...'
                sh 'docker pull $IMAGE_NAME'
                sh 'docker ps'
            }
        }
        stage('service down') {
            steps {
                echo 'Turn down running service'
                sh 'docker-compose down --remove-orphans'
'
            }
        }
         stage('service up') {
            steps {
                echo 'service up'
                sh 'docker compose up -d --build'   
            }
        }
    }
}




