import textwrap

def menu_principal():
    menu = '''\n------------------------MENU------------------------\n
            [Z]- Para Sacar
            [X]- Para ver Extrato
            [C]- Para fazer Deposito
            [NC]- Nova Conta
            [NU]- Novo Usuario
            [L]- Lista de Contas
            [S]- Para sair
=>'''
    return input(textwrap.dedent(menu))

def depositar(saldo, valor_deposito, extrato, /):
    if valor_deposito > 0:
            saldo += valor_deposito
            extrato += f'Depósito de R${valor_deposito:.2f}\n'
            print(f'Depósito de R${valor_deposito} realizado com sucesso!')
            print(f'Seu saldo agora é de R${saldo}')
    else:
        print("Por favor, insira um valor positivo.")
    return saldo, extrato

def sacar(*, saldo, valor_saque, extrato, limite, limite_diario, LIMITE_DIARIO):
    passou_saldo = valor_saque > saldo
    passou_limite = valor_saque > limite
    passou_saques = limite_diario >= LIMITE_DIARIO

    if passou_saldo:
        print(f'\n❌-|-Você não tem saldo suficiente(R${saldo})!')

    elif passou_limite:
        print(f'\n❌-|-O valor do saque passou do limite permitido({limite})!')

    elif passou_saques:
        print(f'\n❌-|-Você atingiu o limite diário de saques({limite_diario})! Tente novamente no próximo dia!')

    elif valor_saque > 0:
        saldo -= valor_saque
        extrato += f'Saque de R${valor_saque:.2f}\n'
        limite_diario += 1
        print(f'✅-|-Saque de R${valor_saque} realizado com sucesso!')
    else:
        print('\n❌-|-Valor informado invalido! Ofereça um valor correspondente.')

    return saldo, extrato

def exibir_extrato(saldo, /, *, extrato):
    print('\n------------------------EXTRATO------------------------')
    print("Não foram realizadas movimentações." if not extrato else extrato)
    print(f"\nSaldo:\tR${saldo:.2f}")

def filtrar_usuario(cpf, usuarios):
    usuarios_filtrados = [usuario for usuario in usuarios if usuario['cpf'] == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None

def criar_usuario(usuarios):
    cpf = input('💬-|-Informe o seu CPF: ')
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print('❌-|-Já existe um usúario com este cpf.')
        return
    
    nome = input('💬-|-Informe seu nome completo: ')
    nascimento = input('💬-|-Informe a sua data de nascimento: ')
    endereço = input('💬-|-Informe o seu endereço de email: ')

    usuarios.append({'nome': nome, 'nascimento': nascimento, 'cpf': cpf, 'endereço': endereço})

    print('✅-|-Usúario criado com Sucesso!')

def criar_conta(agencia, numero_conta, usuarios):
    cpf = input('💬-|-Informe o cpf do Usuario: ')
    usuario =  filtrar_usuario(cpf, usuarios)

    if usuario:
        print('\n✅-|-Conta criada com Sucesso!')
        return {'agencia': agencia, 'numero_conta': numero_conta, 'usuario': usuario}
    
    print('\n❌-|-Usúario não encontrado, processo de criação de contas encerrado!')

def listar_contas(contas):
    for conta in contas:
        dados = f'''\
        Agência:\t{conta['agencia']}
        C/C:\t    {conta['numero_conta']}
        Titular:\t{conta['usuario']['nome']}
        '''

    print('=' * 100)
    print(textwrap.dedent(dados))

def main():

    AGENCIA = '0001'
    saldo = 0
    limite = 500
    limite_diario = 0
    LIMITE_DIARIO = 3
    extrato = ''
    usuarios = []
    contas = []

    while True:

        menu_opçoes = menu_principal()

        if menu_opçoes == 'Z':
            valor_saque = float(input('💬-|-Qual o valor que deseja sacar?\n=>'))
            saldo, extrato = sacar(
                saldo=saldo,
                valor_saque=valor_saque,
                extrato=extrato,
                limite=limite,
                limite_diario=limite_diario,
                LIMITE_DIARIO=LIMITE_DIARIO,
                )

        elif menu_opçoes == 'X':
            exibir_extrato(saldo, extrato=extrato)

        elif menu_opçoes == 'C':
            valor_deposito = float(input('💬-|-Qual o valor que deseja depositar em sua conta?\n=> '))
            saldo, extrato = depositar(saldo, valor_deposito, extrato)

        elif menu_opçoes == 'S':
            print('🌐-|-Saindo do menu...')
            break

        elif menu_opçoes == 'NC':
            numero_conta = len(contas) + 1
            conta = criar_conta(AGENCIA, numero_conta, usuarios)

            if conta:
                contas.append(conta)

        elif menu_opçoes == 'NU':
            criar_usuario(usuarios)

        elif menu_opçoes == 'L':
            listar_contas(contas)

        else:
            ('❌-|-Solitação incorreta. Por favor digite uma opção válida do nosso menu!')

main()