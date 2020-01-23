#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
ruta_EL_PAIS="$DIR/../crawler/crawlerPeriodicos/datos_EL_PAIS"
ruta_EL_MUNDO="$DIR/../crawler/crawlerPeriodicos/datos_EL_MUNDO"
ruta_20_MINUTOS="$DIR/../crawler/crawlerPeriodicos/datos_20_MINUTOS"
ruta_EL_CONFIDENCIAL="$DIR/../crawler/crawlerPeriodicos/datos_EL_CONFIDENCIAL"
ruta_MARCA="$DIR/../crawler/crawlerPeriodicos/datos_MARCA"

echo "¿Estás seguro de borrar todas las noticias?(S/N)"

read confirmacion
confirmacion=$(echo "$confirmacion" | tr '[:upper:]' '[:lower:]')

if [$confirmacion="s"]
then
    echo "SI"
else
    echo "NO"
fi
exit