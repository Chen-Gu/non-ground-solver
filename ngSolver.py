# INSTALLATION
# You'll need Python (I use 2.7.14) and z3 release binaries, which in turn need python-setuptools.
# Download the appropriate Z3 binary release file from:
# https://github.com/Z3Prover/z3/releases
# and unpack it in $z3path

# SYNOPSIS

# cat input.csv| PYTHONPATH=${PYTHONPATH}:$z3path/bin/python/ LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:$z3path/bin/ python $thisfile
# where $z3path/bin/ is the directory containing libz3.so and $z3path/bin/python/ the directory containing z3/z3.py.

# The resulting amended input.csv will be printed on stdout, hence this program acts as a filter.

import re
from io import StringIO
from z3 import *

def execF(x): # to functionify Python2's exec (useful e.g. inside list comprehension; TODO: manage several args)
	exec(x)

def pr(x): # to functionify Python2's print (useful e.g. inside list comprehension; TODO: manage several args)
	print(x)

def head(string):
	return re.match("^[^$\n]*\n",string).group()

def flatten(listlist):
	return [item for lst in listlist for item in lst]

def sublist(l, indices):
	return [l[i] for i in indices]
	
def chunks(l, n): 
	#return [l[x: x+n] for x in xrange(0, len(l), n)]
	return [l[x: x+n] for x in list(range(0, len(l), n))]
	

def filterPositions(testFun, l):
  #return [i for i in xrange(len(l)) if testFun(l[i])]
  return [i for i in list(range(len(l))) if testFun(l[i])]
  	
def im(rel, l):
	return map(lambda pair: pair[1], filter(lambda pair: pair[0] in l, rel))

def revIm(rel, l):
	return map(lambda pair: pair[0], filter(lambda pair: pair[1] in l, rel))

def compo(g,f):
# functional programming is lame in python, so the following only works for one-argument functions
	return (lambda x: g(f(x)))

remdups=compo(list, dict.fromkeys)

def Compo(funList,x):
	if funList==[]: return x
	return Compo(funList[1:],funList[0](x))

def Compo(funList): lambda x: Compo(funList,x) # NOT WORKING

def symCl(relist):
	relist.extend(map (lambda x: x[::-1], relist))
# SIDE EFFECT ON THE ORIGINAL ARGUMENT!!!!!
	return map(list, remdups(map(tuple,relist)))

def convertor(f, status="unknown", name="benchmark", logic=""):
	v = (Ast * 0)()
	if isinstance(f, Solver):
		a = f.assertions()
		if len(a) == 0:
			f = BoolVal(True)
		else:
			f = And(*a)
		return Z3_benchmark_to_smtlib_string(f.ctx_ref(), name, logic, status, "", 0, v, f.as_ast())

inpuTextOriginal=unicode('''
sqmul(int a, unsigned long long k, int n, int set_threat_lvl):sec_lvl_time_nodelay <= sec_lvl_time_delayed + 100
sqmul(int a, unsigned long long k, int n, int set_threat_lvl):sec_lvl_time_nodelay_ORTEXA15 <= sec_lvl_time_delayed_ORTEXA15 + 100:ORTEXA15:sec_lvl_time_nodelay_ORTEXA15:221:sec_lvl_time_delayed_ORTEXA15:201
sqmul(int a, unsigned long long k, int n, int set_threat_lvl):sec_lvl_time_nodelay_LEON <= sec_lvl_time_delayed_LEON + 100:LEON:sec_lvl_time_nodelay_LEON:124:sec_lvl_time_delayed_LEON:163
sqmul(int a, unsigned long long k, int n, int set_threat_lvl):sec_lvl_time_nodelay_CORTEXM0 <= sec_lvl_time_delayed_CORTEXM0 + 100:CORTEXM0:sec_lvl_time_nodelay_CORTEXM0:155:sec_lvl_time_delayed_CORTEXM0:213
sqmul(int a, unsigned long long k, int n, int set_threat_lvl):sec_lvl_time_nodelay <= (sec_lvl_time_delayed + ngtime.minimum + 100)
sqmul(int a, unsigned long long k, int n, int set_threat_lvl):sec_lvl_time_nodelay_ORTEXA15 <= (sec_lvl_time_delayed_ORTEXA15 + ngtime.minimum + 100):ORTEXA15:sec_lvl_time_nodelay_ORTEXA15:221:sec_lvl_time_delayed_ORTEXA15:201:ngtime:(0,100)
sqmul(int a, unsigned long long k, int n, int set_threat_lvl):sec_lvl_time_nodelay_LEON <= (sec_lvl_time_delayed_LEON + ngtime.minimum + 100):LEON:sec_lvl_time_nodelay_LEON:124:sec_lvl_time_delayed_LEON:163:ngtime:(0,100)
sqmul(int a, unsigned long long k, int n, int set_threat_lvl):sec_lvl_time_nodelay_CORTEXM0 <= (sec_lvl_time_delayed_CORTEXM0 + ngtime.minimum + 100):CORTEXM0:sec_lvl_time_nodelay_CORTEXM0:155:sec_lvl_time_delayed_CORTEXM0:213:ngtime:(0,100)
''')

inpuText=unicode('''
sqmul(int a, unsigned long long k, int n, int set_threat_lvl):sec_lvl_time_nodelay <= sec_lvl_time_delayed + 100
sqmul(int a, unsigned long long k, int n, int set_threat_lvl):sec_lvl_time_nodelay_ORTEXA15 <= sec_lvl_time_delayed_ORTEXA15 + 100:ORTEXA15:sec_lvl_time_nodelay_ORTEXA15:221:sec_lvl_time_delayed_ORTEXA15:201
sqmul(int a, unsigned long long k, int n, int set_threat_lvl):sec_lvl_time_nodelay_LEON <= sec_lvl_time_delayed_LEON + 100:LEON:sec_lvl_time_nodelay_LEON:124:sec_lvl_time_delayed_LEON:163
sqmul(int a, unsigned long long k, int n, int set_threat_lvl):sec_lvl_time_nodelay_CORTEXM0 <= sec_lvl_time_delayed_CORTEXM0 + 100:CORTEXM0:sec_lvl_time_nodelay_CORTEXM0:155:sec_lvl_time_delayed_CORTEXM0:213
sqmul(int a, unsigned long long k, int n, int set_threat_lvl):sec_lvl_time_nodelay <= (sec_lvl_time_delayed + ngtime + 100)
sqmul(int a, unsigned long long k, int n, int set_threat_lvl):sec_lvl_time_nodelay_ORTEXA15 <= (sec_lvl_time_delayed_ORTEXA15 + ngtime + 100):ORTEXA15:sec_lvl_time_nodelay_ORTEXA15:221:sec_lvl_time_delayed_ORTEXA15:201:ngtime:(0,100)
sqmul(int a, unsigned long long k, int n, int set_threat_lvl):sec_lvl_time_nodelay_LEON <= (sec_lvl_time_delayed_LEON + ngtime + 100):LEON:sec_lvl_time_nodelay_LEON:124:sec_lvl_time_delayed_LEON:163:ngtime:(0,100)
sqmul(int a, unsigned long long k, int n, int set_threat_lvl):sec_lvl_time_nodelay_CORTEXM0 <= (sec_lvl_time_delayed_CORTEXM0 + ngtime - 1000):CORTEXM0:sec_lvl_time_nodelay_CORTEXM0:155:sec_lvl_time_delayed_CORTEXM0:213:ngtime:(0,100)
''')

# separatorPositions lists the positions of separators within string. Such separators split string into a number of fields. This function returns the start and end positions witin string of the index-th field.
# Note that the argument string is not used directly (only its length is used).
# E.g: extractBoundaries('ab:cde:fg',[2,6], 1) returns (3,6).
# I found it simpler to quickly reimplement something I could have done with, e.g., re.finditer than to study its documentation.
def extractBoundaries(string, separatorPositions, index):
	extendedSeps=separatorPositions[:]; extendedSeps.insert(0,-1); extendedSeps.append(len(string))
	return((extendedSeps[index]+1, extendedSeps[index+1]))

# separatorPositions lists the positions of separators within string. Such separators split string into a number of fields. This function returns the index-th field. E.g: extractField('ab:cde:fg',[2,6], 1) returns 'cde'.
def extractField(line, separatorPositions, index):
	return(line[extractBoundaries(line,separatorPositions,index)[0]:extractBoundaries(line,separatorPositions,index)[1]])

# Each entry of replaceList is a triple (start, end, newstring) whereby the character in string starting from the start-th up to the end-1-th are replaced by newstring. All the start-end pairs are assumed to be non-overlapping.
def simultaneousReplace(replaceList, string):
	for tuple in sorted(replaceList, key=lambda x: x[1], reverse=True):
		string=string[:tuple[0]]+tuple[2]+string[tuple[1]:]
	return string

freshDummy="dummy"; freshPrefix="asdrubale"; firstDeclarationIndex=3; assertionIndex=1;

def amendedLine(line):
	separatorIndices=filterPositions(lambda x: x==':', line); 
	numberOfFields=1+len(separatorIndices)
	if (numberOfFields < 2): return line; 
	formula=extractField(line, separatorIndices, assertionIndex)
	# Each entry of unknownsList is a list with the name of a ng var, an arbitrary fresh name which will substitute it in the formula, its order in the original variable list, the start, end positions of its declaration in the input line, and the proposed range (to be possibly amended by the solver).
	declarationsList=[];	assertionsList=[]; unknownsList=[]
	for i in range(firstDeclarationIndex, numberOfFields, 2):
		name=extractField(line, separatorIndices, i)
		value=eval(extractField(line, separatorIndices, i+1))
		if isinstance(value, tuple):
			minname=name+"_min"; maxname=name+"_max"; minvalue=value[0]; maxvalue=value[1]
			declarationsList.append(minname+"=Int('"+minname+"')")
			declarationsList.append(maxname+"=Int('"+maxname+"')")
			assertionsList.append(minname+" <= "+maxname)
			assertionsList.append(minname+" >= "+str(value[0]))
			assertionsList.append(maxname+" <= "+str(value[1]))
			# this will tell us which variable to evaluate in Z3, where to substitute the result in the input, and how to restrict the search for that variable's admissible values:
			unknownsList.append([name, i, ] + list(extractBoundaries(line,separatorIndices,i+1))+[minvalue, maxvalue])
		else:
			declarationsList.append(name+"=Int('"+name+"')")
			assertionsList.append(name+"=="+str(value))
			
	if unknownsList==[]: return line
	
	# To roughly represent what can occur in a C variable name:
	# CIdentifierCharset="[a-zA-Z0-9._\[\]]"; CSuffixCharset="[.]"; CVarnameCharset="a-zA-Z0-9._"
	
	# For each unknown var, we add an arbitrary (hopefully) fresh variable name:
	[unknownsList[i].insert(1,freshPrefix+'_'+str(i)) for i in range(len(unknownsList))]
	
	# This loop is to take care of issue (**) above:
	formulaSanitised=formula[:]
	for lst in unknownsList:
		# Suppose the non-ground variable name is "varname", possibly occurring in the formula with some ".suffix" (see (**)). We want to discard the occurrences where varname is a proper substring of some other variable name (e.g., "avarname" or "varnamea"). We also want to discard occurrences where "varname" is an index or similar, e.g. "array[varname]" or "record.varname", because these are parsed separately and correspond to values different than the non-ground one.
		# This regex saves all the occurrences of "varname" complying with the restrictions above:
		#
		occurrences=list(re.finditer(r'(^|[^a-zA-Z0-9_\.\[])(?P<focus>'+re.escape(lst[0])+'([\.\[][a-zA-Z0-9_\[\]]*)*)($|[^a-zA-Z0-9_\.\[])', formula))
		# Note re.escape is needed to handle cases where special regex chars occur in varname.
		numOfDistinctOccurrences=len(set([occurrence.group('focus') for occurrence in occurrences]))
		if numOfDistinctOccurrences == 0: return line; 
		if numOfDistinctOccurrences == 1: formulaSanitised=simultaneousReplace([(occurrence.start('focus'), occurrence.end('focus'), lst[1]) for occurrence in occurrences], formula)
		else: print('!! non-ground variable name occurring in more than one form'); exit()
	# Now we can add the important assertions:
	for lst in unknownsList:
		name=lst[0]; freshname=lst[1]; i=lst[2]; minvalue=lst[5]; maxvalue=lst[6]; minname=name+"_min"; maxname=name+"_max"; 
		assertionsList.append("ForAll("+freshDummy+", Implies(And("+freshDummy+">="+minname+", "+freshDummy+"<="+maxname+"), "+formulaSanitised.replace(freshname, freshDummy)+"))")
		assertionsList.append("Implies("+minname+" > "+str(minvalue)+", Not("+formulaSanitised.replace(freshname, "("+minname+" -1)")+"))")
		assertionsList.append("Implies("+maxname+" < "+str(maxvalue)+", Not("+formulaSanitised.replace(freshname, "("+maxname+" +1)")+"))")
	# print(line)
	# print(declarationsList)
	# print(assertionsList)
	# print(unknownsList)
	# print(formula, formulaSanitised)
	# The following variable is for quantifying only (dummy or indicator variable), and you should make sure its name's fresh:
	exec(freshDummy+"=Int('"+freshDummy+"')")
	for decl in declarationsList: exec(decl)
	s=Solver(); [s.add(eval(ass)) for ass in assertionsList]
	# s.add(Implies(x<=3, ForAll(y, y==10)))
	# s.add(False)
	satResult=str(s.check())
	if bool(re.search('sat', satResult)):
		if not(bool(re.search('unsat', satResult))):
			m=s.model()
			for lst in unknownsList:
				lower=eval("m.evaluate("+lst[0]+"_min)"); upper=eval("m.evaluate("+lst[0]+"_max)")
				line=line[:lst[3]]+"("+str(lower)+","+str(upper)+")"+line[lst[4]:]
		else: line=line[:lst[3]]+'"unsat"'+line[lst[4]:]
	else: line=line[:lst[3]]+'"unknown"'+line[lst[4]:]
	return line

for line in sys.stdin: print(amendedLine(line.rstrip())) 

exit()

# TODOS 11/9/2020: output should modify the input txt file as follows: substitute ngtime:(0,100) with the real range, eg ngtime:(46,98)
# in the relevant lines. If the real range is empty, substitute with ngtime:unsat. The lines without non-ground vars should be left unmodified. Note you cannot assume ngtime:(,) is the last entry of a line.
# Also, detail on the dependencies your stuff need and explain how to invoke it.
# Finally, keep in mind that 
# (**): the name of the non-ground variable occurs differently in the assertion and in the declaration: in the former, it has (may have?) a .mininimum (or .maximum) suffix. Deal with that sensibly.

