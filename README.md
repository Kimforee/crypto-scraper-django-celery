# crypto-scraper-django-celery

Crypto Scraper is a Django-based application designed to scrape cryptocurrency data from CoinMarketCap. It utilizes Celery for task management and Redis as a message broker to handle asynchronous tasks.

## Table of Contents

- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Contributing](#contributing)
- [License](#license)

## Installation

### Prerequisites

- Python 3.8 or higher
- Django 3.0 or higher
- Redis server
- Celery

### Steps

1. **Clone the repository**

    ```bash
    git clone https://github.com/yourusername/crypto_scraper.git
    cd crypto_scraper
    ```

2. **Create and activate a virtual environment**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3. **Install the dependencies**

    ```bash
    pip install -r requirements.txt
    ```

4. **Set up the database**

    ```bash
    python manage.py migrate
    ```

5. **Start the Django development server**

    ```bash
    python manage.py runserver
    ```

6. **Start the Redis server**

    Ensure that Redis server is running on your machine. The default configuration assumes Redis is running on localhost:6379.

7. **Start the Celery worker**

    ```bash
    python -m celery -A celery_project worker -l info -P solo
    ```

## Configuration

### Celery Configuration

Add the following configuration in your Django settings:

```python
CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
```

## Usage
To start scraping cryptocurrency data, you need to make a POST request to the start_scraping endpoint with a list of coins.

To create a job : 
curl -X POST -H "Content-Type: application/json" -d '["bitcoin"]' http://127.0.0.1:8000/api/taskmanager/start_scraping

Expected Response:
{
  "job_id": "cc65631c-6e1f-45f6-945e-61d9ea7d0c69"
}

## API Endpoints
### Start Scraping
```Endpoint:
 /api/taskmanager/start_scraping
```
Method: POST
Description: Start scraping data for the given list of coins.
Request:
Content Type: application/json
Body: ["coin1", "coin2", "coin3"]
Response:
job_id: string

### Scraping Status
```Endpoint:
 /api/taskmanager/scraping_status/<job_id>
```
Method: GET
Description: Check the status of the scraping job.

## Contributing
Contributions are welcome! Please open an issue or submit a pull request.

## License
This project is licensed under the MIT License.
