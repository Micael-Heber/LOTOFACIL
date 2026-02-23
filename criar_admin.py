# criar_admin.py
import json
import bcrypt
import os
from datetime import datetime

def hash_senha(senha):
    """Cria hash seguro da senha"""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(senha.encode('utf-8'), salt).decode('utf-8')

def criar_usuario_inicial():
    print("\n" + "="*50)
    print("👤 CRIAR USUÁRIO ADMINISTRADOR")
    print("="*50)
    
    # Garante que pasta data existe
    os.makedirs("data", exist_ok=True)
    
    arquivo = "data/usuarios.json"
    
    # Verifica se já existe
    if os.path.exists(arquivo):
        with open(arquivo, 'r') as f:
            dados = json.load(f)
        if dados.get("usuarios"):
            print("✅ Já existem usuários cadastrados!")
            return
    
    # Pede dados do admin
    usuario = input("Nome de usuário (padrão: admin): ").strip()
    if not usuario:
        usuario = "admin"
    
    senha = input("Senha: ").strip()
    while len(senha) < 4:
        print("❌ Senha deve ter pelo menos 4 caracteres")
        senha = input("Senha: ").strip()
    
    confirmar = input("Confirme a senha: ").strip()
    
    if senha != confirmar:
        print("❌ Senhas não conferem!")
        return
    
    nome = input("Nome completo (opcional): ").strip()
    if not nome:
        nome = "Administrador"
    
    # Cria hash
    senha_hash = hash_senha(senha)
    
    # Salva
    dados = {
        "usuarios": [{
            "id": 1,
            "usuario": usuario,
            "senha_hash": senha_hash,
            "nome": nome,
            "criado_em": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }]
    }
    
    with open(arquivo, 'w', encoding='utf-8') as f:
        json.dump(dados, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Usuário '{usuario}' criado com sucesso!")
    print("🔒 Senha armazenada com segurança (hash bcrypt)")

if __name__ == "__main__":
    criar_usuario_inicial()