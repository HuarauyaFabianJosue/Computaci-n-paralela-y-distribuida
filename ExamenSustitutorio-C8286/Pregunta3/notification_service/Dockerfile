FROM python:3.9-slim
WORKDIR /app
COPY notification_service.py /app
RUN pip install flask
CMD ["python", "notification_service.py"]