import os

print('installing virtual environment')
os.system('pip install virtualenv && virtualenv env && env\\bin\\activate.bat && pip install -r requirements.txt')