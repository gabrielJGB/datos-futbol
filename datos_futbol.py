import requests
import bs4
from time import sleep
from pathlib import Path
from datetime import date    

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:95.0) Gecko/20100101 Firefox/95.0'}

paisesID = ['ARG','BRA','ENG','FRA','USA','GER','MEX','ESP','CHI','COL','PAR','PER','ITA','GRE','JPN','NED','POR','RUS','SCO','TUR','UKR','URU']

# paisesID = ['ARG','BRA']

contenido = "{\"paises\":["

for k in range(len(paisesID)):
	sleep(0.5)
	linkPais = "https://es.soccerwiki.org/country.php?countryId=%s" %(paisesID[k])
	res1 = requests.get(linkPais,headers=headers)
	soup1 = bs4.BeautifulSoup(res1.text, 'html.parser')
	nombrePais = soup1.select('.heading-component h1')[0].text.lower()

	contenidoClubes = soup1.select('#allleagues > div.col-lg-8.col-12 > div:nth-child(4) > table > tbody tr')

	linksEquipos = []

	for i in range(1,len(contenidoClubes)):
		linksEquipos.append('https://es.soccerwiki.org'+contenidoClubes[i].select('a')[0]['href'])

	print('-------------------------------------\n'+nombrePais + ':')
	
	contenido += """
		{
			"pais":"%s",
			"equipos":[

	""" %(nombrePais)

	#for i in range(0,2): 
	for i in range(len(linksEquipos)):
		sleep(0.5)
		res = requests.get(linksEquipos[i],headers=headers)
		soup = bs4.BeautifulSoup(res.text, 'html.parser')
		contenidoElemento = soup.select('#datatable > tbody tr')
		infoEquipo = soup.select('.player-info-corporate .player-info-main p')
		nombre_equipo = soup.select('title')[0].text
		nombre_equipo = nombre_equipo[:-60]
		infoEquipo[3].span.decompose()
		nombre_corto = infoEquipo[3].text.strip()
		if len(infoEquipo[0].select('a')) != 0:
			tecnico = infoEquipo[0].select('a')[1].text
		else:
			tecnico = 'Sin datos'
		linkEscudo = soup.select('.player-img img')[0]['data-src']
		infoEquipo[4].span.decompose()
		fundacion = infoEquipo[4].text.strip()
		infoEquipo[7].span.decompose()
		ubicacion = infoEquipo[7].text.strip()
		estadio = infoEquipo[5].select('a')[0].text
		liga = infoEquipo[6].select('a')[0].text

		print(nombre_equipo + ':Ok')

		contenido += """
		
		{"nombre_equipo":"%s",
		"nombre_corto":"%s",
		"escudo":"%s",
		"tecnico":"%s",
		"fundacion":"%s",
		"ubicacion":"%s",
		"estadio":"%s",
		"liga":"%s",
		"jugadores":[""" %(nombre_equipo,nombre_corto,linkEscudo,tecnico,fundacion,ubicacion,estadio,liga)

		for i in range(len(contenidoElemento)):	
			ID = contenidoElemento[i].select('td')[3].select('a')[0]['href']
			ID = ID.replace('/player.php?pid=','')
			nombre = contenidoElemento[i].select('td')[3].select('a')[0].text
			numero = contenidoElemento[i].select('td')[0].text
			pais = contenidoElemento[i].select('td')[1].select('a')[0]['title']
			foto = contenidoElemento[i].select('td')[2].select('img')[0]['data-src']
			posicion = contenidoElemento[i].select('td')[4].select('span')[0]['title']
			posicion_codigo =  contenidoElemento[i].select('td')[4].select('span')[0].text
			edad = contenidoElemento[i].select('td')[5].text

			contenido += """

			{"ID":"%s",
			"nombre":"%s",
			"numero":"%s",
			"pais":"%s",
			"link_foto":"%s",
			"posicion":"%s",
			"posicion_codigo":"%s",
			"edad":"%s"},""" %(ID,nombre,numero,pais,foto,posicion,posicion_codigo,edad)

		contenido = contenido[:-1]
		contenido += ']},'

	contenido = contenido[:-1]
	contenido+=']},'

contenido = contenido[:-1]
contenido += ']}'

contenido = contenido.replace('es\":]','es\":[]')

fecha = date.today().isoformat()
ruta = Path(__file__).parent.resolve().joinpath('datos_'+fecha+'.json')
archivo = open(ruta,'w',encoding='utf-8')
archivo.write(contenido)
archivo.close()
ruta = str(ruta)
print('\nGuardado en: ' +ruta+ '\n')

