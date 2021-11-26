
# confg = {"apiKey": "AIzaSyCmyMuOn3YswOTwlRFqDOayFE2FJc4_KX4",
#          "authDomain": "qmserver-5e178.firebaseapp.com",
#          "databaseURL": "https://qmserver-5e178-default-rtdb.firebaseio.com",
#          "projectId": "qmserver-5e178",
#          "storageBucket": "qmserver-5e178.appspot.com",
#          "messagingSenderId": "569413910481",
#          "appId": "1:569413910481:web:4c6935d9f9d6f1c9a6eaf0",
#          "measurementId": "G-MWH9PSCGQH"}

import firebase_admin
from firebase_admin import credentials, db

cred = credentials.Certificate("qmkey.json")
default_app = firebase_admin.initialize_app(cred, {
	'databaseURL':'https://qmserver-5e178-default-rtdb.firebaseio.com/'
	})

ref = db.reference("ip")
print(ref.get())
