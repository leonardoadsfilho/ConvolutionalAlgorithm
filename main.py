import math
from tabulate import tabulate

def calculate_beta(service_rate, queue_discipline, num_clients):
    rho = 1 / service_rate

    if queue_discipline == "M/M/m":
        beta = (rho ** num_clients) / math.factorial(num_clients) if num_clients > 0 else 1
    else:
        beta = (1 - rho) * (rho ** num_clients) if num_clients > 0 else 1        

    return beta

def calculate_constant(n, m, num_clients_total, betas):
    
        constant_sum = 0

        if n == 0:
            constant_sum = 1
        elif m == 1:
            constant_sum = betas[m-1][num_clients_total]
        else:
            for k in range(n+1):
                constant_sum += betas[m-1][k] * calculate_constant(n - k, m - 1, num_clients_total, betas)
        
        return constant_sum

def calculate_queue_client_constant(num_clients_total, num_queues, betas):
    
    constants = []

    for i in range(num_clients_total+1):
        constant = [calculate_constant(i, q, num_clients_total, betas) for q in range(1, num_queues+1)]
        constants.append(constant)

    return constants


def calculate_sub_constant(m, n, N, normalization_constant, betas, constants):

    marginal_tax = 0

    if n == 0:
        marginal_tax = 1
    else:
        constant_sum = 0

        for k in range(N+1):
           const = constants[N-k][m-1]
           constant_sum += betas[m-1][k] * const

        marginal_tax = normalization_constant - constant_sum

    return marginal_tax

def calculate_gm_constants(m, n, constants, betas):

    gm = []

    for i in range(m):
        gmn = []
        for k in range(n+1):
            if k == 0:
                gmn.append(1)
            else:
                sum_gms = 0

                for j in range(1, k+1):
                    sum_gms += betas[i][j] * constants[j][i]

                gmn.append(constants[len(constants) - 1][len(constants[0]) - 1] - sum_gms)

        gm.append(gmn)

    return(gm)
        

def calculate_marginal_taxes(queues):
    num_queues = len(queues[0])  # Número de filas na rede

    # Extração das informações das filas
    service_rates = queues[0]  # Taxas de serviço
    queue_disciplines = queues[2]  # Disciplinas das filas
    num_clients_total = queues[3]  # Número máximo de clientes no sistema

    # Cálculo dos betas para cada fila e número de clientes
    betas = []

    for i in range(num_queues):
        betas_i = [calculate_beta(service_rates[i], queue_disciplines[i], n) for n in range(num_clients_total + 1)]
        betas.append(betas_i)

    # Impressão da tabela dos betas
    headers_betas = ["m=" + str(i+1) for i in range(num_queues)]
    beta_table = [["n=" + str(n)] + [betas[i][n] for i in range(num_queues)] for n in range(num_clients_total + 1)]

    print("\nTabela de Bm(n):")
    print(tabulate(beta_table, headers_betas, tablefmt="grid"))

    # Cálculo da constante de normalização para cada fila
    constants = calculate_queue_client_constant(num_clients_total, num_queues, betas)
    
    normalization_constant = constants[len(constants) - 1][len(constants[0]) - 1]

    # Impressão da tabela das constantes
    headers_constants = ["m=" + str(i+1) for i in range(len(constants))]
    constants_table = [["n=" + str(n)] + [constants[n][i] for i in range(len(constants[0]))] for n in range(len(constants))]

    print("\nTabela de constates G(N):")
    print(tabulate(constants_table, headers_constants, tablefmt="grid"))

    gm_constants = calculate_gm_constants(num_queues, num_clients_total, constants, betas)

    # Impressão da tabela das constantes
    headers_constants = ["m=" + str(i+1) for i in range(len(gm_constants))]
    constants_table = [["n=" + str(n)] + [gm_constants[i][n] for i in range(len(gm_constants))] for n in range(len(gm_constants[0]))]

    print("\nTabela das constantes Gm(N):")
    print(tabulate(constants_table, headers_constants, tablefmt="grid"))

    marginal_taxes = []

    for queue in range(num_queues):
        marginal_tax = []
        for k in range(num_clients_total+1):
            beta = betas[queue][k]
            beta_divide_global_constant = beta / normalization_constant
            # sub_constant = calculate_sub_constant(queue+1, k, num_clients_total, normalization_constant, betas, constants)
            sub_constant = gm_constants[queue][k]
            marginal_tax.append(beta_divide_global_constant * sub_constant)
            
        marginal_taxes.append(marginal_tax)

    # Impressão da tabela das taxas marginais
    headers = ["m=" + str(i+1) for i in range(num_queues)]
    beta_table = [["n=" + str(n)] + [marginal_taxes[i][n] for i in range(num_queues)] for n in range(num_clients_total + 1)]

    print("\nTabela de taxas marginais pi_m(n):")
    print(tabulate(beta_table, headers, tablefmt="grid"))

    return marginal_taxes


queues = [
    [  1.0,     1.0,     0.5,     1.0  ],  # Taxas de serviço
    [  1.0,     1.0,     1.0,     1.0  ],  # Taxas de chegada
    ["M/M/m", "M/M/m", "M/M/m", "M/M/m"],  # Disciplinas das filas
                     2                     # Número máximo de clientes no sistema
]

normalization_constants = calculate_marginal_taxes(queues)
