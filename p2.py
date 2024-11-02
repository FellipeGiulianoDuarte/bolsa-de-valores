import datetime

estado = {'hoje': datetime.date.today(), 'cliente_id': 1, 'carteira_id': 1}
clientes = {}
carteiras = {}
mercado = {}
ordens = []

def cria_cliente(nif, nome, data_nasc):
    """
    Cria um novo cliente com os detalhes fornecidos e o adiciona ao dicionário de clientes.

    Args:
    - nif (str): Número de identificação fiscal do cliente.
    - nome (str): Nome do cliente.
    - data_nasc (str): Data de nascimento do cliente no formato 'AAAA-MM-DD'.

    Returns:
    - int: Identificador do cliente criado.
    """
    global estado, clientes
    cliente_id = estado['cliente_id']
    clientes[cliente_id] = {'nif': nif, 'nome': nome, 'data_nasc': data_nasc, 'saldo': 0.0, 'carteiras_id': []}
    estado['cliente_id'] += 1
    return cliente_id


def encerra_cliente(cliente_id):
    """
    Encerra o cliente com o identificador fornecido, liquidando todas as suas carteiras individuais, se houver.

    Args:
    - cliente_id (int): Identificador do cliente a ser encerrado.

    Returns:
    - int: Valor a ser entregue ao cliente, a soma do saldo atual da conta após o encerramento de todas as suas carteiras.
    """
    global clientes, carteiras

    # Verifica se o cliente existe
    if cliente_id not in clientes:
        return 0  # Nenhum cliente com esse ID, retorno 0

    # Verifica se o cliente tem carteiras partilhadas
    carteiras_cliente = clientes[cliente_id]['carteiras_id']
    for carteira_id in carteiras_cliente:
        titulares = carteiras[carteira_id]['titulares_id']
        if isinstance(titulares, int):
            titulares = (titulares,)
        if len(titulares) > 1:
            raise ValueError('cliente tem carteiras partilhadas')

    # Encerra as carteiras individuais do cliente
    total_saldo = clientes[cliente_id]['saldo']
    for carteira_id in carteiras_cliente:
        total_saldo += encerra_carteira(carteira_id)
        del carteiras[carteira_id]

    # Remove o cliente
    del clientes[cliente_id]

    return total_saldo


def posicao_cliente(cliente_id):
    """
    Retorna o valor total do cliente, incluindo o saldo atual e o valor atual de todas as ações das carteiras que o cliente possui.

    Args:
    - cliente_id (int): Identificador do cliente.

    Returns:
    - float: O valor correspondente à soma do saldo do cliente com o valor atual de todas as ações das carteiras que o cliente possui.
    """
    global clientes, carteiras, mercado
    if cliente_id not in clientes:
        return 0
    total_saldo = clientes[cliente_id]['saldo']
    for carteira_id in clientes[cliente_id]['carteiras_id']:
        carteira = carteiras[carteira_id]
        if isinstance(carteira['titulares_id'], tuple):
            n = len(carteira['titulares_id']) + 1
        else:
            n = 1
        for titulo in carteira['titulos']:
            total_saldo += mercado[titulo[0]][1] * titulo[1] / n
    return total_saldo


def movimenta_saldo(cliente_id, valor):
    """
    Movimenta o saldo do cliente.

    Args:
    - cliente_id (int): Identificador do cliente.
    - valor (float): Valor a movimentar.

    Returns:
    - float: O valor movimentado, que pode ser negativo se o saldo for insuficiente ou zero se o valor for negativo.
    """
    global clientes
    if cliente_id not in clientes:
        return 0
    if valor < 0 and clientes[cliente_id]['saldo'] < abs(valor):
        valor = -clientes[cliente_id]['saldo']
        clientes[cliente_id]['saldo'] = 0.0
        return valor
    else:
        clientes[cliente_id]['saldo'] += valor
        return valor if valor >= 0 else 0

def abre_carteira(titulares_id, designacao):
    """
    Abre uma nova carteira de títulos.

    Args:
    - titulares_id (int or tuple): Identificador(es) do(s) cliente(s) titular(es) da carteira. Se houver mais de um titular, deve ser fornecido como um tuple.
    - designacao (str): Designação da carteira.

    Returns:
    - int: O identificador da carteira aberta.
    """
    if titulares_id is None:
        raise ValueError("titulares_id não pode ser None")
    global estado, carteiras
    carteira_id = estado['carteira_id']
    carteiras[carteira_id] = {'titulares_id': titulares_id, 'designacao': designacao, 'data_abertura': estado['hoje'], 'titulos': [], 'operacoes': []}
    if isinstance(titulares_id, int):
        clientes[titulares_id]['carteiras_id'].append(carteira_id)
    elif isinstance(titulares_id, tuple):
        for titular_id in titulares_id:
            clientes[titular_id]['carteiras_id'].append(carteira_id)
    regista_operacao(carteira_id, 'ABERTURA')
    estado['carteira_id'] += 1
    return carteira_id


def encerra_carteira(carteira_id):
    """
    Encerra uma carteira de títulos.

    Args:
    - carteira_id (int): Identificador da carteira a ser encerrada.

    Returns:
    - float: O valor total obtido com a venda dos títulos.
    """
    global carteiras, clientes, mercado
    if carteira_id not in carteiras:
        raise ValueError('carteira inexistente')
    total_valor = 0
    for titulo in carteiras[carteira_id]['titulos']:
        total_valor += titulo[1] * mercado[titulo[0]][1]
    titular_ids = carteiras[carteira_id]['titulares_id']
    if isinstance(titular_ids, list):
        for titular_id in titular_ids:
            clientes[titular_id]['saldo'] += total_valor / len(titular_ids)
            clientes[titular_id]['carteiras_id'].remove(carteira_id)
    else:
        clientes[titular_ids]['saldo'] += total_valor
        clientes[titular_ids]['carteiras_id'].remove(carteira_id)
    regista_operacao(carteira_id, 'FECHO')
    return total_valor



def regista_operacao(carteira_id, descricao, nome_titulo=None, quantidade=None, valor=None):
    """
    Regista uma operação na carteira de títulos.

    Args:
    - carteira_id (int): Identificador da carteira.
    - descricao (str): Descrição da operação.
    - nome_titulo (str): Nome do título transacionado.
    - quantidade (int): Número de unidades do título transacionadas.
    - valor (float): Valor total da operação.

    Returns:
    - None
    """
    global carteiras, estado
    operacao = (estado['hoje'], descricao, nome_titulo, quantidade, valor)
    carteiras[carteira_id]['operacoes'].append(operacao)


def processa_operacao(carteira_id, operacao, nome_titulo, quantidade):
    """
    Regista uma operação na carteira de títulos.

    Args:
    - carteira_id (int): Identificador da carteira.
    - descricao (str): Descrição da operação.
    - nome_titulo (str): Nome do título transacionado.
    - quantidade (int): Número de unidades do título transacionadas.
    - valor (float): Valor total da operação.

    Returns:
    - None
    """
    global carteiras, mercado, clientes
    valor_total = 0

    if operacao == 'COMPRA':
        valor_unidade = mercado[nome_titulo]['preco']
        valor_total = valor_unidade * quantidade

        if isinstance(carteiras[carteira_id]['titulares_id'], int):
            cliente_ids = [carteiras[carteira_id]['titulares_id']]
        else:
            cliente_ids = list(carteiras[carteira_id]['titulares_id'])

        if not all(clientes[cliente_id]['saldo'] >= valor_total / len(cliente_ids) for cliente_id in cliente_ids):
            raise ValueError('fundos insuficientes')

        for cliente_id in cliente_ids:
            clientes[cliente_id]['saldo'] -= valor_total / len(cliente_ids)

        regista_operacao(carteira_id, operacao, nome_titulo, quantidade, valor_total)

    elif operacao == 'VENDA':
        for titulo in carteiras[carteira_id]['titulos']:
            if titulo[0] == nome_titulo:
                if titulo[1] < quantidade:
                    quantidade = titulo[1]
                valor_total = mercado[nome_titulo][1] * quantidade

                if isinstance(carteiras[carteira_id]['titulares_id'], int):
                    cliente_ids = [carteiras[carteira_id]['titulares_id']]
                else:
                    cliente_ids = list(carteiras[carteira_id]['titulares_id'])

                for cliente_id in cliente_ids:
                    clientes[cliente_id]['saldo'] += valor_total / len(cliente_ids)

                regista_operacao(carteira_id, operacao, nome_titulo, quantidade, valor_total)
                return valor_total

        raise ValueError('titulo inexistente em carteira')

    return valor_total


def agenda_ordem(carteira_id, operacao, nome_titulo, quantidade, preco_limite, data_str):
    """
    Permite agendar uma ordem para uma operação a ser realizada na data atual ou numa data futura.

    Args:
    - carteira_id (int): Identificador da carteira sobre a qual deverá ser realizada a operação.
    - operacao (str): Operação a realizar. Pode ser 'COMPRA' ou 'VENDA'.
    - nome_titulo (str): Nome do título a ser transacionado.
    - quantidade (int): Número de unidades do título a serem transacionadas.
    - preco_limite (float): Preço limite para a operação.
    - data_str (str): Data em que a operação deverá ser realizada, no formato 'AAAA-MM-DD'.

    Returns:
    - bool: Valor booleano que indica se a operação pode ou não ser realizada ou a ordem agendada.
    """
    global estado, ordens
    if not data_str or data_str == estado['hoje']:
        try:
            processa_operacao(carteira_id, operacao, nome_titulo, quantidade)
        except ValueError:
            return False
        return True
    if data_str < str(estado['hoje']):
        return False
    ordens.append((carteira_id, operacao, nome_titulo, quantidade, preco_limite, data_str))
    return True


def gera_resumo(carteira_id, data_inicio_str="", data_fim_str=""):
    """
    Gera um resumo da carteira especificada, com as informações correspondentes.

    Args:
    - carteira_id (int): Identificador da carteira para a qual deve ser gerado o resumo.
    - data_inicio_str (str): Data de início das operações a incluir no resumo, no formato 'AAAA-MM-DD'.
    - data_fim_str (str): Data de fim das operações a incluir no resumo, no formato 'AAAA-MM-DD'.

    Returns:
    - list: Lista contendo o resumo da carteira, com os elementos de informação conforme especificado.
    """
    global carteiras, estado
    resumo = []
    if not data_inicio_str:
        data_inicio_str = carteiras[carteira_id]['data_abertura']
    if not data_fim_str:
        data_fim_str = estado['hoje']
    resumo.append(carteira_id)
    resumo.append(carteiras[carteira_id]['designacao'])
    resumo.append(estado['hoje'])
    titulos_info = [(mercado[titulo[0]][0], titulo[0], titulo[1], mercado[titulo[0]][1] * titulo[1]) for titulo in carteiras[carteira_id]['titulos']]
    resumo.append(titulos_info)
    valor_total = sum(info[3] for info in titulos_info)
    resumo.append(valor_total)
    operacoes_info = [(op[0], op[1], op[2], op[3], op[4]) for op in carteiras[carteira_id]['operacoes'] if data_inicio_str <= op[0] <= data_fim_str]
    resumo.append(operacoes_info)
    return resumo


def imprime_resumo(resumo):
    """
    Imprime as informações contidas em um resumo de uma carteira de títulos.

    Args:
    - resumo (list): Lista correspondente ao resumo de uma carteira de títulos, gerada pela função gera_resumo.

    Returns:
    - None
    """
    print("-" * 50)
    print(f"CARTEIRA #{str(resumo[0]).zfill(6)} / {resumo[1]} {resumo[2]}")
    print("-" * 50)
    print(" " * 18 + "** TITULOS **")
    print("-" * 50)
    for titulo in resumo[3]:
        print(f"{titulo[0]:<20}{titulo[1]:<5}{titulo[2]:>9}{titulo[3]:>12.2f}")
    print("-" * 50)
    print(f"TOTAL{'':32}{resumo[4]:>12.2f}")
    print("-" * 50)
    print(" " * 17 + "** OPERACOES **")
    print("-" * 50)
    for operacao in resumo[5]:
        if all(operacao):
            print(f"{operacao[0]} {operacao[1]:<8}  {operacao[2]:<5}{operacao[3]:>9}{operacao[4]:>12.2f}")
    print("-" * 50)


def carrega_mercado(nome_ficheiro):
    """
    Processa um ficheiro contendo informações de todos os títulos disponíveis para serem negociados e respetivas cotações.

    Args:
    - nome_ficheiro (str): Nome do ficheiro a ser processado.

    Raises:
    - ValueError: Se houver um erro ao abrir o ficheiro.

    Returns:
    - None
    """
    try:
        with open(nome_ficheiro, 'r') as file:
            mercado.clear()
            for line in file:
                # parts = line.strip().split('\t')
                parts = [x for x in line.strip().split('\t') if x]
                if len(parts) == 3:
                    mercado[parts[1]] = {'designacao': parts[0], 'preco': float(parts[2])}
    except IOError:
        raise ValueError('erro a abrir o ficheiro')


def carrega_ordens(nome_ficheiro):
    """
    Processa um ficheiro contendo um conjunto de ordens.

    Args:
    - nome_ficheiro (str): Nome do ficheiro a ser processado.

    Raises:
    - ValueError: Se houver um erro ao abrir o ficheiro.

    Returns:
    - None
    """
    try:
        with open(nome_ficheiro, 'r') as file:
            for line in file:
                parts = line.strip().split('\t')
                if len(parts) == 5:
                    carteira_id = int(parts[0])
                    operacao = 'COMPRA' if int(parts[2]) > 0 else 'VENDA'
                    nome_titulo = parts[1]
                    quantidade = abs(int(parts[2]))
                    preco_limite = float(parts[3])
                    data_str = parts[4]
                    agenda_ordem(carteira_id, operacao, nome_titulo, quantidade, preco_limite, data_str)
    except IOError:
        raise ValueError('erro a abrir o ficheiro')


def inicia_dia(data_str=""):
    """
    Atualiza a data atual e processa as operações agendadas para o dia.

    Args:
    - data_str (str): Nova data atual no formato 'AAAA-MM-DD'.

    Returns:
    - None
    """
    global estado
    if data_str:
        estado['hoje'] = datetime.date.fromisoformat(data_str)
    else:
        estado['hoje'] = estado['hoje'] + datetime.timedelta(days=1)

    for ordem in ordens[:]:
        if ordem[5] == str(estado['hoje']):
            try:
                processa_operacao(ordem[0], ordem[1], ordem[2], ordem[3])
                ordens.remove(ordem)
            except ValueError:
                ordens.remove(ordem)
                continue
