from flask import Flask, sessions, request, render_template, redirect, url_for, jsonify
from werkzeug.utils import secure_filename
import json, os, cv2
from modules.Database import Database
from modules.Gallery import Gallery
from modules.Photos import Photos
from definition import *
import pyrebase


app = Flask(__name__)


ALLOWED_EXTENSIONS = set(['jpg', 'jpeg'])
session = {}

firebaseConfig = {
  'apiKey': "AIzaSyCW8XH0St_2fQkwz2yGpiZ6KhdN-LIhTvg",
  'authDomain': "afterparty-b5649.firebaseapp.com",
  'projectId': "afterparty-b5649",
  'storageBucket': "afterparty-b5649.appspot.com",
  'messagingSenderId': "165896534698",
  'appId': "1:165896534698:web:640fc1d8fcd34685826ed3",
  'measurementId': "G-ZQEFZGXKF0",
  'databaseURL': "https://afterparty-b5649-default-rtdb.europe-west1.firebasedatabase.app/"
}

auth = pyrebase.initialize_app(firebaseConfig).auth()
db = Database()
database = db.get_database()

photos_obj = Photos()


@app.route('/')
@app.route('/index')
def index():
    if 'type' in session:
        return redirect(url_for('galleries'))

    return render_template("index.html")


@app.route('/login', methods=['POST'])
def do_login():
    if request.method == "POST":
        user_name = request.form['username']
        password = request.form['password']
        try:
            user = auth.sign_in_with_email_and_password(user_name, password)
            session['uid'] = user['localId']
            session['type'] = "admin"
            
            response = {'success': True}
            return json.dumps(response)
        except:
            response = {'success': False, 'error': 'Invalid email or password'}
            return json.dumps(response)

@app.route('/signup', methods=['POST'])
def do_signup():
    if request.method == "POST":
        email = request.form['username']
        password = request.form['password']
        try:
            user = auth.create_user_with_email_and_password(email, password)
            session['uid'] = user['localId']
            session['type'] = "admin"
            
            database.child("users").child(session['uid']).set({'email': email, 'role': 'admin'})
            
            response = {'success': True}
            return json.dumps(response)
        except:
            response = {'success': False, 'error': 'Invalid email or password'}
            return json.dumps(response)

@app.route('/logout')
def do_logout():
    session.pop('type', None)
    return redirect(url_for('index'))

@app.route('/galleries')
def galleries():
    if 'type' in session:
        gallery_obj = Gallery()
        galleries = gallery_obj.get_all_gallery()
        
        print(db.get_galleries().get().val())
        return render_template("gallery.html", galleries=galleries, session=session)
    else:
        return redirect(url_for("index"))
    
@app.route('/galleries/mygalleries')
def mygalleries():
    if 'type' in session:
        gallery_obj = Gallery()
        galleries = gallery_obj.get_joined_galleries(session.get('uid'))
        return render_template("mygallery.html", galleries=galleries, session=session)
    else:
        return redirect(url_for("index"))


@app.route('/galleries/add', methods=['POST'])
def add_galleries():
    if 'type' in session:
        if request.method == "POST":
            gallery_name = request.form['galleryName']
            password = request.form['password']

            gallery_obj = Gallery()
            result = gallery_obj.add_gallery(gallery_name)
            user_id = session.get('uid')
            
            
            db.set_password(gallery_name, password)
            db.add_memeber(gallery_name, user_id)
            
            response = {'success':result}
            return json.dumps(response)
    else:
        response = {'success': False}
        return json.dumps(response)


@app.route('/galleries/edit', methods=['POST'])
def edit_galleries():
    if request.method == "POST":
        new_name = request.form['newName']
        gallery_name = request.form['galleryName']

        gallery_obj = Gallery()
        result = gallery_obj.edit_gallery_name(gallery_name, new_name)

        response = {'success': result}
        return json.dumps(response)


@app.route('/galleries/delete', methods=['POST'])
def delete_galleries():
    if request.method == "POST":
        gallery_name = request.form['galleryName']

        gallery_obj = Gallery()
        result = gallery_obj.delete_gallery(gallery_name)
        db.delete_gallery(gallery_name)

        response = {'success': result}
        return json.dumps(response)

@app.route('/galleries/album/<gallery_name>', methods=['GET'])
def gallery(gallery_name):
    if 'type' in session:
        photos_obj = Photos()
        photos = photos_obj.get_all_gallery_photos(gallery_name)
        return render_template("photos.html", photos=photos, gallery_folder=Gallery_Folder,gallery_name=gallery_name, session=session)
    else:
        return redirect(url_for("index"))


@app.route('/galleries/album/photos/delete', methods=['POST'])
def delete_gallery_photo():
    if request.method == "POST":
        gallery_name = request.form['galleryName']
        photo_name = request.form['photoName']

        result = photos_obj.delete_gallery_photos(gallery_name, photo_name)

        response = {'success': result}
        return json.dumps(response)
    
@app.route('/view_gallery/<string:name>', methods=['GET','POST'])
def view_gallery(name):
    user_id = session.get('uid')
    if user_id:
        members = database.child("galleries").child(name).child("members").get().val()
        if members and user_id in members:
            return render_template('gallery.html', gallery_name=name, is_member=True)
        else:
            if request.method == 'POST':
                code = request.form['code']
                if code == name:
                    database.child("galleries").child(name).child("members").child(user_id).set(True)
                    return render_template('gallery.html', gallery_name=name, is_member=True)
                else:
                    return render_template('gallery.html', gallery_name=name, is_member=False, error='Invalid code')
            else:
                return render_template('gallery.html', gallery_name=name, is_member=False)
    else:
        return "You need to login to access this gallery."


@app.route('/galleries/album/<gallery_name>/upload', methods=['GET','POST'])
def upload_gallery_photo(gallery_name):
    app.config['UPLOAD_FOLDER'] = Gallery_Folder+gallery_name

    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(url_for('gallery', gallery_name=gallery_name))
        file = request.files['file']
        if file.filename == '':
            msg = 'No selected file'
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('gallery', gallery_name=gallery_name))
    
    return redirect(request.url)

@app.route('/get_code/<string:gallery_name>', methods=['GET'])
def get_code(gallery_name):
    db = Database()
    database = db.get_database()
    
    code = db.get_password(gallery_name)
    return jsonify({"code": str(code)})


@app.route('/check_membership/<string:name>')
def check_membership(name):
    user_id = session.get('uid')
    if user_id:
        members = database.child("galleries").child(name).child("members").get().val()
        if members and user_id in members:
            return jsonify(is_member=True)
        else:
            return jsonify(is_member=False)
    else:
        return jsonify(is_member=False)

@app.route('/add_member/<string:name>/<string:user_id>', methods=['POST'])
def add_member(name, user_id):
    if request.method == 'POST':
        res = db.add_memeber(name, user_id)
        
        if res:
            return jsonify(success=True)
        else:
            return jsonify(success=False)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


if __name__  == "__main__":
    app.run(debug=True)
