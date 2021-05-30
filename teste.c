int fib(int n)
{
    if (n > 1)
        return fib(n - 1) + fib(n - 2);

    return n;
}

int retornaUm()
{
    return 1;
}

int main()
{
    bool x;
    x = true;
    if (x)
    {
        println(x);
    }
    x = retornaUm();
    println(x);
    int y;
    y = retornaUm();
    println(y);
    y = 0;
    while (y < 10)
    {
        println(fib(y));
        y = y + 1;
    }
}