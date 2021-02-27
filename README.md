# Compilador

### Funcionamento do compilador:

Esse compilador funciona somente para argumentos de entrada que buscam calcular operações matemáticas de soma e subtração. O programa deve ser executado da seguinte forma:

~~~
python main.py -e=" 1    -1+2"
~~~

Assim o programa exibirá na tela como saída o resultado da equação, que no exemplo anterior é 2.

Caso na string de entrada haja caractéres que não sejam números, sinais de soma e subtração ou espaços o programa não exibirá um resultado como saída. Nesse caso, o que será exibido é um aviso de que o programa falhou e tentará encaminhar o usuário para a resolução do problema.

Vale destacar que não é permitido que o primeiro caractere não pode ser um sinal. Ou seja, entradas como as dos exemplos abaixo não devem funcionar.

~~~
python main.py -e="-1+2"
python main.py -e="+4 + 10"
~~~
