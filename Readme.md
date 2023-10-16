# nhc.gov.cn Scraper

This project is a web scraper and a Django backend to manage the scraped data with Swagger documentation for http://www.nhc.gov.cn/. 

project setup link: [video](https://share.vidyard.com/watch/kbskiHZLAAvwif7kHXDuyr?)

## To explore the scraped data you can use the remote server

- http://172.105.83.7/ - there is swagger installed
or
- http://172.105.83.7/admin - if you have the correct credentials [I will share them with you]


## Getting Started

These instructions will help you get a copy of the project up and running on your local machine for development and testing purposes.


## Prerequisites to set it up locally

To run this project, you need to have the following software installed:

- Python (3.x)

### Installing

1. Clone the repository

```bash
git clone https://github.com/natnaelabay/nhc-scraper.git
```

2. Create a virtual environment

```bash
# linux
python3 -m venv venv

# windows
python -m venv venv

```
3. Activate virtual environment

```bash

# linux
source venv/bin/activate

# windows
venv\Scripts\activate
```

4. Install requirements
```bash

# linux
pip3 install -r requirements.txt

# windows
pip install -r requirements.txt
```

### Steps to run the api locally

```bash

# Linux
cd scraperApi

python3 manage.py migrate

python3 manage.py createsuperuser (it will ask you for username and password)

python3 manage.py runserver

# go to http://127.0.0.1:8000/admin and put in your username and password to see the dashboard

#################################

# Windows machine
cd scraperApi

python manage.py migrate

python manage.py createsuperuser (it will ask you for username and password)

python manage.py runserver

# go to http://127.0.0.1:8000/admin and put in your username and password to see the dashboard


```

## Scraper

I did not use a headless browser or frameworks like [selenium or playwright] so in order to make the scraper work we need to steal some cookies from our browser.

### Steps to run the scraper locally

 1. ```py
    python runner.py
    ```
2. After copying the cookies from your browser paste it in the prompt from the above command (in the network tab from one of the start_urls I have explained this in detail in the video)
3. It will start scrapping and populating the database
4. If you can use http://127.0.0.1:8000/ to see the details using swagger or http://127.0.0.1:8000/admin using the dashboard
