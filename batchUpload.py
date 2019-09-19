import re
import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from multiprocessing.pool import Pool

# firestore
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
    newlist = []
    for i in attrs:
        if i not in newlist:
            newlist.append(i)
    return(newlist)


def getSnippetName(fileString):
    # Look at the first HTML comment and get the name out of it - this is the title
    snippetName = re.findall(r"<!--([\s\S]+?)-->", fileString)[0].strip()
    return(snippetName)


def getPreviewImage(fileString):
    # Look for a potential 2nd comment - if it's not there, set this to blank
    try:
        previewImage = re.findall(r"<!--([\s\S]+?)-->", fileString)[1].strip()
        return(previewImage)
    else:
        return("")


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
        humanReadable = getSnippetName(tmp)
        previewImage = getPreviewImage(tmp)
        tmp = formatMjmlSnippet(tmp)
        stripExtension = i[:-5]
        # upload entry to fstore
        doc_ref = db.collection(folderName).document(stripExtension)
        doc_ref.set({
            u'name': stripExtension,
            u'attrs': attrs,
            u'mjml': tmp,
            u'humanReadable': humanReadable,
            u'previewImage': previewImage,
            u'uploadTimestamp': firestore.SERVER_TIMESTAMP
        })
    # get back to the root directory before running again
    os.chdir(rootDir)
    return(uploads)


def uploadToFirestore():
    return(True)


def multiLoad(directory):
    print("Uploading directory: " + directory)
    navFormatUpload(directory)
    print("{} directory upload complete.".format(directory))


p = Pool(len(subdirectories))
p.map(multiLoad, subdirectories)
p.close()
p.join()
