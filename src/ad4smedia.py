
__author__ = 'Carles Sistare'

import cgi
import StringIO

import webapp2
#from google.appengine.ext import webapp
from google.appengine.ext import db

import zipfile

import wsgiref.handlers


########################
# MediaFile Model
########################
class MediaFile(db.Model):
    name = db.StringProperty(required=True)
    folder = db.StringProperty(required=True)
    folderType = db.StringProperty(required=True)
    mime = db.StringProperty(required=True)
    data = db.BlobProperty(required=True)

########################
# MediaFile's Managing
########################
class Ad4sMediaUploadFile(webapp2.RequestHandler):
    def post(self):
        
        self.response.headers['Content-Type'] = 'application/json'
        
        img_data = self.request.get('file')
        name = cgi.escape(self.request.get('name'))
        folderType = cgi.escape(self.request.get('folderType'))
        mime = cgi.escape(self.request.get('mime'))
        folder = cgi.escape(self.request.get('folder'))

        try:
            mediaFile = MediaFile(name = name,
                    mime = mime,
                    folderType = folderType,
                    data = img_data,
                    folder = folder)
            mediaFile.put()
                    
            self.response.out.write('{"id":"' + str(mediaFile.key()) + '"}')
            
        except:
            self.error(400)
            self.response.out.write('{"error":"Sorry, we had a problem processing the file provided."}')

class Ad4sMediaUpdateFile(webapp2.RequestHandler):
    def post(self):
        
        self.response.headers['Content-Type'] = 'application/json'
        
        idMediaFile = cgi.escape(self.request.get('id'))
        name = cgi.escape(self.request.get('name'))

        try:
            mediaFile = MediaFile.get(idMediaFile)
            mediaFile.name = name
            mediaFile.put()
                    
            self.response.out.write('{"id":"' + idMediaFile + '"}')
            
        except:
            self.error(400)
            self.response.out.write('{"error":"Sorry, we had a problem processing id provided."}')


class Ad4sMediaShowFile(webapp2.RequestHandler):
    
    def get(self, type_folder, id_folder, id_media_file, file_extention):
        try:
            mediaFile = db.get(id_media_file)
            self.response.headers['Content-Type'] = str(mediaFile.mime)
            self.response.out.write(str(mediaFile.data))
        except :
            self.response.headers['Content-Type'] = 'text/plain'
            self.response.out.write('No File Found. Key: ' + id_media_file + ' ' + id_folder)

class Ad4sMediaDelFile(webapp2.RequestHandler):
    
    def get(self, id_media_file):
        self.response.headers['Content-Type'] = 'application/json'
        try:
            db.delete(id_media_file)
            self.response.out.write('{"id":"' + id_media_file + '"}')
        except :
            self.response.out.write('{"error":"No File Found. Key: ' + id_media_file + '"}')
        
########################
# Folder Managing
########################
class Ad4sMediaDelPackage(webapp2.RequestHandler):
    
    def get(self, type_folder, id_folder):
        self.response.headers['Content-Type'] = 'application/json'
        try:
            mediaFiles = db.GqlQuery("SELECT * FROM MediaFile WHERE folderType = :1 AND folder = :2", type_folder, id_folder)
            db.delete(mediaFiles)
            self.response.out.write('{"idPackage":"' + id_folder + '"}')
        except :
            self.response.out.write('{"error":"No Package Found. Key: ' + id_folder + '"}')
            

class Ad4sMediaGetPackage(webapp2.RequestHandler):
    
    def get(self, type_folder, id_folder):
        try:
            # create the zip stream
            zipstream=StringIO.StringIO()
            zipFile = zipfile.ZipFile(zipstream,'w')
        
            # Write media file into zip file
            mediaFiles = db.GqlQuery("SELECT * FROM MediaFile WHERE folderType = :1 AND folder = :2", type_folder, id_folder)

            if mediaFiles.count() == 0 :
                self.response.headers['Content-Type'] = 'text/plain'
                self.response.out.write('Package not Found. Key: ' + id_folder)
                return
            for mediaFile in mediaFiles:
                # store the contents in a stream
                f=StringIO.StringIO(mediaFile.data)
                length = len(mediaFile.data)
                f.seek(0)
                
                # write the contents to the zip file
                while True:
                    buff = f.read(int(length))
                    if buff=="":break
                    zipFile.writestr(mediaFile.name, buff)
                
            # we have finished with the zip so package it up and write the directory
            zipFile.close()
            zipstream.seek(0)

            # create and return the output stream
            self.response.headers['Content-Type'] ='application/zip'
            self.response.headers['Content-Disposition'] = 'attachment; filename="package.zip"'    
            while True:
                buf=zipstream.read(2048)
                if buf=="": break
                self.response.out.write(buf)
                
        except db.BadKeyError:
            self.response.headers['Content-Type'] = 'text/plain'
            self.response.out.write('Error Zipping File')


def main():
    url_map = [('/package/([-\w]+)/([-\w]+)', Ad4sMediaGetPackage),
               ('/upload', Ad4sMediaUploadFile),
               ('/update', Ad4sMediaUpdateFile),
               ('/delfile/([-\w]+)', Ad4sMediaDelFile),
               ('/delpackage/([-\w]+)/([-\w]+)', Ad4sMediaDelPackage),
               ('/([-\w]+)/([-\w]+)/([-\w]+)(\.\w*)?', Ad4sMediaShowFile)]
    application = webapp2.WSGIApplication(url_map, debug=True)
    wsgiref.handlers.CGIHandler().run(application)



if __name__ == "__main__":
    main()
