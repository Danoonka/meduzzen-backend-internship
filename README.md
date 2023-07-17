## Running FastAPI Application and pytest Tests

Installing Dependencies
Before running the FastAPI application, you need to install all the necessary dependencies. It is recommended to use a virtual environment to isolate the dependencies.

1. Create and activate a virtual environment:

```
python -m venv myenv
source myenv/bin/activate
```

2. Install the dependencies listed in the requirements.txt file:

```
pip install -r requirements.txt
```

## Running the FastAPI Application
You can run the FastAPI application using the uvicorn command. Specify the module that contains your application and the name of the FastAPI application object. For example, if your application is in the main module and the application object is named app, execute the following command:

```
uvicorn main:app --reload
```

The --reload flag enables automatic server reloading when code changes are detected. You can change the port and host by adding the --host and --port flags with the corresponding values.

After a successful launch, the FastAPI application will be available at http://localhost:8000 (unless a different port is specified).

## Running Tests with pytest
To run tests in your FastAPI application, you can use pytest. Your tests should be located in a separate directory (e.g., tests), and their names should start with the test_ prefix.

Make sure your tests are placed in a separate directory, such as tests.

In the activated virtual environment, execute the following command:

```
pytest
```

pytest will automatically discover and run your tests. You can also specify the path to the directory or file containing the tests if they are located elsewhere.

## Running App using docker

1. Build the Docker image

```
docker build -t myapp .
```
This will create a Docker image named "myapp" based on the provided Dockerfile.

2. Run the Docker container
```
docker run -d -p 8000:8000 myapp
```

3. Run tests in Docker

```
docker exec -it <container id> pytest
```

## Migrations 

### To create migrations run:

```
    alembic revision --autogenerate -m <migration name>
```

###  To use migrations run:

```
    alembic upgrade <hash of migration>
```