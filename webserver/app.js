const express = require('express')
const app = express()
const port = 8080

data = {
    'A':{
        'Total':1000,
        'Available':2,
        'Occupancy':1 // %
    },
    'B':{
        'Total':1000,
        'Available':2,
        'Occupancy':1 // %
    },
    'C':{
        'Total':1000,
        'Available':2,
        'Occupancy':1 // %
    }
};

app.get('/', function(req, res) {
    res.send('');
});

app.get('/live', function(req, res) {
    res.send(data);
});

app.all('/api', function(req, res){
    console.log(req.query.data);
    res.send('1');
});


app.listen(port);