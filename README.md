# A Django Social Network

A social network build with Django framework, to learn and understant more some concepts related to web development with a live project.

## online version
Actually offline

## Ssome screenshoot

![Image](https://github.com/pythonbrad/social_network/blob/master/a.png)
![Image](https://github.com/pythonbrad/social_network/blob/master/b.png)
![Image](https://github.com/pythonbrad/social_network/blob/master/c.png)

## How install?

### dependencies
You need to have installed on your computer 

* python3
* virtualenv
* git

### installation process

```bash
cd social_network
virtualenv -p python3 venv
source venv/bin/activate
pip -r install requirements.txt
python manage.py migrate
python manage.py runserver
```

Open your browser at http://localhost:8000
