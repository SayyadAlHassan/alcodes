### aldeobfus.py (IPA: /ʌldɔbfəs/)

Often malware scripts deobfuscate code by splitting the data into characters or integers and calling decryption routine repeatedly on each unit.
It can work for a wide variety of custom decryption functions and replace the obfuscated function calls with the output.
Attached images compare an obfuscated payload of a deobfuscated vbsworm with its deobfuscated values. Although the decryption routine in was very basic, the script can work on more complex decryptions too. 

Here's an example
~~~
Eg: If Am=""THen If LcAsE(MiD(WsCriPt.ScRipTfUlLnAmE,2))=X(58)&X(92)&LcAsE(Ar)THen Am=X(84)&X(82)&X(117)&X(101)&X(32)&X(45)&X(32)&dat
~~~
Parameters:
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
#	   you can provide those characters here in a string. In this example, it is space and & symbol so we can give "& " on windows cmdline it will be "^& "

