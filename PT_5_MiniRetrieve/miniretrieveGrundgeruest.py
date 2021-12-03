#!/usr/bin/python
# coding=iso-8859-1

import collections
import math
import operator
import os.path
import sys
import re

invindex = collections.defaultdict(lambda: collections.defaultdict(int))
noninvindex = collections.defaultdict(lambda: collections.defaultdict(int))
queries = collections.defaultdict(lambda: collections.defaultdict(int))

''' ******************************************** DOCUMENT-SECTION ******************************************** '''
#indir = sys.argv[1]
indir = 'documents'
# Read all Document files
files = [file for file in os.listdir(indir) if os.path.isfile(os.path.join(indir, file))]
# length of all documents
numdocs = len(files)

# Schleife ueber alle Textdateien

for file in files:
    sys.stderr.write("INDEXING: " + file + "\n")
    sys.stderr.flush()

# Textdatei lesen

    with open(os.path.join(indir, file), 'r') as infile:
        text = infile.read()

# Textdatei tokenisieren

        for term in re.split("\W+", text):
            term = term.lower()

# Datenstrukturen aufbauen
            invindex[term][file] += 1
            noninvindex[file][term] += 1

# Hier sind die Dokumente fertig indexiert... Wir bauen jetzt die dNormalisers und Idfs

dnorm = {}
idf = {}

# Pro File:

for file in noninvindex.keys():
    dnorm[file] = 0.0

# Pro Wort: berechne Idf, summiere dnorm auf

    for word in noninvindex[file].keys():
        documentFreqency = len( invindex[word].keys() )
        idf[word] = math.log((1 + numdocs) / (1 + documentFreqency))    
        a = noninvindex[file][word] * idf[word]
        dnorm[file] += (a * a)

    dnorm[file] = math.sqrt(dnorm[file])

''' ******************************************** QUERIES-SECTION ******************************************** '''

#querydir = sys.argv[2]
querydir = 'queries'

files = [file for file in os.listdir(querydir) if os.path.isfile(os.path.join(querydir, file))]

for file in files:

# Querydatei lesen

    with open(os.path.join(querydir, file), 'r') as infile:
        text = infile.read()

# Tokenisieren...

        for word in re.split("\W+", text):
            word = word.lower()

# Datenstruktur fuer Queries bauen

            if len(word):
                queries[file][word] += 1

# Wir sortieren die Queries vor dem Processing..

queryids = sorted(queries.keys(), key=int)

# Pro Query:

for query in queryids:
    sys.stderr.write("QUERY: " + query + "\n")
    sys.stderr.flush()

# Querynorm zurueckstellen, Akku initialisieren

    qnorm = 0.0
    accu = {}

# pro Queryterm:

    for word in queries[query].keys():

# Spezialfall: Queryterm kommt in KEINEM Dokument vor. Hat auf Ranking keinen Einfluss, aber �ndert die absoluten Scores

        if not word in idf:
            idf[word] = math.log(1.0 + numdocs)

# Gewicht Queryterm, aufsummieren Qnorm

        b = queries[query][word] * idf[word]
        qnorm += (b * b)

# Queryterm nachschlagen

        if word in invindex:
            for document in invindex[word].keys():

# Gewicht Queryterm in Dokument

                a = invindex[word][document] * idf[word]
                if not document in accu:
                    accu[document] = 0

# Akku aufdatieren

                accu[document] += (a * b)
    qnorm = math.sqrt(qnorm)

# Akkus normalisieren

    for entry in accu.keys():
        if dnorm[entry] == 0:
            accu[entry] = 0
        else:
            accu[entry] *= 1000
            accu[entry] /= (dnorm[entry] * qnorm)

# Rangliste sortieren

    results = sorted(accu.items(), key=operator.itemgetter(1), reverse=True)

# Ausgabe Resultate

    for rankcounter in range(min(10, len(results))):
        print("{0} Q0 {1} {2} {3} miniRetrieve".format(query, results[rankcounter][0], rankcounter, results[rankcounter][1]))
