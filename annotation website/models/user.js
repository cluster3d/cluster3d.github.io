const db = require('firebase-admin').firestore();

class User {
  constructor(uid) {
    this.uid = uid;
  }

  async get() {
    const docSnapshot = await db.collection('user').doc(this.uid).get();
    return Object.assign(docSnapshot.data(), { id: docSnapshot.id });
  }

  async get_all_annotaors_name() {
    let return_list = []
    const querySnapshot = await db.collection("user").get();
    querySnapshot.forEach(function(docSnapshot) {
      if (docSnapshot.data()['role'] == 'annotator') {
        return_list.push({name: docSnapshot.data()['first-name'], id: docSnapshot.id});
      }
    });
    return return_list;
  }
}

module.exports = User;