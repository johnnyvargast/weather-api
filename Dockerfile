FROM python:3.7.4-slim-stretch

WORKDIR /app

# Dependencies
COPY requirements.txt /app/
RUN  pip install --no-cache-dir -r requirements.txt 

# Source code
COPY backend/ backend
COPY apps/ apps
COPY local_storage/ local_storage
COPY manage.py .

# Permissions to execute
COPY entrypoint.sh .
RUN chmod +x entrypoint.sh
ENTRYPOINT [ "/app/entrypoint.sh" ]

# Default execution
EXPOSE 9000
CMD ["python3", "manage.py", "runserver", "0.0.0.0:9000"]
