# cms_project_UpForce:

* Clone the repo using the following command:
  
    `git clone https://github.com/yameen-dasadiya/cms_project_UpForce.git`
* Create a virtual env with the following command:

    `python -m venv UpForce` (you can also use pyenv)
* For dependencies installation:

    `pip install -r requirements.txt`
* For Database migrations:

    `python manage.py makemigrations`
    `python manage.py migrate`
* Create superuser:
  
    `python manage.py createsuperuser`
* To start the server:

    `python manage.py runserver`
