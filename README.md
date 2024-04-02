# Software Design Project
A fuel quote app for COSC 4353 Software Design written using Flask

# Steps to run the project
Create a new directory.
```
mkdir fuel-app
cd fuel-app
```

Clone the app.
```
git remote add origin https://github.com/spartan24032/Software-Design-Project.git
git pull origin main
```
Create a python virtual environment.
```
python -m venv venv
```
Activate it (Windows).
```
source venv/Sripts/activate 
```
Install requirements.
```
pip install -r requirements.txt
```
Create an .env file.
```
touch .env
```
Within the .env file set the SECRET_KEY and CONFIG_TYPE.
```
SECRET_KEY = "BAD_SECRET_KEY"
CONFIG_TYPE = "config.DevelopmentConfig"
```

CONFIG_TYPE can be "config.DevelopmentConfig", "config.TestingConfig", or "config.ProductionConfig". See config.py for details.

Finally, to run the app:
```
flask --app app run
```

Visit http://127.0.0.1:5000 to see the website.

