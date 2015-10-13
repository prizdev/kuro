var express = require('express');
var path = require('path');
var favicon = require('serve-favicon');
var logger = require('morgan');
var cookieParser = require('cookie-parser');
var multer = require('multer');
var uploads = multer({ dest: path.join(__dirname, 'tmp' )});
var bodyParser = require('body-parser');
var pg = require('pg');

var app = express();

app.use(uploads.fields([
    {name: 'geometry'},
    {name: 'diffuse' },
    {name: 'specular'},
    {name: 'normal'  }
]));

// view engine setup
//app.set('views', path.join(__dirname, 'views'));
//app.set('view engine', 'jade');

// uncomment after placing your favicon in /public
//app.use(favicon(path.join(__dirname, 'public', 'favicon.ico')));
app.use(logger('dev'));
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: false }));
app.use(cookieParser());
//app.use(express.static(path.join(__dirname, 'public')));
var conString = "postgres://ubuntu:KuroB192@localhost/kuro_db";
pg.connect(conString, function(err, client, done) {
    client.query('DELETE FROM jobs;DELETE FROM tasks', function(err, results) {});
});
app.use('/api/v1/', require(path.join(__dirname, 'routes/api/v1/index')));

module.exports = app;
