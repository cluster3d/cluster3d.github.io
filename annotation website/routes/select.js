var express = require('express');
var router = express.Router();
var auth = require('firebase-admin').auth();

/* GET home page. */
router.get('/', function(req, res, next) {
  console.log(req.cookies.token);
  auth.verifyIdToken(req.cookies.token || '').then(function (decodedIdToken) {
    console.log(decodedIdToken);
    res.render('select', { title: '3d-annotation' });
  }).catch(function (err) {
    res.redirect('/login');
  });
});



module.exports = router;
