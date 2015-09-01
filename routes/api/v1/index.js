var express = require('express');
var router = express.Router();
var path = require('path');

// includes
var includes = {
    render : require(path.join(__dirname, 'render')),
    status : require(path.join(__dirname, 'status'))
};
router.post('/:request', function(req, res) {
    var includes_list = Object.keys(includes);
    var includes_length = includes_list.length;
    var i;
    for(i = includes_length; i >= 0; --i) {
        if(includes_list[i] === req.params.request) {
            includes[includes_list[i]](req, res);
            i = -1;
        }
    }
    if(i === -1) {
        res.send({
            success : false,
            data : {},
            err : 'API Call not found'
        });
    }
});

module.exports = router;
