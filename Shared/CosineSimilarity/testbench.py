from PyUtils import *
import random
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import re


def parseTrackingCoords(entries):
	coordExtract = re.compile('TRACKING\[([0-9]+)\]')
	parseDists = re.compile('([^[,]+)\[([0-9]+)\]')
	stats = dict()
	for e in entries:
		[__coord, __ds] = e.split()
		coord = Cmn.demanduniq(coordExtract.findall(__coord))
		ds = parseDists.findall(__ds)
		assert not coord in stats
		stats[coord] = ds 
	return stats


def randomMatrix(r, c, out, l=-1, h=1):
	M = [[random.uniform(l, h) for j in range(c)] for i in range(r)]
	with open(out, 'w') as outfile:
		if c > 1:
			for i in range(r):
				outfile.write('{0} {1}\n'.format(i, ' '.join([str(x) for x in  M[i]])))
		else:
			outfile.write('\n'.join([str(row[0]) for row in M])) 
	return (out, M)

def hash_matrix(f):
	rows = [x.strip().split() for x in Cmn.contents(f) if x.strip()]
	return {int(row[0]) : [float(x) for x in row[1:]] for row in rows} 

def vector(f):
	return [float(x.strip()) for x in Cmn.contents(f)] 

def np_reconstruct(l, e, r, out):
	rh = hash_matrix(r)
	eh = vector(e)
	R = np.matrix([rh[i] for i in range(len(rh))]).transpose()
	D = np.diag(eh)
	lh = hash_matrix(l)
	L = np.matrix([lh[i] for i in range(len(lh))])
	A = L*D*R
	(x, y) = A.shape

	with open(out, 'w') as outfile:
		for i in range(x):
			for j in range(y):
				outfile.write('{0} {1} {2}\n'.format(i, j, A[i, j]))
	return out 

def generate(c, path, threads=1):
	path = path + '/' + c
	Cmn.makedir(path)
	dL = int(random.uniform(1000, 2000))
	rank =  int(random.uniform(1000, 2000))
	left, left_matrix = randomMatrix(dL, rank, out='{2}/test.{0}.left.{1}'.format(c, 0, path))
	eigen, eigen_values = randomMatrix(rank, 1, out='{1}/test.{0}.scale'.format(c, path))
	scaled = np.dot(np.array(left_matrix),  np.diag([e[0] for e in eigen_values]))
	scaled_f = '{0}/scaled.{1}.matrix'.format(path, c)
	scaled_cs_f = '{0}/scaled.{1}.cs'.format(path, c)
	np.savetxt(scaled_f, scaled)
	np.savetxt(scaled_cs_f, cosine_similarity(scaled))

	config = {
			'left' :  left,
			'eigen' : eigen,  
			'rank' : rank,
			'd_left' : dL,
			'block' : dL/50 + 1,
			'track' : dL,
			'scaled' : scaled_f,
			'similarity' : scaled_cs_f,
			'path' : path,
			'tag' : c,
		}

	config['config'] = '{1}/test.{0}.config'.format(c, path)
	print Json.dumpf(config['config'], config)
	Json.pprint(config)
	task = Task('./load -nV:{d_left} -eigen-values:{eigen} -vectors:{left} -dim:{rank} -track:{track} -block-size:{block} -prefix:{path}/closest_coords.{tag}'.format(**config))
	status = task()

	Cmn.log([status['return'], status['cmd']])

	ok = re.compile('#Thread:[0-9]+\.\.OK:')
	trackedLogs = [e.strip() for e in status['err'] if ok.match(e)]
	logs = [l.split()[0].split(':')[-1] for l in trackedLogs]
	verify(config['config'], logs)


	return config


def verify(configfile, tracked):
	def checkTracked(coord, expected, computed, nTrack, tol):
		sorted_e = sorted(enumerate(list(expected)), key = lambda x: x[1])
		for i, e in enumerate(sorted_e[-nTrack:]):
			assert abs(c[i][0] - e[1]) < tol
			#print coord, [i, e[1], c[i][0], e[0]]
		return True

	tol = 0.0001
	config = Json.loadf(configfile)    #  dict([x.strip().split('=') for x in Cmn.contents(configfile) if x.strip()])
	similarity = np.loadtxt(config['similarity']) 
	expected = {i:list(v) for i, v in enumerate(list(similarity))}		
	computed = parseTrackingCoords([e for arg in tracked for e in Cmn.entries(arg)])
	nTrack = int(config['track'])
	errs = list()
	for i in expected:
		e = expected[i]
		__c = computed[str(i)]
		c = map(lambda x:(float(x[0]), int(x[1])), __c) 
		assert checkTracked(i, e, c, nTrack, tol)
		for dist, coord in c:
			err = abs(e[coord] - dist)
			errs.append(err) 
			assert err < tol, [e[coord], coord, dist]
	assert len(errs) == config['d_left'] ** 2
	Cmn.log('cumulative_error/n:' + str([sum(errs), len(errs)]))



if __name__ == '__main__':
	import sys
	if sys.argv[1] == '-generate-and-verify':
		generate(sys.argv[2], sys.argv[3])
	else:
		Cmn.log('usage:\n\tapy testbench.py -generate-and-verify test0 ./testsuites')
 
