# Bucket List Api

[![Build Status](https://travis-ci.org/zmwas/bucketlist-api.svg?branch=develop)](https://travis-ci.org/zmwas/bucketlist-api)   [![Coverage Status](https://coveralls.io/repos/github/zmwas/bucketlist-api/badge.svg?branch=develop)](https://coveralls.io/github/zmwas/bucketlist-api?branch=develop)

# Introduction 

A bucket list application that allows you to create, retrieve, update and delete bucketlists.

### Dependencies
Before installing the application type the following:
  ```
  brew install python 2.7 on MacOS
  sudo apt-get install python 2.7 on Linux
  brew install postgresql on MacOs
  sudo apt-get install postgresql postgresql-contrib on linux
  psql postgres
  create database bucketlist;
  \q
  pip install virtualenv virtualenvwrapper
  ```

### Installation
Open your terminal and type:
```
git clone https://github.com/zmwas/bucketlist-api
git checkout develop
mkvirtualenv api
cd bucketlist-api
pip install -r requirements.txt
```
Before running the application type:

```
export SECRET='YOUR-SECRET-HERE'
export TEST-DB='postgresql://localhost/test_db'
export ENVIRONMENT='development'
```
Create migrations
```
python manage.py db init
python manage.py db migrate
python manage.py db upgrade
```
To run the application type:
```
python manage.py runserver
```
To view the documentation go to :
```127.0.0.1:5000/```

To run the tests type:
```
pytest tests/
```

### API Endpoints

| Methods | Resource URL | Description | Public Access |
| ---- | ------- | --------------- | ------ |
|POST| `/auth/login` | Logs a user in| TRUE |
|POST| `/auth/register` |  Register a user | TRUE |
|POST| `/bucketlists/` | Create a new bucket list | FALSE |
|GET| `/bucketlists/` | List all the created bucket lists | FALSE |
|GET| `/bucketlists/<bucketlist_id>/` | Get single bucket list | FALSE |
|PUT| `/bucketlists/<bucketlist_id>/` | Update this bucket list | FALSE |
|DELETE| `/bucketlists/<bucketlist_id>/` | Delete this single bucket list | FALSE |
|POST| `/bucketlists/<bucketlist_id>/items/` | Create a new item in bucket list | FALSE |
|PUT|`/bucketlists/<bucketlist_id>/items/<item_id>/` | Update a bucket list item | FALSE |
|DELETE|`/bucketlists/<bucket_id>/items/<item_id>/` | Delete an item in a bucket list | FALSE 





