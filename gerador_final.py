# gerador_final.py - VERSÃO FINAL CORRIGIDA
import pandas as pd
import numpy as np
import os
import sys

# ===== PROTEÇÃO DE ACESSO =====
if not os.environ.get('LOGIN_AUTORIZADO'):
    print("\n" + "="*50)
    print("⛔ ACESSO NEGADO")
    print("="*50)
    print("Faça login primeiro:")
    print("python login.py")
    print("="*50)
    sys.exit(1)
# ===== FIM DA PROTEÇÃO =====

class GeradorFinalLotofacil:
    def __init__(self):
        self.carregar_dados()
    
    def carregar_dados(self):
        """Carrega os dados do histórico"""
        try:
            self.df = pd.read_csv("data/historico.csv")
            # Encontra colunas de números
            self.colunas_numeros = [c for c in self.df.columns if 'Bola' in str(c)][:15]
        except Exception as e:
            print(f"❌ Erro ao carregar histórico: {e}")
            exit(1)
    
    def calcular_probabilidades(self):
        """Calcula probabilidades de forma otimizada"""
        # Calcula frequências
        freq = {}
        for num in range(1, 26):
            contagem = 0
            for col in self.colunas_numeros:
                contagem += (self.df[col] == num).sum()
            freq[num] = contagem
        
        # Ajusta por atraso
        probabilidades = {}
        ultimos_30 = self.df[self.colunas_numeros].tail(30).values
        
        for num in range(1, 26):
            # Frequência normalizada
            f_norm = freq[num] / len(self.df) if len(self.df) > 0 else 0.04
            
            # Atraso atual
            atraso = 0
            for concurso in reversed(ultimos_30):
                if num in concurso:
                    break
                atraso += 1
            
            # Combina frequência com atraso
            peso_atraso = min(1.0, atraso / 40)
            probabilidades[num] = f_norm * 0.7 + peso_atraso * 0.3
        
        # Normaliza
        soma = sum(probabilidades.values())
        return {num: p/soma for num, p in probabilidades.items()}
    
    def gerar_palpite_ideal(self):
        """Gera o palpite mais provável"""
        probabilidades = self.calcular_probabilidades()
        
        numeros = list(range(1, 26))
        probs = [probabilidades[num] for num in numeros]
        
        melhor_palpite = None
        melhor_pontuacao = -1
        
        # Testa 500 combinações
        for _ in range(500):
            palpite_raw = np.random.choice(numeros, 15, replace=False, p=probs)
            palpite = sorted(palpite_raw)
            
            # Avalia qualidade
            pares = sum(1 for n in palpite if n % 2 == 0)
            soma_val = sum(palpite)
            
            pontuacao = 0
            if 7 <= pares <= 8:
                pontuacao += 2
            if 180 <= soma_val <= 220:
                pontuacao += 2
            
            # Distribuição por grupos
            grupos_ok = True
            for inicio in range(1, 26, 5):
                fim = inicio + 4
                qtd = sum(1 for n in palpite if inicio <= n <= fim)
                if not (2 <= qtd <= 4):
                    grupos_ok = False
                    break
            
            if grupos_ok:
                pontuacao += 1
            
            if pontuacao > melhor_pontuacao:
                melhor_pontuacao = pontuacao
                melhor_palpite = palpite
        
        return melhor_palpite
    
    def mostrar_cartela(self, palpite):
        """Mostra apenas a cartela com os números"""
        print("\n" + "="*50)
        print("🎫 PALPITE GERADO - LOTOFÁCIL")
        print("="*50)
        print()
        
        # Cartela visual
        print("    1    2    3    4    5")
        print("  " + "─"*25)
        
        for linha in range(5):
            linha_numeros = []
            for col in range(5):
                num = linha * 5 + col + 1
                if num in palpite:
                    linha_numeros.append(f"[{num:2d}]")
                else:
                    linha_numeros.append(f" {num:2d} ")
            
            print("  " + " ".join(linha_numeros))
        
        print("  " + "─"*25)
        print()
    
    def menu_principal(self):
        """Menu principal - já começa com um palpite gerado"""
        
        # GERA O PRIMEIRO PALPITE AUTOMATICAMENTE AO ENTRAR
        print("\n🔮 Gerando primeiro palpite...")
        palpite_atual = self.gerar_palpite_ideal()
        self.mostrar_cartela(palpite_atual)
        
        # Menu de opções
        while True:
            print("\n" + "="*50)
            print("📋 O QUE DESEJA FAZER?")
            print("="*50)
            print("1. Gerar NOVO palpite")
            print("2. Ver estatísticas deste palpite")
            print("3. Voltar ao menu principal")
            print("4. Sair")
            print("="*50)
            
            try:
                opcao = input("\nEscolha: ").strip()
                
                if opcao == "1":
                    print("\n🔮 Gerando novo palpite...")
                    palpite_atual = self.gerar_palpite_ideal()
                    self.mostrar_cartela(palpite_atual)
                    
                elif opcao == "2":
                    self.mostrar_estatisticas(palpite_atual)
                    
                elif opcao == "3":
                    print("\n🔄 Voltando ao menu principal...")
                    return
                    
                elif opcao == "4":
                    print("\n👋 Boa sorte! 🍀")
                    sys.exit(0)
                    
                else:
                    print("❌ Opção inválida!")
                    
            except KeyboardInterrupt:
                print("\n\n👋 Programa encerrado")
                sys.exit(0)
    
    def mostrar_estatisticas(self, palpite):
        """Mostra estatísticas do palpite atual"""
        print("\n" + "="*50)
        print("📊 ESTATÍSTICAS DO PALPITE")
        print("="*50)
        
        pares = sum(1 for n in palpite if n % 2 == 0)
        soma = sum(palpite)
        primos = len([n for n in palpite if n in [2,3,5,7,11,13,17,19,23]])
        
        print(f"\n• Pares: {pares} | Ímpares: {15-pares}")
        print(f"• Soma total: {soma}")
        print(f"• Números primos: {primos}")
        
        # Distribuição por grupos
        print(f"\n• Distribuição:")
        grupos = ["1-5", "6-10", "11-15", "16-20", "21-25"]
        for i, grupo in enumerate(grupos):
            inicio = i * 5 + 1
            fim = inicio + 4
            qtd = sum(1 for n in palpite if inicio <= n <= fim)
            print(f"  {grupo}: {qtd} números")
        
        input("\nPressione Enter para continuar...")

# EXECUÇÃO PRINCIPAL
def main():
    print("\n" + "="*50)
    print("         🎲 LOTOFÁCIL - GERADOR INTELIGENTE")
    print("="*50)
    
    # Verifica arquivo
    if not os.path.exists("data/historico.csv"):
        print("\n❌ Arquivo data/historico.csv não encontrado!")
        input("\nPressione Enter para sair...")
        return
    
    # Inicia gerador
    try:
        gerador = GeradorFinalLotofacil()
        gerador.menu_principal()
    except Exception as e:
        print(f"\n❌ Erro: {e}")
        input("\nPressione Enter para sair...")

if __name__ == "__main__":
    main()