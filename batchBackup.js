const fs = require("fs");
const firestoreService = require("firestore-export-import");
const serviceAccount = require("./credentials/key.json");

// Initiate Firebase App

firestoreService.initializeApp(
  serviceAccount,
  "https://email-maker-192bb.firebaseio.com"
);

// Start exporting your data
firestoreService.backups().then((data) => {
  data = JSON.stringify(data);
  fs.writeFile(
    `./backups/firestore/backup_${+new Date()}.json`,
    data,
    function (err) {
      if (err) return console.log(err);
      console.log("backup written");
    }
  );
});
