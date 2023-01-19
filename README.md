# AfterParty Gallery #
## Anghelescu Andrei, Chesches Iulia, Gheorghiu Vlad, Spinochi Andreea ##

### Brief description ###
Afterparty Gallery is a web-based application that provides a simple and user-friendly interface
and is meant to make it easy for friends to share photos and memories of their group activities.
Some of the features include user registration and login, creating galleries, uploading or deleting photos,
everything done in a secure way by using code verification.

### Used technologies ###
The application uses the Flask library to handle routing and rendering templates, as well as the Pyrebase 
library to interact with the Firebase API, which is responsible for user authentication and database
storage.
It allows users to upload photos to a gallery and manages the uploaded files using the os library.
The session object is used for checking the user's login status before allowing certain routes
to be accessed and redirects the user to the login page if they are not logged in. This way, only 
logged-in users can access certain pages of the application.
The HTML template uses Bootstrap for styling and layout, including a JavaScript file (that adds 
functionality to the buttons) and multiple CSS files (that make the website visually appealing).

### Run instructions ###
We added a Makefile that makes the project easy to run: it creates a virtual environment and installs
all the necessary dependencies. <br>
Commands: <br>
make -> install required packages <br>
make run -> launch app

### Site <3 ###
http://gemdekaise.pythonanywhere.com/index

### Contributors ###

Members | Andrei Anghelescu | Iulia Chesches | Vlad Gheorghiu | Andreea Spinochi
--- | --- | --- | --- |--- 
Idea and Planning | x | x | x | x | 
App Sketch | x | x | x | x |
Workflow | x | x | x | x | 
Design |  |  |  | x | 
Photo Editing |  |  |  | x | 
HTML Template |  |  | x |  | 
Server Pages |  |  | x |  | 
CSS |  |  |  | x | 
JavaScript |  |  |  | x | 
Bootstrap |  |  | x | x | 
Sign in/Sign up/Logout |  | x | x |  | 
Gallery Upload/Delete |  | x |  |  | 
Gallery Security with Password |  | x |  |  | 
Memberships | x |  |  |  | 
Photo Upload/Delete |  |  | x |  | 
Firebase Setup | x | x |  |  |
Firebase Users | x |  |  |  |
Firebase Galleries and Photos | x |  |  |  |
Error Pop-ups |  |  |  | x |
Code Refactoring |  |  | x |  | 
Makefile and Environment |  | x |  |  | 
Galleries for Demo | x |  |  |  |
Site Deployment | x |  |  |  | 
README |  | x |  |  | 

LsacParty - lasc
UrbanParty - urbanistic
NeverseGascaVesela - neversea
Partyyyyyyy- 123456

### Difficulties ###
Some of our difficulties: <br>
* Firebase: It took a long time for us to understand how it works. We had to follow multiple tutorials but in the 
end we figured out how to store both users and their accessible galleries. <br>
* Debugging: Flask's built-in development server does not provide any debugging features, so we had to use pdb to fix
any mistakes.<br>
* Integration: We found different resources online (for python, html, javascript), but it was challenging to make
them work together.<br>
