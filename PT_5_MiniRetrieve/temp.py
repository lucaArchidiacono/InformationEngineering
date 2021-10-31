
""" FEHLT """

# Datenstrukturen aufbauen

""" FEHLT """

# Hier sind die Dokumente fertig indexiert... Wir bauen jetzt die Normalisers und Idfs

dnorm = {}
idf = {}

# Pro File:

for file in noninvindex.keys():
	dnorm[file] = 0.0

# Pro Wort: berechne Idf, summiere dnorm auf

	for word in noninvindex[file].keys():
""" FEHLT """

	dnorm[file] = math.sqrt( dnorm[file] )

# Lese die Queies

querydir = sys.argv[2]

files = [ file for file in os.listdir(querydir) if os.path.isfile(os.path.join(querydir,file)) ]

for file in files:

# Querydatei lesen

	with open(os.path.join(querydir,file), 'r') as infile:
		text = infile.read()

# Tokenisieren...

""" FEHLT """

# Datenstruktur f�r Queries bauen

		if len(word):
			queries[file][word] += 1

# Wir sortieren die Queries vor dem Processing..

queryids = queries.keys()
queryids.sort(key=int)

# Pro Query:

for query in queryids:
	sys.stderr.write("QUERY: " + query + "\n")
	sys.stderr.flush()

# Querynorm zur�ckstellen, Akku initialisieren

	qnorm = 0.0
	accu = {}

# pro Queryterm:

	for word in queries[query].keys():

# Spezialfall: Queryterm kommt in KEINEM Dokument vor. Hat auf Ranking keinen Einfluss, aber �ndert die absoluten Scores

		if not word in idf:
			idf[word] = math.log( 1.0 + numdocs )

# Gewicht Queryterm, aufsummieren Qnorm

""" FEHLT """

# Queryterm nachschlagen

		if word in invindex:
			for document in invindex[word].keys():

# Gewicht Queryterm in Dokument

""" FEHLT """

# Akku aufdatieren

""" FEHLT """

	qnorm = math.sqrt(qnorm)

# Akkus normalisieren

	for entry in accu.keys():
""" FEHLT """

# Rangliste sortieren

	results = sorted(accu.items(), key=operator.itemgetter(1), reverse=True)

# Ausgabe Resultate

	for rankcounter in xrange(min(10, len(results))):
		print ("{0} Q0 {1} {2} {3} miniRetrieve".format(query, results[rankcounter][0], rankcounter, results[rankcounter][1]))
