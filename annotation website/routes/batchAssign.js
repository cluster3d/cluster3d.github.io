var express = require('express');
var router = express.Router();
const checkAuthenticated = require('../middlewares/index').checkAuthenticated;
const User = require('../models/user');
const db = require('firebase-admin').firestore();

router.get('/', checkAuthenticated, async (req, res) => {
  const usr = new User(req.user.id)
  let usr_names = await usr.get_all_annotaors_name()
  res.render('batchAssign', {admin: req.user.role=="admin", usr_names: usr_names.sort()});
});

function pad(num, size) {
  var s = String(num)+"";
  while (s.length < size) s = "0" + s;
  return s;
}
router.post('/assign-user', checkAuthenticated, async (req, res) => {
  if (!req.body.annotator || !req.body.batchObject) {
    res.redirect('/batch-assign')
    return
  }
  let annotators = []
  let ranges = []
  if (!Array.isArray(req.body.annotator)) {
    annotators.push(req.body.annotator)
  } else {
    annotators = req.body.annotator
  }
  if (!Array.isArray(req.body.batchObject)) {
    ranges.push([Number(req.body.batchObject.split('-')[0]), Number(req.body.batchObject.split('-')[1])])
  } else {
    req.body.batchObject.forEach(function(batch) {
      ranges.push([Number(batch.split('-')[0]), Number(batch.split('-')[1])])
    });
  }
  const promises = [];
  for (let j = 0; j < ranges.length; j ++) {
    const range = ranges[j]
    for (let i = range[0]; i <= range[1]; i ++) {
      const oid = pad(i, 8);
      const objectDocSnapshot = await db.collection("objects").doc(oid).get();
      if (objectDocSnapshot.exists) {
        for (let k = 0; k < annotators.length; k++) {
          const annotator = annotators[k]
          const aid = annotator + "*" + oid;
          const annotationDocSnapshot = await db.collection("annotation").doc(aid).get();
          if (!annotationDocSnapshot.exists) {
            let annotation_data = {
              assignedBy: req.user.id,
              assignTime: new Date(),
              done: false,
              objectId: oid,
              annotator: annotator
            }
            promises.push(db.collection("annotations").doc(aid).set(annotation_data))
          }
        }
      }
    }
  }

  await Promise.all(promises)

  res.redirect('/batch-assign')
});

module.exports = router;