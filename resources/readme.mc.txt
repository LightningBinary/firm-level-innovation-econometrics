Michele Cincera, "Patents, R&D and Spillovers at the Firm Level: Some
Evidence from Econometric Count Models for Panel Data", Journal of
Applied Econometrics, Vol. 12, No. 3, 1997, pp. 265-280.

The ASCII file data.mc, which is in DOS format, consists of a 181 firms x
30 variables matrix. It is zipped in mc-data.zip. The variables are
organized as columns. They are ordered as follows: 

 ___________________________________________________________________________________
|VARIABLE|DEFINITION				       |SOURCE			    |
|________|_____________________________________________|____________________________|
|var.#1: |fi=firm's identifier 			       |			    |
|var.#2: |s=firm's main industry sector (s=1,...,15)   |Dun & Bradstreet Int.	    |	
|var.#3: |g=firm's geographical area (g=1,...,4)       |		"	    |
|var.#4: |p83=# of European patent applications in 1983|European Patent Office	    |
| :      |					       |	"		    |
|var.#12:|p91=# of European patent applications in 1991| 	"		    |
|var.#13:|lr83=log of R&D expenditures in 1983	       |Compustat, Standard & Poor's| 
| :	 |					       |	"		    |
|var.#21:|lr91=log of R&D expenditures in 1991	       |	"		    |
|var.#22:|ls83=log of spillovers in 1983               |Anberd, OECD		    |
| :	 |					       |	"		    |
|var.#30:|ls91=log of spillovers in 1991	       |	"		    |
|________|_____________________________________________|____________________________|

Notes:
1. Industry sectors:
s=1: Aerospace
s=2: Chemistry
s=3: Computers	
s=4: Drugs	
s=5: Electricity	
s=6: Food	
s=7: Fuel and Mining	
s=8: Glass	
s=9: Instruments	
s=10: Machinery
s=11: Metals	
s=12: Other
s=13: Paper
s=14: Software
s=15: Motor Vehicles

2. Geographic areas:
g=1: European Union
g=2: Japan
g=3: U.S.
g=4: Rest of the World

3. var.#13-var.#30: millions of 1990 U.S. $ deflated by national GDP price
indices. 

4. The construction of the variables is discussed in section 3 of the
paper. 

