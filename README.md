# Online Ticket App

A one-stop website that gathers all of Singapore's attractions and movie tickets for easy purchase.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Folders and Main

app.py is the main driver of the app

/api contains all the backend files (classes) 
/Scraping contains website scraping for tickets information
/templates contains all the html file
/static contains css

### Prerequisites and Installation of pip modules

All dependancies are in the requirements.txt file. Make sure to pip install all required modules before running the application.

Example:
```
pip install flask flask_sqlalchemy flask_mail flask_cors sqlalchemy autocorrect
```

## Instructions 

### For Deployment

Our current application is placed in the "OnlineTicketApp" folder. To run the application (using commandprompt):
1) Ensure that all dependencies are installed.
2) In commandprompt, change the working directory to where app.py is located. The working directory can be found by app.py -> Properties -> Location
3) Run application by typing this into the command prompt line: 
```
python app.py
```
4) If successfully launched, cmd should display something like this: 
```
Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```
5) Copy the link into a web browser and the webpage will be displayed.

### For Testing

After deploying the application, unit testing can be done.
1) Run application
2) Run test by typing this into the commandprompt line:
```
python app_test.py
```