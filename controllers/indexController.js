const datos = require('../datos_2022-06-05.json')

const index = (req, res) => {

    res.render('index', {
        paises: datos.paises
    });

}

const mostrar_pais = (req, res) => {

    datos.paises.forEach(pais => {

        if (pais.nombre_pais === req.params.pais)
            res.render('pais', {
                nombre_pais: req.params.pais,
                equipos: pais.equipos
            });
    })

}


const mostrar_equipo = (req, res) => {

    datos.paises.forEach(pais => {
        if (pais.nombre_pais === req.params.pais)
            pais.equipos.forEach(equipo => {
                if (equipo.nombre_equipo === req.params.equipo)
                    res.render('equipo', {
                        tecnico: equipo.tecnico,
                        estadio:equipo.estadio,
                        ciudad:equipo.ubicacion,
                        fundacion:equipo.fundacion,
                        liga:equipo.liga,

                        pais: pais.nombre_pais,
                        escudo: equipo.escudo,
                        nombre_equipo: req.params.equipo,
                        jugadores: equipo.jugadores
                    })
            })
    })
}


module.exports = {
    index,
    mostrar_pais,
    mostrar_equipo
};