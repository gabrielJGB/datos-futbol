var express = require('express');
var router = express.Router();
const indexController = require("../controllers/indexController");


router.get('/', indexController.index);
router.get('/:pais', indexController.mostrar_pais);
router.get('/:pais/:equipo', indexController.mostrar_equipo);


module.exports = router;