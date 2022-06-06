const express = require('express')
const bodyParser = require('body-parser')
const datos = require('./datos_2022-06-05.json')
const app = express()
const PORT = process.env.PORT || 3000;

app.use(bodyParser.urlencoded({
    extended: true
}))
app.use(express.static('public'));
app.use(bodyParser.json())
app.set('view engine', 'ejs');


const indexRouter = require('./routes/routes.js');

app.use('/',indexRouter)

app.use((req, res) => {
    res.status(404).send('Error 404: Pagina no encontrada');
});

app.listen(PORT, () => {
    console.log('Listening on port '+PORT);
})