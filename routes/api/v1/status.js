var pg = require('pg');
var conString = "postgres://ubuntu:KuroB192@localhost/kuro_db";

module.exports = function(req, res) {
    pg.connect(conString, function(err, client, done) {
        if(err) {error(err, res);done();}
        else client.query('SELECT status FROM tasks WHERE name = $1 LIMIT(1)',[req.body.taskname], function(err, results) {
            if(err) {error(err, res);done();}
            res.send({
                success: true,
                data: {
                    status: results.rows[0].status
                }
            });
        });
    });
};

function error(err, res) {
    res.send({
        success: false,
        data: err
    });
}
