var express = require('express');
var router = express.Router();
var rp = require('request-promise');
var firebaseAPIKEY = require('../secrets').firebaseAPIKEY;

router.get('/', function(req, res, next) {
  res.render('login', { title: 'Login' });
});

router.post('/', function (req, res) {
  rp.post({
    uri: 'https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key=' + firebaseAPIKEY,
    form: {
      email: req.body.email,
      password: req.body.password,
      returnSecureToken: true
    },
    json: true
  }).then(function (payload) {
    res.cookie('token', payload.idToken);
    res.redirect('/');
  }).catch(function (err) {
    console.log(err)
    res.redirect('/login');
    
  });
});

module.exports = router;
