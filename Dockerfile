FROM python:3.8.2-slim-buster

# Create workdir
COPY ./src /src/
WORKDIR /src

# Copy and install the requirements.txt
COPY requirements.txt .
RUN pip install -r requirements.txt

# Run the server
CMD uvicorn api.main:app --host 0.0.0.0 --port 1234 --timeout-keep-alive 500 --workers 2
