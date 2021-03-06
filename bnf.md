# Syntax of SM based on SML97

This is the BNF syntax of SM Language, for the Compiler Design course, based 
on SML97 standard, contain only a subset and modified a little.

The first edition is called chrysanthemum.

## Reserved Words

1. and
2. andalso
3. as
4. case
5. datatype
6. do
7. else
8. end
9. fn
10. fun
11. if
12. in
13. infix
14. infixr *
15. let
16. local *
17. nonfix *
18. of
19. op
20. open *
21. orelse *
22. rec
23. then
24. type
25. val
26. with *
27. withtype *
28. while
29. ( ) [ ] { } , : ; `...` _ | = => -> #
30. use

## Literal Constant

1. Integer
	1. optional negation symbol (~)
	2. 0...9 sequence
	3. hexadecimal notation start with 0x, 0..9, a..f, A..F
	4. RE: INT = ~?(\d+)|(0x[0-9a-fA-F]+)
2. Real
	1. A **Integer** in **decimal notation**, possibly followed by a point (.) .
	2. Followed by `E` or `e`.
	3. RE: REAL = ~?\d+(\.\d+)?([eE]~?\d+)
3. String
	1. between quotes (") , 0 or more printable characters, spaces or escape sequences.
	2. escape sequence with form `\ddd`, three digital.
4. Char
	1. `#"x"`

## Comments

A comment is any character sequence within comment brackets (\* \*) in which comment brackets are properly nested. No space is allowed between the two characters which make up a comment bracket (* or \*). An unmatched (\* should be detected by the compiler.

	COMMENT_START = "(*"
	COMMENT_END = "*)"
	COMMENT -> COMMENT_START ANY_STRING COMMENT_END

## Identifier

There are syntactically two kinds of identifiers:

**Alphanumeric**: starts with a letter or prime (') and is followed by letters, digits, primes and underbars (_). 

Examples: abc, ABC123, Abc_123, 'a.


**Symbolic**: a sequence of the following

 	! % & $ # + - / : < = > ? @ \ ~ ` ^ | *
	
Examples: +=, <=, >>, $.

There are a number of different classes of identifiers, some of which have additional syntactic rules.

- Identifiers not starting with a prime.
value identifier (includes variables and constructors)
	- **type constructor**
	- **functor identifier**
- Identifiers starting with a prime.
	- **type variable**
- Identifiers not starting with a prime and numeric labels (1, 2, …).
	- **record label**

Four types should be defined seperately.

## Lexical analysis

Each item of lexical analysis is either a reserved word, a numeric label, a special constant or a long identifier. Comments and formatting characters separate items (except within string constants) and are otherwise ignored. At each stage the longest next item is taken.

## Grammer

### type construction

```
- type ('a, 'b) kk = 'a * 'a * 'b;
type ('a,'b) kk = 'a * 'a * 'b
- val a : (int, int)kk = (1,1,1);
val a = (1,1,1) : (int,int) kk
- val b : (int, real) kk = (1,1,1.2);
val b = (1,1,1.2) : (int,real) kk
```

### type scope

[This Link](http://mlton.org/TypeVariableScope) described the what type variables means.

### type variables bound

To understand this concept, read the following snippets carefully.

```
fun f (x,y,a,b,c) =
    let
        fun 'a pair (x : 'a, y : 'a) = (x, y)
        fun 'a triple (x : 'a, y : 'a, z : 'a) = (x, y, z)
    in
        (pair(x, y), triple(a, b, c))
    end
val f = fn : 'a * 'a * 'b * 'b * 'b -> ('a * 'a) * ('b * 'b * 'b)

fun 'a f (x,y,a,b,c) =
    let
        fun pair (x : 'a, y : 'a) = (x, y)
        fun triple (x : 'a, y : 'a, z : 'a) = (x, y, z)
    in
        (pair(x, y), triple(a, b, c))
    end
val f = fn : 'a * 'a * 'a * 'a * 'a -> ('a * 'a) * ('a * 'a * 'a)

fun f (x,y,a,b,c) =
    let
        fun pair (x, y) = (x, y)
        fun triple (x, y, z) = (x, y, z)
    in
        (pair(x, y), triple(a, b, c))
    end
val f = fn : 'a * 'b * 'c * 'd * 'e -> ('a * 'b) * ('c * 'd * 'e)
```

Along with the answer from [this queston](http://stackoverflow.com/questions/30710680/what-type-variables-means-when-they-occurred-in-val-declaration-statement-in?answertab=active#tab-top) and section 1.1.3 in [this page](http://www.smlnj.org/doc/Conversion/types.html).

## Reference

[_The Definition of Standard ML, revised_](sml-family.org/sml97-defn.pdf) by Robin Milner, Mads Tofte, Robert Harper and David MacQueen  
[Standard ML Grammar](https://www.mpi-sws.org/~rossberg/sml.html) by Andreas Rossberg
