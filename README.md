## Date: 2025-05-08
### Step 1: Create EC2 set up all the networking variables
- Chose [Tech Stack/Tool] (e.g., Docker + Flask)
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

-
-
```bash
# ------------------- Stage 1: Build Stage ------------------------------
FROM python:3.9 AS builder

WORKDIR /app

# Copy and install Python dependencies
COPY . .
RUN pip install -r requirements.txt --target=/app/deps

# ------------------- Stage 2: Final Stage ------------------------------
FROM gcr.io/distroless/python3-debian12

WORKDIR /app

# Copy dependencies and application code from the builder stage
COPY --from=builder /app/deps /app/deps
COPY /app .

EXPOSE 5000

CMD ["python", "app.py"]
```

docker build -f ./Docker_multistage_Distroless -t flask_app_mini .


docker run -d --name flask-app --network my_network -e DB_USER=postgres -e DB_PASSWORD=admin -e DB_NAME=dbuser -e DB_HOST=my-postgres -p 5001:5000 flaskapp:latest

```bash
# Stage 1 - Builder
FROM python:3.9-slim as builder

WORKDIR /app

COPY . .

# Create a virtual environment
RUN python -m venv /opt/venv

# Upgrade pip and install dependencies into the venv
RUN /opt/venv/bin/pip install --upgrade pip && \
    /opt/venv/bin/pip install -r requirements.txt

# Stage 2 - Distroless runtime
FROM gcr.io/distroless/python3-debian12

WORKDIR /app

COPY --from=builder /opt/venv /opt/venv
COPY --from=builder /app /app

# Activate venv
ENV PATH="/opt/venv/bin:$PATH"

EXPOSE 5000

ENTRYPOINT ["python3"]
CMD ["app.py"]
```

# or 

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

#error
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
# big time fail to implement multistage and distroless 

# AGAIN

  docker run -d --name my-postgres --network my_network -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=admin -e POSTGRES_DB=dbuser -v pgdata:/var/lib/postgresql/data -p 5432:5432 postgres
5be79138a78cf9017a4e82c6ffde448a700b40bfde3483eab409fbfad713cf22

docker run -d --name flask-app --network my_network -e DB_USER=postgres -e DB_PASSWORD=admin -e DB_NAME=dbuser -e DB_HOST=my-postgres -p 5000:5000 flaskapp
b1d18140ca5b127aab4fe4b131e59105a9cd594fa39bc85c617368a668b5869a
---

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


```
