FROM python:3.14.7-slim
# Set the working directory
WORKDIR /app
# Install dependencies
COPY requirements.txt .
# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt
# Copy the rest of the application code
COPY . .
# Run as non-root
RUN useradd -m appuser && chown -R appuser /app
# Switch to the non-root user
USER appuser
# Set the entry point for the container
CMD ["gunicorn", "--bind", "0.0.0.0:5001", "app:app"]
# Expose the port the app runs on
EXPOSE 5001