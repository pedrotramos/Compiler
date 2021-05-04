{
    a = 2;        /* Verifica se uma equação de segundo grau possui raízes */
    b = readln(); /* Só depende do input do termo b da esquação */
    c = 2;
    delta = (b * b) - (4 * a * c);
    if (delta == 0 || delta > 0)
    {
        println(1);
    }
    else
    {
        println(0);
    }

    i = 1;
    while (!(i > 4))
    {
        j = 4;
        while (j > 1 || j == 1)
        {
            println(i * j);
            j = j - 1;
        }
        i = i + 1;
    }
}