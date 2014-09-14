#FlaskGenerator

###What?
FlaskGenerator is very simple Python script which will bootstrap your Flask project files in seconds. It will create virtualenv for you, install Flask, extensions and other dependencies. During execution, it will ask you several y/n questions to perform specific actions based on your decision.

###How?
Required: **Python2.7, pip, virtualenv**

Simply call `python flask-generator.py` in your project folder (you must have flask-generator.py in that folder) or pass a path to project folder as first command-line argument.

Script will obtain all decorated actions and call them in random order. Function decorated with **@action** will be executed before functions with **@prompt_action** decorator.

###Contribution
You can add your own actions very easily. Create function with your tasks and decorate it with either @action or @prompt_action. Functions with *@action* decorator will just execute and their docstring will be printed. Functions with *@prompt_action* will execute with question saved in their docstring. If **y** answer is provided, function body will execute. If not, script will skip this function. Please note that default answer is **N**.

###TODO

 - setup.py
 - termcolor
