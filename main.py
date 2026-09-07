from dsaentidades.cliente import Cliente
from dsaentidades.conta import ContaCorrente, ContaPoupanca
from dsautilitarios.exceptions import BancoError, SaldoInsuficienteError


def exibir_menu() -> str:
    print("\n" + "=" * 40)
    print("        SISTEMA BANCÁRIO (DSA)        ")
    print("=" * 40)
    print("[1] Criar Cliente e Conta Corrente")
    print("[2] Depositar")
    print("[3] Sacar")
    print("[4] Transferir")
    print("[5] Exibir Extrato")
    print("[6] Listar Contas Cadastradas")
    print("[0] Sair do Sistema")
    print("=" * 40)
    return input("Escolha uma opção: ").strip()


def main():
    contas = {}  # Dicionário para armazenar as contas por número: {numero: conta}
    proximo_numero_conta = 1001

    while True:
        opcao = exibir_menu()

        try:
            # 1. Criar Cliente e Conta
            if opcao == "1":
                nome = input("Digite o nome completo do cliente: ")
                cpf = input("Digite o CPF (apenas números ou formatado): ")

                cliente = Cliente(nome, cpf)
                conta = ContaCorrente(numero=proximo_numero_conta, cliente=cliente)
                cliente.adicionar_conta(conta)

                contas[proximo_numero_conta] = conta
                print(f"\n✅ Conta #{proximo_numero_conta} criada com sucesso para {cliente.nome}!")
                proximo_numero_conta += 1

            # 2. Depositar
            elif opcao == "2":
                num_conta = int(input("Número da conta: "))
                if num_conta not in contas:
                    print("❌ Conta não encontrada!")
                    continue

                valor = float(input("Valor do depósito: R$ "))
                contas[num_conta].depositar(valor)
                print(f"✅ Depósito de R${valor:.2f} realizado! Saldo atual: R${contas[num_conta].saldo:.2f}")

           # 3. Sacar
            elif opcao == "3":
                num_conta = int(input("Número da conta: "))
                if num_conta not in contas:
                    print("❌ Conta não encontrada!")
                    continue

                valor = float(input("Valor do saque: R$ "))
                conta = contas[num_conta]
                
                # Realiza o saque
                conta.sacar(valor)
                
                # Exibe a confirmação de acordo com o estado do saldo
                if conta.saldo < 0:
                    # Verifica se a conta possui limite (ex: ContaCorrente)
                    limite_total = getattr(conta, "limite", 0.0)
                    limite_restante = limite_total + conta.saldo
                    
                    print(f"✅ Saque de R${valor:.2f} realizado!")
                    print(f"⚠️ ATENÇÃO: Você entrou no cheque especial!")
                    print(f"   • Saldo atual: R${conta.saldo:.2f}")
                    print(f"   • Limite restante disponível: R${limite_restante:.2f}")
                else:
                    print(f"✅ Saque de R${valor:.2f} realizado! Saldo atual: R${conta.saldo:.2f}")
                    
            # 4. Transferir
            elif opcao == "4":
                origem = int(input("Número da sua conta (Origem): "))
                destino = int(input("Número da conta de destino: "))

                if origem not in contas or destino not in contas:
                    print("❌ Conta de origem ou destino não encontrada!")
                    continue

                valor = float(input("Valor da transferência: R$ "))
                contas[origem].transferir(valor, contas[destino])
                print(f"✅ Transferência de R${valor:.2f} realizada com sucesso!")

            # 5. Extrato
            elif opcao == "5":
                num_conta = int(input("Número da conta: "))
                if num_conta not in contas:
                    print("❌ Conta não encontrada!")
                    continue

                conta = contas[num_conta]
                print(f"\n📌 Extrato - {conta.cliente.nome} (Conta #{conta.numero})")
                print(f"Saldo Atual: R${conta.saldo:.2f} | Limite: R${conta.limite:.2f}")
                print("-" * 40)
                if not conta.historico:
                    print("Nenhuma movimentação realizada.")
                else:
                    for t in conta.historico:
                        print(t)

            # 6. Listar Contas
            elif opcao == "6":
                if not contas:
                    print("\n⚠️ Nenhuma conta cadastrada ainda.")
                else:
                    print("\n📋 Contas Cadastradas:")
                    for num, c in contas.items():
                        print(f"• Conta #{num} | Cliente: {c.cliente.nome} | Saldo: R${c.saldo:.2f}")

            # 0. Sair
            elif opcao == "0":
                print("\nObrigado por utilizar o Sistema Bancário DSA! Até logo.")
                break

            else:
                print("❌ Opção inválida! Tente novamente.")

        except SaldoInsuficienteError as e:
            print(f"\n❌ [ERRO DE SALDO]: {e}")
        except ValueError as e:
            print(f"\n❌ [ERRO DE VALIDAÇÃO]: {e}")
        except BancoError as e:
            print(f"\n❌ [ERRO DO BANCO]: {e}")
        except Exception as e:
            print(f"\n❌ [ERRO INESPERADO]: {e}")


if __name__ == "__main__":
    main()