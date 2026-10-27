# Parent image
FROM python:3.9

# Working directory inside the image
WORKDIR /code

# Copy requirements first so Docker can cache the install layer
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Copy the application code
COPY ./app /code/app

# The port the app listens on
EXPOSE 8080

# Start the server
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]