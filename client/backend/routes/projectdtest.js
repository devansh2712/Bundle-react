const router = require('express').Router();
let newProject = require('../models/projectmodel');

router.route('/').get((req, res) => {
User.find()
    .then(users => res.json(users))
    .catch(err => res.status(400).json('Error: ' + err));
});

router.route('/add').post((req, res) => {
const username = req.body.username;

const newProj = new newProject({username});

newUser.save()
    .then(() => res.json('User added!'))
    .catch(err => res.status(400).json('Error: ' + err));
});

module.exports = router;