### Pregunta 3 (5 puntos): Crea un sistema de microservicios que incluya servicios de autenticación, gestión de usuarios y un servicio de notificaciones. Orquesta estos servicios usando Docker Compose.

Para crear un sistema de microservicios con Flask y Docker Compose, seguiremos los pasos indicados:

1. **Crear microservicios con Flask:**
   - Servicio de autenticación.
   - Servicio de gestión de usuarios.
   - Servicio de notificaciones.

2. **Configurar Dockerfiles para cada microservicio.**
3. **Configurar Docker Compose para orquestar los contenedores.**
4. **Utilizar una base de datos común (PostgreSQL).**
5. **Implementar pruebas para verificar la interacción entre los microservicios.**

### 1. Crear microservicios con Flask

#### Servicio de Autenticación (`auth_service.py`)
```python
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if data['username'] == 'admin' and data['password'] == 'admin':
        return jsonify({"message": "Login successful", "token": "123456"}), 200
    return jsonify({"message": "Invalid credentials"}), 401

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
```

#### Servicio de Gestión de Usuarios (`user_service.py`)
```python
from flask import Flask, request, jsonify

app = Flask(__name__)

users = []

@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    users.append(data)
    return jsonify({"message": "User created"}), 201

@app.route('/users', methods=['GET'])
def get_users():
    return jsonify(users), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)
```

#### Servicio de Notificaciones (`notification_service.py`)
```python
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/notify', methods=['POST'])
def notify():
    data = request.get_json()
    return jsonify({"message": f"Notification sent to {data['user']}"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003)
```

### 2. Configurar Dockerfiles para cada microservicio

#### `Dockerfile` para `auth_service`
```Dockerfile
FROM python:3.9-slim   
WORKDIR /app
COPY auth_service.py /app
RUN pip install flask
CMD ["python", "auth_service.py"]
```

#### `Dockerfile` para `user_service`
```Dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY user_service.py /app
RUN pip install flask
CMD ["python", "user_service.py"]
```

#### `Dockerfile` para `notification_service`
```Dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY notification_service.py /app
RUN pip install flask
CMD ["python", "notification_service.py"]
```

### 3. Configurar Docker Compose

#### `docker-compose.yml`
```yaml
version: '3'
services:
  auth_service:
    build:
      context: .
      dockerfile: Dockerfile.auth
    ports:
      - "5001:5001"
  user_service:
    build:
      context: .
      dockerfile: Dockerfile.user
    ports:
      - "5002:5002"
  notification_service:
    build:
      context: .
      dockerfile: Dockerfile.notification
    ports:
      - "5003:5003"
  db:
    image: postgres:13
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
      POSTGRES_DB: microservices
    ports:
      - "5432:5432"
```

### 4. Utilizar una base de datos común (PostgreSQL)
- La configuración de PostgreSQL ya está incluida en el archivo `docker-compose.yml`.

### 5. Implementar pruebas para verificar la interacción entre los microservicios

#### `test_microservices.py`
```python
import requests

def test_auth_service():
    response = requests.post('http://localhost:5001/login', json={"username": "admin", "password": "admin"})
    assert response.status_code == 200
    assert "token" in response.json()

def test_user_service():
    response = requests.post('http://localhost:5002/users', json={"name": "testuser"})
    assert response.status_code == 201
    response = requests.get('http://localhost:5002/users')
    assert response.status_code == 200
    assert len(response.json()) > 0

def test_notification_service():
    response = requests.post('http://localhost:5003/notify', json={"user": "testuser"})
    assert response.status_code == 200

if __name__ == "__main__":
    test_auth_service()
    test_user_service()
    test_notification_service()
    print("All tests passed!")
```

### Instrucciones para la ejecución:

1. **Construir y levantar los contenedores con Docker Compose:**
   ```bash
   docker-compose up --build
   ```

2. **Ejecutar las pruebas para verificar la interacción entre los microservicios:**
   ```bash
   python test_microservices.py
   ```

### Explicación del Código:

1. **Microservicios con Flask:**
   - Cada microservicio (`auth_service`, `user_service`, `notification_service`) está implementado como una aplicación Flask simple que expone algunas rutas.
   
2. **Dockerfiles:**
   - Cada microservicio tiene su propio Dockerfile que especifica cómo construir el contenedor correspondiente.

3. **Docker Compose:**
   - `docker-compose.yml` define cómo orquestar los contenedores, incluyendo los microservicios y la base de datos PostgreSQL.

4. **Pruebas:**
   - `test_microservices.py` contiene pruebas simples para verificar que los microservicios funcionan correctamente y se pueden comunicar entre sí.

### Resultado:


 