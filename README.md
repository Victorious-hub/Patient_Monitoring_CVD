## Setup
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

