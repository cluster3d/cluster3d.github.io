const db = require('firebase-admin').firestore();

function pad(num, size) {
    var s = String(num)+"";
    while (s.length < size) s = "0" + s;
    return s;
}

class Object {
    constructor() {
    }


    async get() {
        const docSnapshot = await db.collection("objects").get();
        return docSnapshot.docs.map(doc => doc.id);
    }

    async get_on_shape_id(oid) {
        const docSnapshot = await db.collection("objects").doc(oid).get()
        return docSnapshot.data()['id']
    }

    async get_on_shape_url(oid) {
        const docSnapshot = await db.collection("objects").doc(oid).get()
        return docSnapshot.data()['href']
    }

    async get_on_shape_url_part(oid) {
        const docSnapshot = await db.collection("objects").doc(oid).get()
        return docSnapshot.data()['hrefPart']
    }

    async get_not_done(uid) {
        var return_list = []
        let querySnapshot;
        try {
            querySnapshot = await db.collection("annotations").where("annotator", "==" , uid).where('done', '==', false).get();
        } catch(e) {
            console.log(e)
        }
        querySnapshot.forEach(function(docSnapshot) {
            return_list.push(docSnapshot.data()['objectId']);
        });
        return return_list;
    }

    async add(datas) {
        for (const data of datas) {
            db.collection("objects").doc(data.seq).set({
                id: data.id,
                href: data.href,
                hrefPart: data.hrefPart
            })
        }
    }

    async get_same_assembly_obj(part_id) {
        var return_list = []
        const docSnapshot = await db.collection("objects").doc(part_id).get()
        const onshape_id = docSnapshot.data()['id']
        const querySnapshot = await db.collection("objects").where('id', '==', onshape_id).get();
        querySnapshot.forEach(function(docSnapshot) {
            return_list.push(docSnapshot.id);
        });
        return return_list;
    }

}

module.exports = Object;