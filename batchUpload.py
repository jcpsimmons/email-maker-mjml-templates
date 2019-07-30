import os

os.chdir('mjml-snippets')
rootDir = os.getcwd()
subdirectories = os.listdir('.')


def getFileContents(filename):
    with open(filename) as f:
        return f.read()


def formatMjmlSnippet(mjmlContents):
    templatedMjml = "`" + mjmlContents + "`"
    return(templatedMjml)


def navAndFormat(folderName):
    uploads = {}
    os.chdir(folderName)
    mjmlFiles = os.listdir('.')
    for i in mjmlFiles:
        tmp = getFileContents(i)
        tmp = formatMjmlSnippet(tmp)
        stripExtension = i[:-5]
        uploads[stripExtension] = tmp
    # get back to the root directory before running again
    os.chdir(rootDir)
    return(uploads)


def uploadToFirestore():
    return(True)


for directory in subdirectories:
    uploadObject = navAndFormat(directory)
    # upload logic - below here is pseudocode
    for thing in uploadObject:
        uploadToFirestore(thing)
