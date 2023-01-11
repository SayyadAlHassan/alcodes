#generic deobfuscation for
# x(numbers)+x(numbers)...
#CreAteOvjJect(X(119)&X( 99+ 1)& X(112 )&X(108)).&CreAteOvjJect(X(119)&X(99)&X(112)&X(108))hello  X(109)
#	CreAteOvjJect(X(119)&X( 99+ 1)& X(112 )&X(99)&X(112)&X(108))hello  X(109)

#inputs:
#function name: The name of the function. In the example above it's X
#Parameters regex: a regex that should be able to capture the paramaters between '(' and ')'
#				 usually [\d]+ is enough. but in the example above some parameter have '+' and ' ' so here it is '[\d \+]']
#deobfuscateLogic: a decryption logic, usually the decryption function.
#			 In the example it is simply chr(int({}))
#codefile: path of the file that contains the deobfuscated code
#delimiters: usually strings are deobfuscated so that characters needs to be decoded one by one and concatenated, in such cases you might want to
#	   add " as delimiters. This will enclose all the contigous occurances of function calls within the delimiters after concatenating the ret vals.
#concatChars: when each character of a string is obfuscated with one function call there are letters like "+" or "&" between two function calls for concatenation
#	   you can provide those characters here in a string. In this example, it is space and & symbol so we can give "& "

import re
import argparse


def params():
	sampleinput = {
	'syntax' : """python3 deob.py -n X -p "[\d \+]+" -l "chr(int({0}))" -f ./dummy.vbsa.py -d '"' -c " &" """,
	'inputfiletext': """CreAteOvjJect(X(119)&X( 99+ 1)& X(112 )&X(108)).&CreAteOvjJect(X(119)&X(99)&X(112)&X(108))hello  X(109)  eh
	CreAteOvjJect(X(119)&X( 99+ 1)& X(112 )&X(99)&X(112)&X(108))hello  X(109)  eh
	huhaa""",
	'sampleOutput': """Createovjject("wdpl" ).&createovjject("wcpl" )hello  "m" eh
	Createovjject("wdpcpl" )hello  "m" eh
	Huhaa"""
	}

	parser = argparse.ArgumentParser('Deobfuscate scripts by replacing all function calls with their values.')
	parser.add_argument('--funcName',  '-n', type=str, help="Name of the deobfuscation function" )
	parser.add_argument('--ParametersRegex', '-p', type=str, help="regex to parse parameters")
	parser.add_argument('--deobfusLogic', '-l', type=str, help="Deobfuscation logic")
	parser.add_argument('--codefile', '-f', type=str, help="obfuscated code file")
	parser.add_argument('--delimiters', '-d', type=str, default="", help='delimiter you might want to put before and after a series of function calls. -d "\"" ')
	parser.add_argument('--concatChars', '-c', type=str, default="", help='set of concatenation chars between two function calls\n X(1)&X(2)+X(3) then -c "^&" Note:^ is used as escape char in windows cmdline' )
	parser.add_argument('--outfile', '-o', type=str, default="out.txt", help="outfile" )
	parser.add_argument("--changeCase", "-s", type=bool, default=False, help ="Change the case to small case")
	return parser.parse_args()


def evalcustom(iDeobfusLogic, Parameter_, delim=""):
	tmpDLogic = iDeobfusLogic
	toEval = tmpDLogic.format(Parameter_)
	dobSz = delim + str( eval (toEval)) + delim
	return dobSz


def replacecalls(iFunctionName, iParamRegex, iDeobfusLogic, iObfusCode, delim = "", concatChars = "", Changecase=False):
	f = ""
	for line in iObfusCode.split("\n"):
		sline = line
		if len(concatChars) >0:
			szOneCall = "({fn}\({pr}\)[{cc}]*)".format(cc=concatChars, fn=iFunctionName, pr=iParamRegex)
			szAllCalls = "({fc1}+[{cc}]*?)".format(cc=concatChars, fc1 = szOneCall)

			comre = re.compile(szAllCalls)
			multipleCalls = comre.findall(line)
			for multipleCall, tmp in multipleCalls:
				szTmpReg = r"({fName}\(({ParamReg})\))".format(fName=iFunctionName,ParamReg= iParamRegex)
				dobCalls = re.findall(szTmpReg, multipleCall)

				repSz = delim
				for dobCall in dobCalls:
					dobOut = evalcustom(iDeobfusLogic, dobCall[1], delim="")
					repSz += dobOut
				repSz += delim + " "
				sline = sline.replace(multipleCall.strip(concatChars), repSz, 1)
		else:
			szTmpReg = r"({fName}\(({ParamReg})\))".format(fName=iFunctionName,ParamReg= iParamRegex)
			dobCalls = re.findall(szTmpReg, line)

			for dobCall in dobCalls:
				dobSz = evalcustom(iDeobfusLogic, dobCall[1], delim )
				sline = sline.replace(dobCall[0], dobSz, 1)

		tmpsline = sline
		if Changecase:
			tmpsline = sline.casefold()
		print(tmpsline)
		f+= tmpsline
		f+= "\n"
	return f


def main():
	ins = params()
	print(ins)

	with open(ins.codefile) as inf:
		ofl = replacecalls(ins.funcName, ins.ParametersRegex, ins.deobfusLogic, inf.read(), ins.delimiters, ins.concatChars, ins.changeCase)

	with open(ins.outfile, "w")as otf:
		otf.write(ofl)
	return


if __name__ == "__main__":
	main()
