import re
import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# fstore
cred = credentials.Certificate('credentials/key.json')
firebase_admin.initialize_app(cred)
db = firestore.client()
# init shit
os.chdir('mjml-snippets')
rootDir = os.getcwd()
subdirectories = os.listdir('.')
###


def getVariableNames(fileString):
    attrs = re.findall(r"\{(.*?)\}", fileString)
    return(attrs)


def getFileContents(filename):
    with open(filename) as f:
        return f.read()


def formatMjmlSnippet(mjmlContents):
    templatedMjml = "`" + mjmlContents + "`"
    return(templatedMjml)


def navFormatUpload(folderName):
    uploads = {}
    os.chdir(folderName)
    mjmlFiles = os.listdir('.')
    for i in mjmlFiles:
        tmp = getFileContents(i)
        attrs = getVariableNames(tmp)
        tmp = formatMjmlSnippet(tmp)
        stripExtension = i[:-5]
        # upload entry to fstore
        doc_ref = db.collection(folderName).document(stripExtension)
        doc_ref.set({
            u'name': stripExtension,
            u'attrs': attrs,
            u'mjml': tmp,
            u'uploadTimestamp': firestore.SERVER_TIMESTAMP
        })
    # get back to the root directory before running again
    os.chdir(rootDir)
    return(uploads)


def uploadToFirestore():
    return(True)


for directory in subdirectories:
    print("Uploading directory: " + directory)
    navFormatUpload(directory)
