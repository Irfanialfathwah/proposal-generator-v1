# Proposal Generator

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.
Every template in the program is based on the design file `proposal-generator.drawio`

### Step to run the program

A step by step series of examples that tell you how to get a development env running

1. Install virtual environment

```
pip install virtualenv
```
2. Create virtual environment and activate inside proposal-generator directory according the structure below
```
virtualenv venv
> On windows -> venv\Scripts\activate
> On linux -> . env/bin/activate
```
3. Install flask library on your virtual environment with pip
```
pip install flask
```
4. Run this project with terminal or command promt on your virtual environment
```
python run.py
```
9. Access `localhost:5000` according port that created in `run.py`
    Sign In with email "admin@admin.com" and password "admin" without ""

![Sample](https://github.com/Irfanialfathwah/proposal-generator/blob/master/Sample-run.png)

10. To stop the service of flask project (__CTRL + C__)

### Prerequisites

Make sure you have installed Python 3 on your device

### Project structure
```
* proposal-generator/
  |--- app/
  |    |--- static/ (Template [AdminLTE](https://github.com/ColorlibHQ/AdminLTE.git))
  |    |--- templates/
  |    |    |--- add-proposal.html
  |    |    |--- base.html
  |    |    |--- customers.html
  |    |    |--- footer.html
  |    |    |--- head.html
  |    |    |--- index.html
  |    |    |--- login.html
  |    |    |--- main-sidebar.html
  |    |    |--- navbar.html
  |    |    |--- proposals.html
  |    |    |--- scripts.html
  |    |--- __init__.py
  |    |--- views.py
  |--- venv/ (install virtualenv first)
  |--- config.py
  |--- proposal-generator.drawio
  |--- requirements.txt
  |--- run.py
```

## Built With

* [Python 3](https://www.python.org/download/releases/3.0/) - The language programming used
* [Flask](http://flask.pocoo.org/) - The web framework used
* [Virtualenv](https://virtualenv.pypa.io/en/latest/) - The virtual environment used

## Clone or Download

You can clone or download this project
```
> Clone : git clone https://github.com/irfanialfathwah/proposal-generator.git
```



* **Irfanialfathwah**

