#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
ruta_PROCESAMIENTO_LN="$DIR/../creacionHistorial"

cd "$ruta_PROCESAMIENTO_LN"

python historialNoticias.py EL_CONFIDENCIAL https://www.elconfidencial.com/espana/cataluna/2019-10-20/quim-torra-vuelve-a-llamar-a-pedro-sanchez-sin-obtener-respuesta_2291844/ JUICIO_PROCÉS 01
python historialNoticias.py EL_MUNDO https://www.elmundo.es/internacional/2020/02/09/5e405358fdddff0f278b45bd.html BREXIT 02
python historialNoticias.py EL_PAIS https://elpais.com/cultura/2019/04/27/actualidad/1556380153_549141.html INCENDIO_NÔTRE_DAME 03
python historialNoticias.py EL_MUNDO https://www.elmundo.es/deportes/baloncesto/nba/2020/02/07/5e3dd42c21efa035088b459f.html KOBE_BRYANT 07
python historialNoticias.py EL_MUNDO https://www.elmundo.es/espana/2020/03/17/5e6fd1fcfdddff5f1c8b45b3.html CORONAVIRUS 08

echo "Operación realizada con éxito."