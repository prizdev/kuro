var pg = require('pg');
var fs = require('fs');
var path = require('path');
var mkdirp = require('mkdirp');
var kuro_renderer = require('kuro_renderer');
var needle = require('needle');

var conString = "postgres://ubuntu:KuroB192@localhost/kuro_db";
var insert_query = "INSERT INTO tasks(status, nogl, gif, uname, pass, host, model_id, user_id) VALUES($1, $2, $3, $4, $5, $6, $7, $8) returning name";
var count_query = "SELECT count(*) FROM jobs";
var job_query = "INSERT INTO jobs(taskname) VALUES($1)";

module.exports = function(req, res) {

    if( req.body.nogl      !== undefined &&
        req.body.gif       !== undefined &&
        req.body.user_id   !== undefined &&
        req.body.model_id  !== undefined &&
        req.body.host      !== undefined &&
        req.body.user      !== undefined &&
        req.body.pass      !== undefined &&
        (req.body.geometry_url !== undefined || req.files.geometry !== undefined)  &&
        (req.body.diffuse_url  !== undefined || req.files.diffuse  !== undefined)
    ) {
        pg.connect( conString, function( err, client, done ) {

            if (err) { error( err, res ); done(); }
            else client.query( insert_query, [
                'queued',
                parseInt(req.body.nogl),
                parseInt(req.body.gif),
                req.body.user,
                req.body.pass,
                req.body.host,
                parseInt(req.body.model_id),
                parseInt(req.body.user_id)
            ], function(err, insert_results) {

                mkdirp('./assets/'+insert_results.rows[0].name+'/input', function(err) {

                    if (err) res.send('task creation failed: directory creation failed1');
                    else mkdirp('./assets/'+insert_results.rows[0].name+'/output', function(err) {

                        if (err) res.send('task creation failed: directory creation failed2');
                        else mkdirp('./assets/'+insert_results.rows[0].name+'/render', function(err) {

                            if (err) res.send('task creation failed: directory creation failed3');
                            else {

                                if (req.body.geometry_url) {
                                    console.log('geo url: '+req.body.geometry_url);
                                    var obj_out = fs.createWriteStream('./assets/'+insert_results.rows[0].name+'/input/geometry.obj');
                                    needle.get(req.body.geometry_url).pipe(obj_out);
                                }

                                if (req.body.diffuse_url) {
                                    console.log('diff url: '+req.body.diffuse_url);
                                    var diff_out = fs.createWriteStream('./assets/'+insert_results.rows[0].name+'/input/diffuse.jpg');
                                    needle.get(req.body.diffuse_url).pipe(diff_out);
                                }

                                Object.keys(req.files).forEach(function(e){
                                    console.log('file ' + e + ' - ' + req.files[e][0].path);
                                    fs.renameSync(req.files[e][0].path, path.join(process.cwd(), '/assets/'+insert_results.rows[0].name+'/input/' + e + '.' + req.files[e][0].originalname.split('.')[1].toLowerCase()));
                                });

                                client.query(count_query, function(err, count_results) {
                                    if(err) {error(err, res);done();}
                                    else client.query(job_query, [insert_results.rows[0].name] , function(err, job_results) {
                                        done();
                                        if(err) error(err, res);
                                        res.send({
                                            success: true,
                                            data: {
                                                message: 'Render added to queue',
                                                taskname: insert_results.rows[0].name
                                            }
                                        });
                                        if(parseInt(count_results.rows[0].count) === 0) {
                                            kuro_renderer();
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
        res.send('Missing Params');
    }
};

function error(err, res) {
    res.send({
        success: false,
        data: err
    });
}
