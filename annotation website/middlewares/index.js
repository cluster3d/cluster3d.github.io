const auth = require('firebase-admin').auth();
const User = require('../models/user');

module.exports.checkAuthenticated = async (req, res, next) => {
  try {
    const decodedIdToken = await auth.verifyIdToken(req.cookies.token || '');
    const user = new User(decodedIdToken.uid);
    req.user = await user.get();
    next();
  } catch(e) {
    return res.redirect('/login');
  }
}