import spacy
import string
import re
import math
from sklearn.metrics.pairwise import cosine_distances
import numpy as np
from nltk.corpus import stopwords as stopW

def trataStrings(strr):

    stopwords = stopW.words('spanish')

    regex_pun = re.compile('[%s]' % re.escape(string.punctuation))
    regex_espacios = re.compile('\s\s+')

    strr = regex_pun.sub(' ', strr).strip()
    strr = regex_espacios.sub(' ', strr).strip()

    lst = strr.split(" ")
    lst = [word for word in lst if word.lower() not in stopwords]

    return " ".join(lst)


def my_similitudCoseno(vec1, vec2):

    numerador = sum(vec1[idx] * vec2[idx] for idx in range(vec1.size))
    sum1 = sum(vec1[idx]**2 for idx in range(vec1.size))
    sum2 = sum(vec2[idx]**2 for idx in range(vec2.size))
    denominador = math.sqrt(sum1) * math.sqrt(sum2) 
    if not denominador: 
        return 0.0 
    else: 
        return float(numerador) / denominador


if __name__ == '__main__':

    print(  "#########################################################\n" +
            "#\tImplementación usando similarity() con Spacy\t#\n" +
            "#########################################################")

    # Cargamos el modelo de palabras de Spacy en español
    nlp = spacy.load("es_core_news_md")
    
    # Definimos dos string de test
    strr1 = "Casi 20.000 euros al año. Esa el la cifra que el gobierno pide."
    strr2 = "El Gobierno de Pedro Sánchez y Pablo Iglesias quiere una cifra de muchos euros."
    strr3 = "El gato de San Roque no tiene nabo, porque Ramón Ramirez se lo ha depilado."
    strr4 = "La perra de San Pedro no tiene rabo, porque Iglesias Ramirez se lo ha cortado."

    # Eliminamos los signos de puntución de las dos cadenas
    strr1, strr2, strr3, strr4 = trataStrings(strr1), trataStrings(strr2), trataStrings(strr3), trataStrings(strr4) 

    # Tokenizamos los strings
    doc1, doc2, doc3, doc4 = nlp(strr1), nlp(strr2), nlp(strr3), nlp(strr4)
    
    print("Doc 1:")
    #print(doc1.vector)
    print("1 y 1: {}\t1 y 2: {}\t1 y 3: {}\t1 y 4: {}".format(  round(doc1.similarity(doc1), 5),
                                                                round(doc1.similarity(doc2), 5),
                                                                round(doc1.similarity(doc3), 5),
                                                                round(doc1.similarity(doc4), 5)))
    print("Doc 2:")
    #print(doc2.vector)
    print("2 y 1: {}\t2 y 2: {}\t2 y 3: {}\t2 y 4: {}".format(  round(doc2.similarity(doc1), 5),
                                                                round(doc2.similarity(doc2), 5),
                                                                round(doc2.similarity(doc3), 5),
                                                                round(doc2.similarity(doc4), 5)))
    print("Doc 3:")
    #print(doc3.vector)
    print("3 y 1: {}\t3 y 2: {}\t3 y 3: {}\t3 y 4: {}".format(  round(doc3.similarity(doc1), 5),
                                                                round(doc3.similarity(doc2), 5),
                                                                round(doc3.similarity(doc3), 5),
                                                                round(doc3.similarity(doc4), 5)))
    print("Doc 4:")
    #print(doc4.vector)
    print("4 y 1: {}\t4 y 2: {}\t4 y 3: {}\t4 y 4: {}".format(  round(doc4.similarity(doc1), 5),
                                                                round(doc4.similarity(doc2), 5),
                                                                round(doc4.similarity(doc3), 5),
                                                                round(doc4.similarity(doc4), 5)))

    print(  "#########################################################\n" +
            "#\tImplementación de similitud coseno de sklearn\t#\n" +
            "#########################################################")
            
    # Cosine distance is defined as 1.0 minus the cosine similarity.

    cosDist11 = round(1 - cosine_distances(doc1.vector.reshape(1,-1), doc1.vector.reshape(1,-1))[0][0], 5)
    cosDist12 = round(1 - cosine_distances(doc1.vector.reshape(1,-1), doc2.vector.reshape(1,-1))[0][0], 5)
    cosDist13 = round(1 - cosine_distances(doc1.vector.reshape(1,-1), doc3.vector.reshape(1,-1))[0][0], 5)
    cosDist14 = round(1 - cosine_distances(doc1.vector.reshape(1,-1), doc4.vector.reshape(1,-1))[0][0], 5)
    cosDist21 = round(1 - cosine_distances(doc2.vector.reshape(1,-1), doc1.vector.reshape(1,-1))[0][0], 5)
    cosDist22 = round(1 - cosine_distances(doc2.vector.reshape(1,-1), doc2.vector.reshape(1,-1))[0][0], 5)
    cosDist23 = round(1 - cosine_distances(doc2.vector.reshape(1,-1), doc3.vector.reshape(1,-1))[0][0], 5)
    cosDist24 = round(1 - cosine_distances(doc2.vector.reshape(1,-1), doc4.vector.reshape(1,-1))[0][0], 5)
    cosDist31 = round(1 - cosine_distances(doc3.vector.reshape(1,-1), doc1.vector.reshape(1,-1))[0][0], 5)
    cosDist32 = round(1 - cosine_distances(doc3.vector.reshape(1,-1), doc2.vector.reshape(1,-1))[0][0], 5)
    cosDist33 = round(1 - cosine_distances(doc3.vector.reshape(1,-1), doc3.vector.reshape(1,-1))[0][0], 5)
    cosDist34 = round(1 - cosine_distances(doc3.vector.reshape(1,-1), doc4.vector.reshape(1,-1))[0][0], 5)
    cosDist41 = round(1 - cosine_distances(doc4.vector.reshape(1,-1), doc1.vector.reshape(1,-1))[0][0], 5)
    cosDist42 = round(1 - cosine_distances(doc4.vector.reshape(1,-1), doc2.vector.reshape(1,-1))[0][0], 5)
    cosDist43 = round(1 - cosine_distances(doc4.vector.reshape(1,-1), doc3.vector.reshape(1,-1))[0][0], 5)
    cosDist44 = round(1 - cosine_distances(doc4.vector.reshape(1,-1), doc4.vector.reshape(1,-1))[0][0], 5)
    
    print("Doc 1:")
    print("1 y 1: {}\t1 y 2: {}\t1 y 3: {}\t1 y 4: {}".format(  cosDist11,
                                                                cosDist12,
                                                                cosDist13,
                                                                cosDist14))
    print("Doc 2:")
    print("2 y 1: {}\t2 y 2: {}\t2 y 3: {}\t2 y 4: {}".format(  cosDist21,
                                                                cosDist22,
                                                                cosDist23,
                                                                cosDist24))
    print("Doc 3:")
    print("3 y 1: {}\t3 y 2: {}\t3 y 3: {}\t3 y 4: {}".format(  cosDist31,
                                                                cosDist32,
                                                                cosDist33,
                                                                cosDist34))
    print("Doc 4:")
    print("4 y 1: {}\t4 y 2: {}\t4 y 3: {}\t4 y 4: {}".format(  cosDist41,
                                                                cosDist42,
                                                                cosDist43,
                                                                cosDist44))

    print(  "#########################################################\n" +
            "#\tImplementación propia de similitud coseno\t#\n" +
            "#########################################################")

    my_cosDist_11 = round(my_similitudCoseno(doc1.vector, doc1.vector), 5)
    my_cosDist_12 = round(my_similitudCoseno(doc1.vector, doc2.vector), 5)
    my_cosDist_13 = round(my_similitudCoseno(doc1.vector, doc3.vector), 5)
    my_cosDist_14 = round(my_similitudCoseno(doc1.vector, doc4.vector), 5)
    my_cosDist_21 = round(my_similitudCoseno(doc2.vector, doc1.vector), 5)
    my_cosDist_22 = round(my_similitudCoseno(doc2.vector, doc2.vector), 5)
    my_cosDist_23 = round(my_similitudCoseno(doc2.vector, doc3.vector), 5)
    my_cosDist_24 = round(my_similitudCoseno(doc2.vector, doc4.vector), 5)
    my_cosDist_31 = round(my_similitudCoseno(doc3.vector, doc1.vector), 5)
    my_cosDist_32 = round(my_similitudCoseno(doc3.vector, doc2.vector), 5)
    my_cosDist_33 = round(my_similitudCoseno(doc3.vector, doc3.vector), 5)
    my_cosDist_34 = round(my_similitudCoseno(doc3.vector, doc4.vector), 5)
    my_cosDist_41 = round(my_similitudCoseno(doc4.vector, doc1.vector), 5)
    my_cosDist_42 = round(my_similitudCoseno(doc4.vector, doc2.vector), 5)
    my_cosDist_43 = round(my_similitudCoseno(doc4.vector, doc3.vector), 5)
    my_cosDist_44 = round(my_similitudCoseno(doc4.vector, doc4.vector), 5)   
    
    print("Doc 1:")
    print("1 y 1: {}\t1 y 2: {}\t1 y 3: {}\t1 y 4: {}".format(  my_cosDist_11,
                                                                my_cosDist_12,
                                                                my_cosDist_13,
                                                                my_cosDist_14))
    print("Doc 2:")
    print("2 y 1: {}\t2 y 2: {}\t2 y 3: {}\t2 y 4: {}".format(  my_cosDist_21,
                                                                my_cosDist_22,
                                                                my_cosDist_23,
                                                                my_cosDist_24))
    print("Doc 3:")
    print("3 y 1: {}\t3 y 2: {}\t3 y 3: {}\t3 y 4: {}".format(  my_cosDist_31,
                                                                my_cosDist_32,
                                                                my_cosDist_33,
                                                                my_cosDist_34))
    print("Doc 4:")
    print("4 y 1: {}\t4 y 2: {}\t4 y 3: {}\t4 y 4: {}".format(  my_cosDist_41,
                                                                my_cosDist_42,
                                                                my_cosDist_43,
                                                                my_cosDist_44))

    
    
