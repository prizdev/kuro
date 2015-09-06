var path = require('path');
var mkdirp = require('mkdirp');
var os = require('os');

module.exports = function(req, res) {
    if(req.body.nogl !== undefined && req.body.gif !== undefined) {
        // add task to database
        // check to see if database is running
        // if(not running)
        var taskname = '123456';
        mkdirp('./assets/'+taskname+'/input', function(err) {
            if(err) res.send('task creation failed: directory creation failed');
            else mkdirp('./assets/'+taskname+'/output', function(err) {
                if(err) res.send('task creation failed: directory creation failed');
                else mkdirp('./assets/'+taskname+'/render', function(err) {
                    if(err) res.send('task creation failed: directory creation failed');
                    else {
                        var exec = require('child_process').exec;
                        var cmd;
                        if(os.platform === 'win32') {
                            cmd = '"C:\\Program Files\\Blender Foundation\\Blender\\blender.exe" -b -P ' + path.join(__dirname, 'main.py') + ' -t ' + taskname + ' ' + ' -nogl ' + req.body.nogl + ' -gif ' + req.body.gif;
                        }
                        else {
                            cmd = 'blender -b -P ' + path.join(__dirname, 'main.py') + ' -t ' + taskname + ' ' + '-nogl ' + req.body.nogl + ' -gif ' + req.body.gif;
                        }
                        console.log(cmd);
                        exec(cmd, function(error, stdout, stderr) {
                            console.log('error:', error);
                            console.log('stdout:', stdout);
                            console.log('stderr:', stderr);
                        });
                        res.send({
                            success: true,
                            message: 'Render added to queue'
                        });
                    }
                });
            });
        });
    }
    else {
        res.send('nogl size and gif size required');
    }
};
