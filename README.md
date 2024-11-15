# AI Skin Cancer Detector

Welcome to my first-ever Flask project! :)

## What is it about?
It's a tool that allows people to check what the chances are for their skin formations being cancerogenic. Simply upload a photo showing a close-up of the skin thingy that bothers you, wait a few seconds, and you will get a fairly reasonable prediction. If chances turn out to be quite high, it is recommended to go to the doctor. 

## Tech
Apart from the model itself, which I trained using Tensorflow, Keras and Numpy (among others), all code is written in Flask and PostgreSQL which communicate via SQLALchemy. 

## MVC pattern
The project follows the Model View Controller pattern as closely as possible. 

## Folder Content:

#### 1. Models
Here you can find the models which define the format in which the tool communicates with the database. Here you can find logic about what types of tables you have and what kind of info they contain. Not to be confused with the Deep Learning model.
#### 2. CNN Model
This folder contains the Convolutional Neural Network (the file ending with ".keras"), while the file "model_run" defines how it should be used.
#### 3. Managers
This is where the main logic is written. Its files contain classes that enrich other classes and objects such as coming from **Models**, **CNN Model** and **Services** with functionality. This is also where the regulations regarding authentication and authorisation ("auth.py").
#### 4. Migrations
This folder contains all migrations of the different stages of the development of the database.
#### 5. Resources
Here is the place where additional manipulations are made before the code's functionality being distributed to the endpoints allowing for the tool can interact with the outside world. 
#### 6. Schemas
Schemas regulate the format of the API's inputs and outputs. They are being used by the objects in the **Resources**.
#### 7. Services
This is the folder usually dedicated for third-party APIs and solutions. I'm using AWS S3 for storing the photos outside of the **Temp Files**
#### 8. Temp Files
The project needs this folder as a temporary place of storage for users' skin photos.
#### 9. Utils
This is the place for additional useful stuff such as custom decorators and helpers.
#### 10. Tests
This is where unit and integration tests were performed using PyTest.

## Separate Files:

#### app.py
This is the tool's main governing body. It's where we run the app
#### config.py
This is where the different environments are defined and configured.
#### db.py
This is where SQLAlchemy is being called.
#### constants.py
This is where a few constant variables are being stored.


## Installation

First, clone this repository:

<!-- start:code block -->
# Clone this repository
git clone https://github.com/human1abs/flaskProjectCNN/.git

# Install dependencies
Be sure to install all the dependencies from the **requirements/txt** file. Enjoy!




