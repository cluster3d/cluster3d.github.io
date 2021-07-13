var express = require('express');
var router = express.Router();
var auth = require('firebase-admin').auth();
const db = require('firebase-admin').firestore();
const User = require('../models/user');
const Object_db = require('../models/object');
const Annotation = require('../models/annotation');
const checkAuthenticated = require('../middlewares/index').checkAuthenticated;

const yaml = require('js-yaml');
const fs   = require('fs');

var path = require('path');
var abc_obj_path = './public/abc_dataset/chunk_000/obj/'
var abc_feat_path = './public/abc_dataset/chunk_000/feat/'

function load_file(folder) {
  let parsed_feat = '';
  let obj_path = '';
  if (fs.statSync(abc_obj_path+folder).isDirectory()) {
    var items = fs.readdirSync(abc_obj_path+folder)
    if (items[0]) {
      obj_path = '../abc_dataset/chunk_000/obj/'+folder+'/'+items[0]
    }
  }
  if (fs.statSync(abc_feat_path+folder).isDirectory()) {
    var items = fs.readdirSync(abc_feat_path+folder)
    if (items[0]) {
      parsed_feat = yaml.safeLoad(fs.readFileSync(path.join(__dirname, '../public/abc_dataset/chunk_000/feat', folder, items[0]), 'utf8'));
    }
  }
  if (obj_path == '' || parsed_feat == '') {
    return -1
  }
  return {objPath: obj_path, feat: parsed_feat.surfaces}
}

router.get('/filename/:folder', (req, res) => {
  const obj_file = load_file(req.params.folder)
  if (obj_file != -1) {
    res.json(obj_file)
  } else {
    res.status(400).send('failed to read file')
  }
});

router.get('/complete_model/:folder', async (req, res) => {
  const obj = new Object_db();
  try {
    object_list = await obj.get_same_assembly_obj(req.params.folder);
    console.log('COMPLETE:', object_list)
  } catch(e) {
    console.log(e);
  }
  let fileList = []
  object_list.forEach(obj_id => {
    const data = load_file(obj_id)
    if (data != -1) {
      fileList.push({...data, folderNmae: obj_id})
    }
  });
  res.json(fileList)
})

router.post('/assign-user', checkAuthenticated, (req, res) => {
  console.log(req.body)
  const annotation = new Annotation();
  let annotation_data = req.body
  annotation_data['assignedBy'] = req.user.id
  annotation_data['assignTime'] = new Date();
  annotation_data['done'] = false
  annotation.add(annotation_data)
  res.redirect('/assign?file=' + annotation_data.objectId);
});

router.get('/', checkAuthenticated, async (req, res) => {

  const obj = new Object_db(req.user.id);
  const usr = new User(req.user.id)
  let usr_names = await usr.get_all_annotaors_name()
  var object_list = []
  try {
    object_list = await obj.get();
  } catch(e) {
    console.log(e);
  }
  res.render('assign', { title: '3d-annotation', hello: object_list.sort(), usr_names: usr_names.sort(), admin: req.user.role=="admin" });

});

router.post('/annotation', async (req, res) => {
  const uid = req.body.uid;
  const oid = req.body.oid;
  const querySnapshots = await db.collection("annotations").where("annotator", "==", uid).where("objectId", "==", oid).get();
  res.json(querySnapshots.docs.map(doc => doc.data())[0]);
});

router.post('/annotator', async (req, res) => {
  const oid = req.body.oid;
  const querySnapshot = await db.collection("annotations").where("objectId", "==", oid).get();
  const annotations = querySnapshot.docs.map(doc => doc.data());
  const result = await Promise.all(annotations.map(async annotation => {
    const user = await db.collection("user").doc(annotation.annotator).get();
    return Object.assign(annotation, { annotator: Object.assign(user.data(), {id: user.id}) });
  }));
  const userQuerySnapshot = await db.collection("user").where("role", "==", "annotator").get();
  const users = userQuerySnapshot.docs.map(doc => Object.assign(doc.data(), { id: doc.id }));
  const uidInResult = result.map(annotation => annotation.annotator.id);
  const usersNotInResult = users.filter(user => uidInResult.indexOf(user.id) === -1);
  res.json({
    annotators: result,
    dropdownUsers: usersNotInResult
  });
});

module.exports = router;
