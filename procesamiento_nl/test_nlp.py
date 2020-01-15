from __future__ import unicode_literals
import sys
import spacy



if __name__ == "__main__":

    try:
        frase = sys.argv[1]
    except:
        print('Ejecuta: python test_nlp.py "PON UNA FRASE"')
        sys.exit(">> Error en los parametros")
        
    nlp = spacy.load('es_core_news_sm')
    doc = nlp(frase)

    for token in doc:
        print(token.text, token.lemma_, token.pos_, token.tag_, token.dep_, token.shape_, token.is_alpha, token.is_stop)
        print("\n")

