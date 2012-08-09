
with open("../files/COTAHIST_A2011.TXT") as f:

	for line in f:
		tipReg	= line[0:1]
		data 	= line[2:9]
		codBdi	= line[10:11]
		codNeg	= line[12:23].rstrip()
		tipMer	= line[24:26]
		nomeRe	= line[27:38]
		print "Codigo %s da empresa %s" % (codNeg, nomeRe)

