const functions = require('firebase-functions');
const admin = require('firebase-admin');
admin.initializeApp();
const db = admin.firestore();

exports.sendWelcomeEmail = functions.auth.user().onCreate((user) => {
  return db.collection('user').doc(user.uid).set({ role: "annotator" });
});