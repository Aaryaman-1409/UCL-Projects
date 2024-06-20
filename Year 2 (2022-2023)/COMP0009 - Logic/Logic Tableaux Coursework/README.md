A python program to determine syntactic correctness and semantic satisfiability of first order and propositional formulae

## Usage: 
Run `python skeleton.py [optional_input_file]`

The first line of the input file should have either PARSE or SAT or both to determine parse correctness or satisfiability respectively

## Example format of optional_input_file:
```
PARSE SAT
Ax(P(x,x)^-P(x,x))
(Ax(P(x,x)^-P(x,x))^ExQ(x,x))
(ExP(x,x)^Ax(-P(x,x)>P(x,x)))
-EyEzAz(((P(x,x)>Q(y,y))^(Q(z,z)>P(z,z)))>AxEy(P(x,x)>Q(y,y)))
```