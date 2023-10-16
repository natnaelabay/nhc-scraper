# nhc.gov.cn Scraper

This project is a Django-based RESTful API(http://172.105.83.7/) with Swagger documentation and a a web scraper for http://www.nhc.gov.cn/. 

## Getting Started

These instructions will help you get a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

To run this project, you need to have the following software installed:

- Python (3.x)

### Installing

You can install the required Python packages using `pip`:

```bash
pip3 install -r requirements.txt
```


## Scraper

I did not use a headless browser [selenium or playwright] as we discussed so in order to make the scraper work we need to steal some cookies from our browser.

### Video setup links

1. api
2. scraper

### Steps to run the api locally

```bash
cd scraperApi

python3 manage.py migrate

python3 manage.py createsuperuser (it will ask you for username and password)

python3 manage.py runserver

# go to http://127.0.0.1:8000/admin and put in your username and password to see the dashboard
```


### Steps to run the scraper locally

 1. ```py
    python runner.py
    ```
2. After copying the cookies from your browser paste it in the prompt from the above command
3. It will start scrapping and populating the database
4. If you can use http://127.0.0.1/ to see the details