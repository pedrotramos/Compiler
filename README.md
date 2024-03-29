# Compilador

## Status dos testes

![git_status](http://3.129.230.99/svg/pedrotramos/Compiler/)

### Funcionamento do compilador:

Esse compilador funciona somente para argumentos de entrada que buscam calcular operações aritiméticas, booleanas e relativas, atribuições a variáveis e comandos de *println*, *readln*, *while* e *if-else*. O programa deve ser executado da seguinte forma:

~~~
python main.py "arquivo.c"
~~~

Sendo ```arquivo.c``` o arquivo que contém a equação a ser resolvida. Assim, o programa exibirá na tela como saída a resolução do programa ```arquivo.c```.

### Diagrama Sintático:

<img src="Assets/DiagramaSintatico.png"/>

### Notação EBNF:

<img src="Assets/EBNF.png"/>

### EBNF Atual:

~~~
BLOCK = "{", { COMMAND }, "}" ;
COMMAND = ((λ | ASSIGNMENT | DECLARATION | PRINT), ";" | LOOP | IF-ELSE) ;
LOOP = "while", "(", OR_EXPRESSION, ")", BLOCK ;
IF-ELSE = "if", "(", OR_EXPRESSION, ")", BLOCK, ["else", BLOCK] ;
DECLARATION = TYPE, IDENTIFIER, ["=", (OR_EXPRESSION | READ)] ;
ASSIGNMENT = IDENTIFIER, "=", (OR_EXPRESSION | READ) ;
READ = "readln", "(", ")" ;
PRINT = "println", "(", OR_EXPRESSION, ")" ;
OR_EXPRESSION = AND_EXPRESSION, { "||", AND_EXPRESSION } ;
AND_EXPRESSION = EQ_EXPRESSION, { "&&", EQ_EXPRESSION } ;
EQ_EXPRESSION = REL_EXPRESSION, { "==", REL_EXPRESSION } ;
REL_EXPRESSION = EXPRESSION, { (">" | "<"), EXPRESSION } ;
EXPRESSION = TERM, { ("+" | "-"), TERM } ;
TERM = FACTOR, { ("*" | "/"), FACTOR } ;
FACTOR = ((("+" | "-"), FACTOR) | NUMBER | "(", EXPRESSION, ")" | IDENTIFIER | STRING);
IDENTIFIER = LETTER, { LETTER | DIGIT | "_" } ;
NUMBER = DIGIT, { DIGIT } ;
LETTER = ( a | ... | z | A | ... | Z ) ;
STRING = """, LETTER, { LETTER }, """ ;
DIGIT = ( 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 0 ) ;
~~~