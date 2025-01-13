# Development stage
FROM python:3.10-alpine AS development

WORKDIR /python-docker

# Install necessary build dependencies for Alpine
RUN apk add --no-cache gcc musl-dev libffi-dev

# Copy the requirements file and install dependencies
COPY requirements.txt requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Run tests (adjust `test_app.py` if not applicable)
CMD ["python3", "test_app.py", "-v"]

# Production stage
FROM python:3.10-alpine AS production

WORKDIR /python-docker

# Install necessary runtime dependencies for Alpine
RUN apk add --no-cache libffi libressl

# Copy the requirements file and install dependencies
COPY requirements.txt requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy only necessary application files
COPY . .

# Create a new user with UID 10016 for security
RUN addgroup -g 10016 choreo && \
    adduser --disabled-password --no-create-home --uid 10016 --ingroup choreo choreouser

# Switch to the non-root user
USER 10016

# Expose the Flask default port
EXPOSE 5000

# Start the Flask application
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
