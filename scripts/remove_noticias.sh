#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
ruta_EL_PAIS="$DIR/../crawler/crawlerPeriodicos/datos_EL_PAIS"
ruta_EL_MUNDO="$DIR/../crawler/crawlerPeriodicos/datos_EL_MUNDO"
ruta_20_MINUTOS="$DIR/../crawler/crawlerPeriodicos/datos_20_MINUTOS"
ruta_EL_CONFIDENCIAL="$DIR/../crawler/crawlerPeriodicos/datos_EL_CONFIDENCIAL"
ruta_MARCA="$DIR/../crawler/crawlerPeriodicos/datos_MARCA"

echo "¿Estás seguro de borrar todas las noticias?(S/n)"

read confirmacion
confirmacion=$(echo "$confirmacion" | tr '[:upper:]' '[:lower:]')

if [ "$confirmacion" = "s" ] || [ "$confirmacion" = "si" ] || [ "$confirmacion" = "y" ] || [ "$confirmacion" = "yes" ];
then
    rm -r "$ruta_EL_PAIS/"
    mkdir "$ruta_EL_PAIS/"
    rm -r "$ruta_EL_MUNDO/"
    mkdir "$ruta_EL_MUNDO/"
    rm -r "$ruta_20_MINUTOS/"
    mkdir "$ruta_20_MINUTOS/"
    rm -r "$ruta_EL_CONFIDENCIAL/"
    mkdir "$ruta_EL_CONFIDENCIAL/"
    rm -r "$ruta_MARCA/"
    mkdir "$ruta_MARCA/"
else
    echo "Abortando operación..."
fi