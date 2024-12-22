FROM python:3.12-slim

# Set working directory
WORKDIR /code

# Install dependencies and create virtual environment
RUN python -m venv /env

# Activate virtual environment and install dependencies
RUN /env/bin/pip install --upgrade pip
COPY requirements.txt .
RUN /env/bin/pip install -r requirements.txt

# Copy the project files into the container
COPY . .

# Expose port 8000 for Django
EXPOSE 8000

# Run the Django development server using the virtual environment
CMD ["/env/bin/python", "manage.py", "runserver", "0.0.0.0:8000"]