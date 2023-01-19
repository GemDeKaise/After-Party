import os
import shutil
from modules.Database import Database
from definition import *

class Gallery:

    def _init_(self):
        pass

    def get_all_gallery(self):
        galleries = [name for name in os.listdir(Gallery_Folder)]
        return galleries

    def add_gallery(self,gallery_name):
        if os.path.isdir(Gallery_Folder+gallery_name) is False:
            if os.mkdir(Gallery_Folder+gallery_name):
                return True
        else:
            return False

    def delete_gallery(self, gallery_name):
        if os.path.isdir(Gallery_Folder+gallery_name) is True:
            try:
                shutil.rmtree(Gallery_Folder+gallery_name)
                return True
            except OSError:
                return False
        else:
            return False


    def edit_gallery_name(self,oldName,newName):
        if os.path.isdir(Gallery_Folder+oldName) is True:
            if os.rename(Gallery_Folder+oldName, Gallery_Folder+newName):
                return True
        else:
            return False
        
    def get_images(self, gallery_name):
        images = [name for name in os.listdir(Gallery_Folder+gallery_name)]
        return images
    
    def get_joined_galleries(self, user_id):
        galleries = [name for name in os.listdir(Gallery_Folder)]
        mygalleries = []
        db = Database()
        for gallery in galleries:
            print(db.is_member(gallery, user_id))
            if db.is_member(gallery, user_id) == True:
                mygalleries = mygalleries + [gallery]
        return mygalleries
    