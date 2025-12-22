# Use an official Python image
FROM python:3.11

# Set working directory
WORKDIR /app

# Copy app files
COPY . .

# Install dependencies
RUN pip install -r requirements.txt

# For deploying with Flask
# ENV FLASK_APP=main.py
# ENV FLASK_CONFIG=development
# ENV FLASK_APP=main:app
# CMD ["flask", "run", "--host", "0.0.0.0", "--port", "8000"]

EXPOSE 5000

# Run the app
CMD ["gunicorn", "main:app", "-b", "0.0.0.0:8000"]