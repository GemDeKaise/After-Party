import pyrebase

class Database:
    def __init__(self):
        self.config = {
          'apiKey': "AIzaSyCW8XH0St_2fQkwz2yGpiZ6KhdN-LIhTvg",
          'authDomain': "afterparty-b5649.firebaseapp.com",
          'projectId': "afterparty-b5649",
          'storageBucket': "afterparty-b5649.appspot.com",
          'messagingSenderId': "165896534698",
          'appId': "1:165896534698:web:640fc1d8fcd34685826ed3",
          'measurementId': "G-ZQEFZGXKF0",
          'databaseURL': "https://afterparty-b5649-default-rtdb.europe-west1.firebasedatabase.app/"
        }
        self.firebase = pyrebase.initialize_app(self.config)
        self.database = self.firebase.database()
    def get_database(self):
        return self.database
      
    def get_users(self):
        return self.database.child("users")
      
    def add_memeber(self, gallery_name,  user_id):
        return self.database.child("galleries").child(gallery_name).child("members").update({user_id: True})
    
    def is_member(self, gallery_name, user_id):
        return self.get_galleries().child(gallery_name).child("members").child(user_id).get().val()
      
    def get_galleries(self):
        return self.database.child("galleries")

    def set_password(self, gallery_name, password):
        return self.database.child("galleries").child(gallery_name).set({'code': password})
    
    def get_password(self, gallery_name):
        return self.database.child("galleries").child(gallery_name).get().val()['code']
      
    def add_gallery(self, gallery_name, user_id):
        return self.database.child("galleries").child(gallery_name).set("members", user_id)
      
    def delete_gallery(self, gallery_name):
        return self.database.child("galleries").child(gallery_name).remove()
      
    def add_user_to_gallery(self, gallery_name, user_id):
        return self.database.child("galleries").child(gallery_name).child("members").push(user_id)
