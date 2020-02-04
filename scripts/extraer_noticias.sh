#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
ruta_CRAWLER="$DIR/../crawler"

echo "¿Por cual fecha deberíamos empezar? (dd-MM-YYYY)"
read fechaIni

echo "¿En qué fecha deberíamos terminar? (dd-MM-YYYY)"
read fechaFin

cd "$ruta_CRAWLER"

scrapy crawl Spider_ElPais -a fechaIni="$fechaIni" -a fechaFin="$fechaFin"
scrapy crawl Spider_ElMundo -a fechaIni="$fechaIni" -a fechaFin="$fechaFin"
scrapy crawl Spider_20Minutos -a fechaIni="$fechaIni" -a fechaFin="$fechaFin"
scrapy crawl Spider_ElConfidencial -a fechaIni="$fechaIni" -a fechaFin="$fechaFin"
scrapy crawl Spider_Marca -a fechaIni="$fechaIni" -a fechaFin="$fechaFin"

echo "Operación realizada con éxito."