var createError = require('http-errors');
var express = require('express');
var path = require('path');
var cookieParser = require('cookie-parser');
var bodyParser = require('body-parser')
var logger = require('morgan');
var admin = require('firebase-admin');
var hbs = require( 'express-handlebars');
var firebaseServiceAccount = require('./secrets').firebaseServiceAccount;

admin.initializeApp({
  credential: admin.credential.cert(firebaseServiceAccount)
});

var indexRouter = require('./routes/index');
var loginRouter = require('./routes/login');
var taxonomyRouter = require('./routes/taxonomy');
var selectRouter = require('./routes/select');
var assignRouter = require('./routes/assign');
var batchAssignRouter = require('./routes/batchAssign');

var app = express();

app.use(bodyParser.urlencoded({
  extended: true
}));

// view engine setup
app.set('views', path.join(__dirname, 'views'));
app.set('view engine', 'hbs');

app.engine( 'hbs', hbs( {
  extname: 'hbs',
  defaultView: 'default',
  // layoutsDir: __dirname + '/views/pages/',
  partialsDir: __dirname + '/views/partials/'
}));

app.use('/jquery', express.static(__dirname + '/node_modules/jquery/dist/'));
app.use(logger('dev'));
app.use(express.json());
app.use(express.urlencoded({ extended: false }));
app.use(cookieParser());
app.use(express.static(path.join(__dirname, 'public')));
app.use(express.static('/abc_dataset'))

app.use('/', indexRouter);
app.use('/login', loginRouter);
app.use('/taxonomy', taxonomyRouter);
app.use('/assign', assignRouter);
app.use('/select', selectRouter);
app.use('/batch-assign', batchAssignRouter);

// catch 404 and forward to error handler
app.use(function(req, res, next) {
  next(createError(404));
});

// error handler
app.use(function(err, req, res, next) {
  // set locals, only providing error in development
  res.locals.message = err.message;
  res.locals.error = req.app.get('env') === 'development' ? err : {};

  // render the error page
  res.status(err.status || 500);
  res.render('error');
});

// const yaml = require('js-yaml');
// const fs   = require('fs');
// console.log('dddd~~~');
// // Get document, or throw exception on error
// try {
//   const doc = yaml.safeLoad(fs.readFileSync('../images/4999_feat.yml', 'utf8'));
//   console.log('dddd');
// } catch (e) {
//   console.log('ssss');
// }

process.on('uncaughtException', function (exception) {
  console.log(exception); // to see your exception details in the console
});

module.exports = app;
