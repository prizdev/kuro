var pg = require('pg');
var fs = require('fs');
var path = require('path');
var mkdirp = require('mkdirp');
var kuro_renderer = require('kuro_renderer');
var conString = "postgres://ubuntu:KuroB192@localhost/kuro_db";
var insert_query = "INSERT INTO tasks(status, nogl, gif, uname, pass, host) VALUES($1, $2, $3, $4, $5, $6) returning name";
var count_query = "SELECT count(*) FROM jobs";
var job_query = "INSERT INTO jobs(taskname) VALUES($1)";
module.exports = function(req, res) {
    console.log(req.body);
    if(req.body.nogl !== undefined && req.body.gif !== undefined) {
        pg.connect(conString, function(err, client, done) {
            if(err) {console.log(err);done();}
            else client.query(insert_query, ['queued', parseInt(req.body.nogl), parseInt(req.body.gif), 'username', 'password', 'hostname'], function(err, insert_results) {
                console.log(insert_results.rows[0].name);
                mkdirp('./assets/'+insert_results.rows[0].name+'/input', function(err) {
                    if(err) res.send('task creation failed: directory creation failed1');
                    else mkdirp('./assets/'+insert_results.rows[0].name+'/output', function(err) {
                        if(err) res.send('task creation failed: directory creation failed2');
                        else mkdirp('./assets/'+insert_results.rows[0].name+'/render', function(err) {
                            if(err) res.send('task creation failed: directory creation failed3');
                            else {
                                Object.keys(req.files).forEach(function(e){
                                    var derp = fs.statSync(path.join(__dirname, '/../../../assets/'+insert_results.rows[0].name+'/input/'));//req.files[e][0].path);
                                    console.log(derp.isFile());
                                    console.log(derp.isDirectory());
                                    fs.renameSync(req.files[e][0].path, path.join(__dirname, '/../../../assets/'+insert_results.rows[0].name+'/input/' + e + req.files[e][0].originalname.split('.')[1]));
                                });
                                client.query(count_query, function(err, count_results) {
                                    if(err) {console.log(err);done();}
                                    else client.query(job_query, [insert_results.rows[0].name] , function(err, job_results) {
                                        done();
                                        if(err) console.log(err);
                                        console.log(count_results.rows[0].count);
                                        if(parseInt(count_results.rows[0].count) === 0) {
                                            res.send({
                                                success: true,
                                                message: 'Render added to queue'
                                            });
                                            //kuro_renderer();
                                        }
                                    });
                                });
                            }
                        });
                    });
                });
            });
        });
    }
    else {
        res.send('nogl size and gif size required');
    }
};
