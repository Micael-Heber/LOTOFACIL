# login.py - VERSÃO FINAL CORRIGIDA (COM gerador_final)
import json
import bcrypt
import os
import sys

def verificar_senha(senha_digitada, senha_hash):
    """Verifica se a senha está correta (seguro)"""
    try:
        return bcrypt.checkpw(
            senha_digitada.encode('utf-8'),
            senha_hash.encode('utf-8')
        )
    except:
        return False

def fazer_login():
    """Tela de login"""
    print("\n" + "="*50)
    print("         🎰 LOTOFÁCIL - ACESSO RESTRITO")
    print("="*50)
    print("         Digite suas credenciais")
    print("="*50)
    
    # Carrega usuários
    arquivo = "data/usuarios.json"
    
    if not os.path.exists(arquivo):
        print("\n❌ Nenhum usuário cadastrado!")
        print("💡 Execute primeiro: python criar_admin.py")
        input("\nPressione Enter para sair...")
        return False
    
    try:
        with open(arquivo, 'r', encoding='utf-8') as f:
            dados = json.load(f)
    except:
        print("\n❌ Erro ao carregar banco de dados")
        return False
    
    # 3 tentativas
    tentativas = 3
    while tentativas > 0:
        print(f"\n📝 Tentativas restantes: {tentativas}")
        print("-"*30)
        
        usuario = input("Usuário: ").strip()
        senha = input("Senha: ").strip()
        
        # Procura usuário
        usuario_encontrado = None
        for u in dados.get("usuarios", []):
            if u["usuario"] == usuario:
                usuario_encontrado = u
                break
        
        if usuario_encontrado and verificar_senha(senha, usuario_encontrado["senha_hash"]):
            print(f"\n✅ Login bem-sucedido!")
            print(f"👋 Bem-vindo, {usuario_encontrado.get('nome', usuario)}!")
            
            # Configura variável de ambiente para autorização
            os.environ['LOGIN_AUTORIZADO'] = 'true'
            os.environ['USUARIO_LOGADO'] = usuario
            
            return True
        else:
            print("❌ Usuário ou senha incorretos!")
            tentativas -= 1
    
    print("\n⛔ Número máximo de tentativas excedido!")
    return False

def menu_principal():
    """Menu após login"""
    print("\n" + "="*50)
    print("         📋 MENU PRINCIPAL")
    print("="*50)
    print("1. Gerar palpites")
    print("2. Sair")
    print("="*50)
    
    while True:
        try:
            opcao = input("\nEscolha: ").strip()
            
            if opcao == "1":
                print("\n🔮 Carregando gerador de palpites...\n")
                
                # IMPORTANDO O ARQUIVO CORRETO: gerador_final.py
                try:
                    import gerador_final
                    gerador_final.main()
                except ImportError:
                    print("❌ Erro: arquivo gerador_final.py não encontrado!")
                    print("💡 Verifique se o arquivo existe na pasta")
                except Exception as e:
                    print(f"❌ Erro ao executar gerador: {e}")
                
                # Volta ao menu após sair do gerador
                print("\n" + "="*50)
                print("🔄 Voltando ao menu principal...")
                print("="*50)
                
            elif opcao == "2":
                print("\n👋 Até logo! Boa sorte! 🍀")
                sys.exit(0)
            else:
                print("❌ Opção inválida! Digite 1 ou 2")
                
        except KeyboardInterrupt:
            print("\n\n👋 Programa interrompido pelo usuário")
            sys.exit(0)
        except Exception as e:
            print(f"\n❌ Erro inesperado: {e}")

def main():
    """Função principal"""
    if fazer_login():
        menu_principal()
    else:
        print("\n🔒 Acesso negado. Programa encerrado.")
        input("\nPressione Enter para sair...")

if __name__ == "__main__":
    main()
    