# Use an official Python image
FROM python:3.12

# Set working directory
WORKDIR /app

# Copy app files
COPY . .

# Install dependencies
RUN pip install -r requirements.txt

ENV FLASK_APP=app.py
ENV FLASK_CONFIG=development

EXPOSE 5000

# Run the app
CMD ["flask", "run", "--host=0.0.0.0"]