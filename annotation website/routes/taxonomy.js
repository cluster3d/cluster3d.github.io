var express = require('express');
var router = express.Router();
var auth = require('firebase-admin').auth();
const fs   = require('fs');
const checkAuthenticated = require('../middlewares/index').checkAuthenticated;
const db = require('firebase-admin').firestore();

router.post('/submit', checkAuthenticated, async (req, res) => {
  var my_data = req.body
  // var annotation_data = {}

  const cluster_ID = parseInt(my_data.cluster_id)
  const user_sanpshot = await db.collection('user').doc(req.user.id).get();

  console.log(my_data.oid)
  if (cluster_ID == user_sanpshot.data()['cluster-mission']) {
    const cid = req.user.id + "*" + cluster_ID;
    const clusterDocSnapshot = await db.collection("cluster-similarities").doc(cid).get();
    
    // annotation_data['objects'] = my_data.oid
    
    if (clusterDocSnapshot.exists) {
      const original_data = clusterDocSnapshot.data().similarities;
      await db.collection("cluster-similarities").doc(cid).update({similarities: original_data.concat({"objectID": my_data.oid})})
    } else {
      await db.collection("cluster-similarities").doc(cid).set({"similarities": [{"objectID": my_data.oid}]});
    }
    const newClusterDocSnapshot = await db.collection("cluster-similarities").doc(cid).get();
    const new_names = newClusterDocSnapshot.data().similarities;
    let object_cnt = 0
    for (x in new_names) {
      object_cnt += new_names[x].objectID.length;
    }

    const clusterObjectSnapshot = await db.collection("clusters").doc(cluster_ID.toString()).get();
    cluster_obj_length = clusterObjectSnapshot.data().objectID.length;
    if (object_cnt >= cluster_obj_length){
      var userRef = db.collection('user').doc(req.user.id);
      await userRef.update({ 'cluster-mission': cluster_ID+1 });
    }
    res.send({"status": "Success."});
  } else {
    res.send({"status": "Error"});
  }


  // var annotation_data = {}
  // var partial = {}
  // const cluster_ID = parseInt(my_data.cluster_id)
  // const user_sanpshot = await db.collection('user').doc(req.user.id).get();

  // if (cluster_ID < user_sanpshot.data()['cluster-mission']) {
  //   res.send({"status": "Error"});
  // } else {
  //   const cid = req.user.id + "*" + cluster_ID;
  //   const clusterDocSnapshot = await db.collection("cluster-names").doc(cid).get();
    
  //   partial['productClassification'] = my_data.cluster
  //   partial['objects'] = my_data.oid
    
  //   if (!clusterDocSnapshot.exists) {
  //     annotation_data['names'] = [partial]
  //     await db.collection("cluster-names").doc(cid).set(annotation_data);
  //   } else {
  //     const original_data = clusterDocSnapshot.data().names;
  //     await db.collection("cluster-names").doc(cid).update({names: original_data.concat(partial)})
  //   }
  //   const newClusterDocSnapshot = await db.collection("cluster-names").doc(cid).get();
  //   const new_names = newClusterDocSnapshot.data().names;
  //   let object_cnt = 0
  //   for (x in new_names) {
  //     object_cnt += new_names[x].objects.length;
  //   }

  //   const clusterObjectSnapshot = await db.collection("cluster").doc(cluster_ID.toString()).get();
  //   cluster_obj_length = clusterObjectSnapshot.data().objectID.length;
  //   if (object_cnt >= cluster_obj_length){
  //     var userRef = db.collection('user').doc(req.user.id);
  //     await userRef.update({ 'cluster-mission': cluster_ID+1 });
  //   }

  //   res.send({"status": "Success."});
  // }
})

router.post('/skip', checkAuthenticated, async (req, res) => {
  const my_data = req.body;
  const cluster_ID = parseInt(my_data.cluster_id)
  var userRef = db.collection('user').doc(req.user.id);
  await userRef.update({ 'cluster-mission': cluster_ID+1 });

  res.send("Success.");
})

router.get('/', checkAuthenticated, async (req, res) => {
  const doc = await db.collection('user').doc(req.user.id).get();
  var data = doc.data()
  var cluster_ID;
  if (('cluster-mission' in data) && data['cluster-mission'] < 1914) {
    cluster_ID = data['cluster-mission'];
  } else {
    console.log('No cluster need to be annotated');
    res.redirect('/');
  }

  const clusterObjectSnapshot = await db.collection("clusters").doc(cluster_ID.toString()).get();

  var render_obj_array = clusterObjectSnapshot.data().objectID;
  const cid = req.user.id + "*" + cluster_ID;
  const clusterDocSnapshot = await db.collection("cluster-similarities").doc(cid).get();
  if (clusterDocSnapshot.exists) {
    const new_names = clusterDocSnapshot.data().similarities;
    var annotated_obj = []
    for (x in new_names) {
      annotated_obj = annotated_obj.concat(new_names[x].objectID);
    }

    for (x in annotated_obj) {
      var index = render_obj_array.indexOf(annotated_obj[x]);
      if (index !== -1) {
        render_obj_array.splice(index, 1);
      }
    }
    
  } 

  res.render('taxonomy', { title: '3d-annotation', admin: req.user.role=="admin", cluster_ID: cluster_ID, cluster: render_obj_array });
});



module.exports = router;