# Jarvis

### Set up virutal environment: (install requirements)
- Activate Virtual environment and run:
    `pip install -r requirements.txt`

### For poetry
`poetry install --with dev`

### Set up Google Calendar API:
- Follow steps here:
    https://developers.google.com/calendar/api/quickstart/python
- Make sure to add your email as a test user for your project
- Once you make your OAuth 2.0 Client ID, download the json file and rename it `credentials.json` and add to: `reminders` folder
- create `config.ini` file and add email following `config_example.ini`