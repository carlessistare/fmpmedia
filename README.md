fmpmedia
========

Python framework for storing media files in Google App Engine


1. INTRODUCTION

This document describes the communication protocol of Ad4sMedia Platform for storing and serving all kind of files.
Regarding to its efficiency it could be a good idea to use this service as our own adServing platform.

2. REQUESTS

2.1 Upload File

http://ad4smedia.appspot.com/upload
Type: POST
Fields:
•	name: original name of the file with its extension ( Ex.: cocacola-logo.jpg )
•	mime: MIME TYPE in order to be served properly ( Ex.: image/jpeg , application/zip, application/msword , …  )
•	folder: group notion, which can be used as campaign identifier. Integer
•	folderType: type of the group, which can be used as ‘campaign’ or ‘support’, depending on what the images are related to. We could have the same identifier for both campaign and support, that’s why we need this notion. 
•	file: file type field which contains the archive to post

Returns: Json with the unique identifier for this file.




2.2 Update File

http://ad4smedia.appspot.com/update
Type: POST
Fields:
•	id: identifier of the file
•	name: original name of the file with its extension ( Ex.: cocacola-logo.jpg )
Returns: Json with the unique identifier for this file.



2.3 Show Image

http://ad4smedia.appspot.com/xxx/yyy/zzzzzzzzzzzzz

Type: GET
Fields:
xxx: ‘campaign’ | ‘support’
yyy: campaign or support identifier
zzzzzzzzzzzzz: image identifier

2.4 Download Package

http://ad4smedia.appspot.com/package/xxx/yyy
Type: GET
Fields:
•	xxx: ‘campaign’ | ‘support’
•	yyy: campaign or support identifier
Returns: ZIP package containing all the campaign files


2.5 Delete File

http://ad4smedia.appspot.com/delfile/yyyyyyyyyyyyy 
Type: GET
Fields:
•	yyyyyyyyyyyyy: file identifier


2.6 Delete package

http://ad4smedia.appspot.com/delpackage/xxx/yyy 
Type: GET
Fields:
•	xxx: ‘campaign’ | ‘support’
•	yyy: campaign or support identifier


