import pyrebase

firebaseConfig = {
  'apiKey': "AIzaSyCW8XH0St_2fQkwz2yGpiZ6KhdN-LIhTvg",
  'authDomain': "afterparty-b5649.firebaseapp.com",
  'projectId': "afterparty-b5649",
  'storageBucket': "afterparty-b5649.appspot.com",
  'messagingSenderId': "165896534698",
  'appId': "1:165896534698:web:640fc1d8fcd34685826ed3",
  'measurementId': "G-ZQEFZGXKF0",
  'databaseURL': "https://afterparty-b5649-default-rtdb.firebaseio.com/"
}

firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()

email = 'iuliastefana1705@yahoo.com'
password = '432422'

user = auth.create_user_with_email_and_password(email, password)
print(user)