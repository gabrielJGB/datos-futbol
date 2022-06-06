var express = require('express');
var router = express.Router();
const indexController = require("../controllers/indexController");


router.get('/', indexController.index);
router.get('/:pais', indexController.mostrarPais);
router.get('/:pais/:equipo', indexController.mostrarEquipo);


module.exports = router;