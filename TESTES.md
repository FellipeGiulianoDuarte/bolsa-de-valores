# Documentação dos Testes Unitários do Projeto P2

## Introdução

Este documento fornece uma visão geral dos testes implementados no módulo `p2` usando a biblioteca `unittest`. Os testes são projetados para verificar o funcionamento correto das funções relacionadas à gestão de clientes, carteiras e operações de mercado.

## Motivação

A motivação por trás desses testes é garantir que o código implementado no módulo `p2` esteja funcionando conforme o esperado e que as operações de criação, manipulação e encerramento de clientes e carteiras sejam realizadas de maneira correta e segura. Isso é fundamental para garantir a integridade dos dados e a consistência das operações de mercado.

## Explicação dos Testes

### 1. Teste de Criação de Cliente
Verifica se a função `cria_cliente` cria corretamente um novo cliente e se o ID do cliente está presente na lista de clientes. Caso falhe, pode indicar um problema na criação de novos clientes.

### 2. Teste de Encerramento de Cliente
Garante que a função `encerra_cliente` encerre corretamente um cliente e que o valor total retornado seja zero após o encerramento. Caso falhe, pode indicar um problema no processo de encerramento do cliente ou no cálculo do valor total.

### 3. Teste de Posição do Cliente
Verifica se a função `posicao_cliente` calcula corretamente a posição total do cliente, levando em consideração o saldo e o valor atual das ações nas carteiras. Também garante que a posição seja atualizada corretamente após as operações. Se falhar, pode indicar um problema no cálculo da posição do cliente.

### 4. Teste de Abertura de Carteira
Garante que a função `abre_carteira` abra corretamente uma nova carteira e que o ID da carteira esteja presente na lista de carteiras. Se falhar, pode indicar um problema na abertura de novas carteiras.

### 5. Teste de Encerramento de Carteira
Verifica se a função `encerra_carteira` encerra corretamente uma carteira e se o valor total obtido com a venda dos títulos é calculado corretamente. Se falhar, pode indicar um problema no processo de encerramento da carteira ou no cálculo do valor total.

### 6. Teste de Encerramento de Cliente com ID Inválido
Garante que a função `encerra_cliente` levante corretamente um erro ao receber um ID de cliente inexistente. Se falhar, pode indicar um problema na validação do ID do cliente.

### 7. Teste de Abertura de Carteira com Inputs Inválidos
Verifica se a função `abre_carteira` levanta corretamente um erro ao fornecer um valor 'titulares_id' inválido. Se falhar, pode indicar um problema na validação dos inputs da função.

### 8. Teste de Movimentação de Saldo
Garante que a função `movimenta_saldo` movimente corretamente o saldo do cliente e que o valor movimentado seja calculado corretamente. Se falhar, pode indicar um problema na movimentação de saldo do cliente.

### 9. Teste de Agendamento de Ordem
Verifica se a função `agenda_ordem` agenda corretamente uma ordem e se ela está presente na lista de ordens. Se falhar, pode indicar um problema no processo de agendamento de ordens.

### 10. Teste de Impressão de Resumo
Verifica se a função `imprime_resumo` imprime corretamente as informações contidas no resumo de uma carteira. Se falhar, pode indicar um problema na geração ou na impressão do resumo.

## Conclusão

A implementação e execução desses testes são essenciais para garantir a confiabilidade e a robustez do módulo `p2`. Através desses testes, é possível identificar e corrigir potenciais problemas, garantindo o bom funcionamento do sistema de gestão de clientes e carteiras no mercado.
