const db = require('firebase-admin').firestore();

class Annotation {
    constructor(uid) {
        this.uid = uid;
    }
    async add(data) {
      db.collection("annotations").doc(data.annotator+'*'+data.objectId).set(data)
    }

    async update(uid, oid, data) {
      let querySnapshot;
      try {
        querySnapshot = await db.collection("annotations").where("annotator", "==", uid).where('objectId', '==', oid).get();
      } catch(e) {
        console.log(e)
      }
      querySnapshot.forEach(function(docSnapshot) {
        db.collection("annotations").doc(docSnapshot.id).update(data)
      });
    }

    async delete(uid, oid) {
      db.collection("annotations").doc(uid+'*'+oid).delete()
    }
    
}

module.exports = Annotation;