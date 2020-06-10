# -*- coding: utf-8 -*-

import os
import json

if __name__ == '__main__':

    print("Introduzca <directorioNoticia>/<archivoNoticia>:")
    pathDirectorio = input(">> ")
    filePath = os.getcwd() + "/../creacionDataset/crawlerPeriodicos/" + pathDirectorio
    fileIn = open(filePath, 'r')
    data = json.load(fileIn)

    print("Introduzca el tag que han de tener las noticias:")
    tag = input(">> ")

    print("Introduzca la etiqueta del tema que van a tener las noticias:")
    tema = input(">> ")

    listNoticiasTematicas = []
    for noticia in data:
        if tag in noticia['tagsNoticia']:
            noticia['temaNoticia'] = tema
            listNoticiasTematicas.append(noticia)

    fileIn.close()
    pathHastaDataset = "../creacionDataset/crawlerPeriodicos/dataset_pruebas_ficheros/"
    datasetPathFile = "{}/{}dataset_pruebas_{}.json".format(os.getcwd(),
                                                            pathHastaDataset,
                                                            "_".join(pathDirectorio.split("/")[0].split("_")[1:]))
    if os.path.exists(datasetPathFile):
        fileDaset = open(datasetPathFile, 'r')
        dataset = json.load(fileDaset)
        dataset += listNoticiasTematicas
        fileDaset.close()
    else:
        dataset = listNoticiasTematicas
        
    with open(datasetPathFile, 'w') as fileOut:
        json.dump(dataset, fileOut, indent=4, ensure_ascii=False)
    fileOut.close()

    print("Se han escrito {} noticias nuevas".format(len(listNoticiasTematicas)))

            

