
# Django Project: CSV Uploader (Dockerized)

This project is a Django application that provides an interface to upload and process CSV files. It is containerized using Docker.

## Prerequisites

Ensure you have the following installed on your system:

- Docker
- Docker Compose (if not bundled with Docker)

## Installation

### Clone the Repository
Clone the project repository using Git:
```bash
git clone <repository-url>
cd <repository-folder>
```

### Build the Docker Image
Build the Docker image for the project:
```bash
docker-compose build
```

### Set Up Environment Variables
Create a `.env` file in the project root and configure it as required. Example `.env` file:
```
SECRET_KEY=your_secret_key
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
DATABASE_URL=sqlite:///db.sqlite3  # Update if using PostgreSQL or another database
```

## Running the Application

### Start the Docker Containers
Start the application using Docker Compose:
```bash
docker-compose up
```

### Run Migrations
Apply database migrations to set up the schema:
```bash
docker-compose exec web python manage.py makemigrations
docker-compose exec web python manage.py migrate
```

### Create a Superuser (Optional)
To access the Django admin interface, create a superuser:
```bash
docker-compose exec web python manage.py createsuperuser
```

## Usage

1. Open your browser and navigate to `http://127.0.0.1:8000/upload_csv/`.
2. Use the provided interface to upload a CSV file.
3. Process the uploaded file as per your project logic.

## API Endpoints

### 1. Upload CSV
#### Endpoint: /upload_csv/

- Method: POST
- Description: Uploads a CSV file containing movie data to the database.
- Content-Type: multipart/form-data
- File Requirements:
  - File must be a valid CSV file.
  - Maximum file size: 100 MB.
  - Required columns in the CSV file:
    - title
    - release_date (in YYYY-MM-DD format)
    - language
    - rating (decimal)
    - description

#### Request Example
curl -X POST -F "file=@movies.csv" http://127.0.0.1:8000/upload_csv/

#### Response
- Success:
  {
      "message": "File uploaded successfully"
  }
- Error (e.g., file too large or invalid format):
  {
      "error": "File size exceeds 100MB"
  }
  or
  {
      "error": "Invalid CSV format"
  }
 or
  {
      "error": "Invalid request method or file"
  }
 or
  {
      "error": "error message"
  }


---

### 2. Get Movies
#### Endpoint: /get_movies/

- Method: GET
- Description: Retrieves a paginated list of movies, with optional filtering and sorting.
- Query Parameters:
  | Parameter      | Type   | Default         | Description                                      |
  |----------------|--------|-----------------|--------------------------------------------------|
  | page           | int    | 1               | The page number to retrieve.                    |
  | page_size      | int    | 10              | Number of items per page.                       |
  | language       | string | None            | Filter movies by language.                      |
  | year           | int    | None            | Filter movies by release year.                  |
  | sort_by        | string | release_date    | Field to sort movies by (release_date, title, rating, language). |

#### Request Example
curl -X GET "http://127.0.0.1:8000/get_movies/?page=1&page_size=5&language=English&sort_by=rating"

#### Response
- Success:
  {
      "movies": [
          {
              "title": "Inception",
              "release_date": "2010-07-16",
              "language": "English",
              "rating": 8.8,
              "description": "A thief who steals corporate secrets through dream-sharing."
          },
          {
              "title": "Interstellar",
              "release_date": "2014-11-07",
              "language": "English",
              "rating": 8.6,
              "description": "A team of explorers travel through a wormhole in space."
          }
      ],
      "total_pages": 20,
      "current_page": 1,
      "page_size": 5,
      "total_movies": 100
  }
- Error (e.g., invalid sorting field or invalid page):
  {
      "error": "Invalid sort field: 'unknown_field'"
  }
  or
  {
      "error": "An unexpected error occurred."
  }

---

## CSV Format Example

The uploaded CSV file must follow this format:

| title          | release_date | language | rating | description                                      |
|-----------------|--------------|----------|--------|-------------------------------------------------|
| Inception      | 2010-07-16   | English  | 8.8    | A thief who steals corporate secrets...         |
| Interstellar   | 2014-11-07   | English  | 8.6    | A team of explorers travel through a wormhole.  |

---

## Error Handling

- Invalid File: If the uploaded file is not a valid CSV or exceeds the size limit, the API returns an appropriate error message.
- Invalid Query Parameters: If invalid parameters (e.g., invalid sort_by or page) are provided, the API returns an error message with details.


## Running Tests

To run the test suite, use the following command:
```bash
docker-compose exec web python manage.py test
```

## Deployment

For deploying to production:

1. Set `DEBUG=False` in your `.env` file.
2. Update `ALLOWED_HOSTS` with your production domain or server IP.
3. Use a production-grade database and configure it in `.env`.
4. Configure static files using Django's `collectstatic`:
   ```bash
   docker-compose exec web python manage.py collectstatic --noinput
   ```

