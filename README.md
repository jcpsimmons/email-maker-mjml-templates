# email-maker-mjml-templates

Repository of MJML email templates for Email Maker application. MJML components are contained in the ```mjml-snippets``` folder.

---

## Automation Details

```batchUpload.py``` is a Python script that automatically crawls all subfolders in the mjml-snippets directory, and uploads them to the Firestore DB on Firebase hosting. While doing this the script automatically extracts names of each of the components, and provides the front end with an easy way of replacing variables (ES6 template literals). **This Python script runs whenever a git commit is made using the 'post-commit' hook.**

The batchUpload.py script will not run without credentials which I've excluded from this repo in the .gitignore. 
