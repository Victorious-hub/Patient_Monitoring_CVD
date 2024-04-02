# Setup
First, clone the repository:

```sh
$ git clone https://github.com/Victorious-hub/Patient_Monitoring_App.git
$ cd medtech
```

Create virtual environment and activate:

- Install virtualenv using pip:
```sh
$ pip install virtualenv
```
- For Linux and macOS:

```sh
$ python3 venv -m <name_of_your_venv>
$ source venv/bin/activate
```

- For Windows:
```sh
$ python venv -m <name_of_your_venv> 
$ .\venv\Scripts\activate
```
! For deactivating virtualenv, just write:
```sh
$ deactivate
```

Note: if you haven't installed docker on your machine, follow the links:
- Linux: https://docs.docker.com/engine/install/ubuntu/
- Windows https://docs.docker.com/desktop/install/windows-install/ and setup WSL https://learn.microsoft.com/en-us/windows/wsl/install
- macOS https://docs.docker.com/desktop/install/mac-install/

Install all requirements from requirements.txt file:
```sh
$ pip freeze > requirements.txt
$ pip install -r requirements.txt
```

In -medtech- current directory, build and run you docker-compose images:
```sh
$ docker-compose up --build 
```

# Project overview

Patient Cardio Vascular Disease monitoring is just a simple application, that main goal is an easy track doctor patients with their potential cvd problems or anomalies, provide some treatment, make their life better and just to be on air). For searching cdv anomalues, this app includes some machine learning models, that were trained on CVD dataset
- Cardiovascular Disease dataset https://www.kaggle.com/datasets/sulianovacardiovascular-disease-dataset

It's also a good choice for patient to track it's analyses, doctor info, notification, condition and treat proccess

## Project stack
It's a backend part of my application. It includes:
- Python
- Jupyter notebook analysis
- REST architecture
- Django Rest Framework
- Docker/docker-compose
- PostgreSQL
- Celery/Celery-Flow
- Redis


