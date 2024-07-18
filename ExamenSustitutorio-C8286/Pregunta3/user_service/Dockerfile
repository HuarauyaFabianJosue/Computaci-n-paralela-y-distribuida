FROM python:3.9-slim
WORKDIR /app
COPY user_service.py /app
RUN pip install flask
CMD ["python", "user_service.py"]