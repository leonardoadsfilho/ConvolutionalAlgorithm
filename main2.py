import math


def Beta(fila, numero_cliente_na_fila):
    P = 0
    ro = 1/fila.taxa_de_servico

    if numero_cliente_na_fila == 0:
        P = 1
    elif fila.disciplina == "M/M/1":
        P = (1-ro)*(ro**numero_cliente_na_fila)
    elif fila.disciplina == "M/M/m":
        P = (ro**numero_cliente_na_fila)/math.factorial(numero_cliente_na_fila)
    return P


def G(fila, numero_cliente_na_fila, quantidade_fila):
    if numero_cliente_na_fila == 0:
        return 1
    elif quantidade_fila == 1:
        return Beta(fila, numero_cliente_na_fila)
    else:
        somatorio = 0
        for i in range(numero_cliente_na_fila):
            somatorio += Beta(fila, i) * G(fila, numero_cliente_na_fila-i, quantidade_fila-1)

        return somatorio


def G2(fila, numero_cliente_na_fila, N, constate_de_normalziacao):
    if (N-numero_cliente_na_fila) == 0:
        return 1
    else:
        result = 0
        for i in range(1,N):
            result += constate_de_normalziacao - Beta(fila,numero_cliente_na_fila)*G2(fila,numero_cliente_na_fila, N-i,constate_de_normalziacao)
        return constate_de_normalziacao - result

# Mi, m, n, disciplinaFila
# taxa = [()] => (a fila, quantidade cliente, resultado)


def F(filas, n):
    taxa = []
    m = len(filas)
    for i in range(m):  # A Fila
        for j in range(n, 0, -1):  # Numero de clientes na fila
            constate_de_normalziacao = G(i, j, m)
            result = (Beta(i, j)/constate_de_normalziacao)*G2(i, j,n,constate_de_normalziacao)
            taxa.append(i, j, result)
    return taxa
