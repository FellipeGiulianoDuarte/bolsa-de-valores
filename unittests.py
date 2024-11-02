import unittest

from p2 import *

class TestFunctions(unittest.TestCase):
    def setUp(self):
        carrega_mercado('mercado.txt')

    def test_cria_cliente(self):
        # Teste para a função cria_cliente
        print("-" * 50)
        print('\nteste de criacao de cliente\n')
        cliente_id = cria_cliente('123456789', 'John Doe', '1990-01-01')
        print('cliente id: %s' % cliente_id)
        print('clientes: %s\nmercado: %s\ncarteiras: %s\n' % (clientes, mercado, carteiras))
        self.assertIn(cliente_id, clientes)

    def test_encerra_cliente(self):
        # Teste para a função encerra_cliente
        print("-" * 50)
        print('\nteste de encerramento de cliente\n')
        cliente_id = cria_cliente('123456789', 'John Doe', '1990-01-01')
        print('cliente id: %s' % cliente_id)
        valor_total = encerra_cliente(cliente_id)
        print('valor total: %s' % valor_total)
        print('clientes: %s\nmercado: %s\ncarteiras: %s\n' % (clientes, mercado, carteiras))
        self.assertEqual(valor_total, 0)

    def test_posicao_cliente(self):
        # Teste para a função posicao_cliente
        print("-" * 50)
        print('\nteste de posicao de cliente\n')
        cliente_id = cria_cliente('123456789', 'John Doe', '1990-01-01')
        print('cliente id: %s' % cliente_id)
        posicao = posicao_cliente(cliente_id)
        print('posicao: %s' % posicao)
        print('clientes: %s\nmercado: %s\ncarteiras: %s\n' % (clientes, mercado, carteiras))
        self.assertEqual(posicao, 0.0)
        carteira_id = abre_carteira(cliente_id, "Carteira Teste")
        print('carteira id: %s' % carteira_id)
        nome_titulo = "CUR"
        quantidade = 10
        movimenta_saldo(cliente_id, 100)
        processa_operacao(carteira_id, 'COMPRA', nome_titulo, quantidade)
        posicao_atualizada = posicao_cliente(cliente_id)
        print('posicao atualizada: %s' % posicao_atualizada)
        print('clientes: %s\nmercado: %s\ncarteiras: %s\n' % (clientes, mercado, carteiras))
        self.assertNotEqual(posicao, posicao_atualizada)

    def test_abre_carteira(self):
        # Teste para a função abre_carteira
        print("-" * 50)
        print('\nteste abre a carteira\n')
        cliente_id = cria_cliente('123456789', 'John Doe', '1990-01-01')
        print('cliente id: %s' % cliente_id)
        carteira_id = abre_carteira(cliente_id, "Carteira 1")
        print('carteira id: %s' % carteira_id)
        print('clientes: %s\nmercado: %s\ncarteiras: %s\n' % (clientes, mercado, carteiras))
        self.assertIn(carteira_id, carteiras)

    def test_encerra_carteira(self):
        # Teste para a função encerra_carteira
        print("-" * 50)
        print('\nteste para criacao de carteira\n')
        cliente_id = cria_cliente('123456789', 'John Doe', '1990-01-01')
        print('cliente id: %s' % cliente_id)
        carteira_id = abre_carteira(cliente_id, "Carteira 1")
        print('carteira id: %s' % carteira_id)
        valor_total = encerra_carteira(carteira_id)
        print('valor total: %s' % valor_total)
        print('clientes: %s\nmercado: %s\ncarteiras: %s\n' % (clientes, mercado, carteiras))
        self.assertEqual(valor_total, 0)

    def test_encerra_cliente_id_invalido(self):
        # Teste para um ID de cliente inválido na função encerra_cliente
        print("-" * 50)
        print('\nteste tentando encerrar um cliente inexistente\n')
        print('clientes: %s\nmercado: %s\ncarteiras: %s\n' % (clientes, mercado, carteiras))
        self.assertEqual(encerra_cliente(100), 0) # ID de cliente inexistente

    def test_abre_carteira_inputs_errados(self):
        # Teste para inputs inválidos na função abre_carteira
        print("-" * 50)
        print('\nteste tentando abrir carteira com titular_id = None\n')
        print('clientes: %s\nmercado: %s\ncarteiras: %s\n' % (clientes, mercado, carteiras))
        with self.assertRaises(ValueError):
            abre_carteira(None, "Carteira 1")  # Titulares_id não deve ser None

    def test_movimenta_saldo(self):
        # Teste para a função movimenta_saldo
        print("-" * 50)
        print('\nteste de movimentacao de saldo\n')
        cliente_id = cria_cliente('987654321', 'Jane Doe', '1980-01-01')
        print('cliente id: %s' % cliente_id)
        saldo_inicial = clientes[cliente_id]['saldo']
        print('saldo inicial: %s' % saldo_inicial)
        valor_movimentado = movimenta_saldo(cliente_id, 500)
        print('valor movimentado: %s' % valor_movimentado)
        print('clientes: %s\nmercado: %s\ncarteiras: %s\n' % (clientes, mercado, carteiras))
        self.assertEqual(valor_movimentado, 500)
        self.assertEqual(clientes[cliente_id]['saldo'], saldo_inicial + 500)

    def test_agenda_ordem(self):
        # Teste para a função agenda_ordem
        print("-" * 50)
        print('\nteste de agendamento de ordem\n')
        cliente_id = cria_cliente('987654321', 'Jane Doe', '1980-01-01')
        print('cliente id: %s' % cliente_id)
        carteira_id = abre_carteira(cliente_id, "Carteira 2")
        print('carteira id: %s' % carteira_id)
        sucesso = agenda_ordem(carteira_id, 'COMPRA', 'CUR', 5, 100, '2023-11-11')
        print('sucesso no agendamento: %s' % sucesso)
        print('ordens: %s\n' % ordens)
        self.assertTrue(sucesso)
        self.assertIn((carteira_id, 'COMPRA', 'CUR', 5, 100, '2023-11-11'), ordens)

    def test_imprime_resumo(self):
        # Teste para a função imprime_resumo
        print("-" * 50)
        print('\nteste para a funcao imprime_resumo\n')
        cliente_id = cria_cliente('987654321', 'Jane Doe', '1980-01-01')
        carteira_id = abre_carteira(cliente_id, "Carteira 2")
        resumo = gera_resumo(carteira_id)
        print('impressao do resumo:\n')
        imprime_resumo(resumo)


if __name__ == '__main__':
    unittest.main()
