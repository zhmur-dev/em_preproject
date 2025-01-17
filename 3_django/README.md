# dog_api

---

## Description

**dog_api** is a sample RESTful API service that provides the following API endpoints to set up a database of dogs and dog breeds:
```commandline
/api/breeds/
/api/breeds/<id>
/api/dogs/
/api/dogs/<id>
```

---

## Installation and start-up

- Clone the repository and change directory:
```commandline
git clone https://github.com/zhmur-dev/em_preproject.git
cd em_preproject/3_django/
```

- Copy `.env.example` to `.env` and change it, if necessary
```commandline
cp .env.example .env
```

- For your first start, execute the following command:
```commandline
docker compose -f docker-compose-first-start.yml up --build
```
The first-start docker-compose script will automatically apply required migrations, copy static files and create a superuser with login `admin` and password `admin`.️

> ☝️ Make sure [Docker Desktop](https://www.docker.com/products/docker-desktop/) is installed, configured and running on your machine before running this command!

- If this is not your first start of this project, execute the following command:
```commandline
docker compose up
```

- Open your browser and go to `localhost:8000`

---

## Usage
This project has no frontend as such, but you can work with the database from any of the available interfaces:
- Django admin panel
- Django REST Framework API Root
- Swagger UI

The complete list of endpoints is as follows:
- `localhost:8000/admin/` - Django admin panel
- `localhost:8000/api/` - Django REST Framework API Root
- `localhost:8000/api/breeds/` - API endpoint for GET (list) and POST methods of Breed model
- `localhost:8000/api/breeds/<id>` - API endpoint for GET (detail), PUT, PATCH and DELETE methods of Breed model
- `localhost:8000/api/dogs/` - API endpoint for GET (list) and POST methods of Dog model
- `localhost:8000/api/dogs/<id>` - API endpoint for GET (detail), PUT, PATCH and DELETE methods of Dog model
- `localhost:8000/api/schema/` - Download API specification
- `localhost:8000/swagger/` - View API specification in Swagger UI

>  ☝️ Make sure that you have necessary permissions before taking action!
>
> - You need to log in as Administrator to apply POST, PUT, PATCH and DELETE methods to model Breed.
> - You need to be authorized to apply POST, PUT, PATCH and DELETE methods to model Dog.
> - You do not need authorization to apply GET methods to any model.

---

## API requests examples

Use one of the following methods to see the examples of all possible API requests.

- If the project is not running:
1. Go to https://editor.swagger.io/.
2. Select "File" from top menu and choose "Import file".
3. Open `/openapi_files/schema.yaml` from root directory of the project.
4. The complete list of examples is now in your browser!

- If the project is running:
1. Go to https://localhost:8000/swagger/.
2. The complete list of examples is now in your browser!

---

Developed by Alexander [zhmur-dev](https://github.com/zhmur-dev/) Zhmurkov in 2025