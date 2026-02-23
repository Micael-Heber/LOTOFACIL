# main_novo.py - OTIMIZADO PARA PYTHON 3.14
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter
import random
from datetime import datetime
import os

class LotofacilAnalyzer:
    def __init__(self):
        self.total_numeros = 25
        self.numeros_sorteados = 15
        print("🎰 LOTOFÁCIL ANALYZER v1.0 - Python 3.14")
        print("="*50)
    
    def gerar_historico(self, n_concursos=200):
        """Gera histórico realista de concursos"""
        print(f"🎲 Gerando {n_concursos} concursos históricos...")
        
        # Frequências baseadas em dados reais (25 é mais frequente)
        pesos = np.array([1.0, 0.95, 1.05, 0.92, 1.03,
                         0.97, 1.08, 0.91, 1.02, 0.96,
                         1.04, 0.93, 1.06, 0.94, 1.01,
                         0.98, 1.07, 0.90, 1.03, 0.95,
                         1.05, 0.92, 1.09, 0.93, 1.15])  # 25 tem peso 1.15
        
        pesos = pesos / pesos.sum()
        
        dados = []
        for i in range(1, n_concursos + 1):
            # Gera 15 números únicos com pesos
            numeros = np.random.choice(
                range(1, 26),
                size=15,
                replace=False,
                p=pesos
            )
            
            # Adiciona algum padrão de "sequências" ocasionais
            if i % 20 == 0:
                # A cada 20 concursos, força algumas sequências
                seq = random.randint(1, 20)
                numeros = np.array(list(set(numeros.tolist()[:12] + [seq, seq+1, seq+2])))
                numeros = np.random.choice(numeros, 15, replace=False)
            
            dados.append([i] + sorted(numeros.tolist()))
        
        # Cria DataFrame
        colunas = ['Concurso'] + [f'N{i}' for i in range(1, 16)]
        self.df = pd.DataFrame(dados, columns=colunas)
        
        # Salva
        os.makedirs('data', exist_ok=True)
        self.df.to_csv('data/historico_realista.csv', index=False, encoding='utf-8-sig')
        
        print(f"✅ Histórico salvo: {len(self.df)} concursos")
        print(f"📁 Arquivo: data/historico_realista.csv")
        
        return self.df
    
    def analisar_estatisticas(self):
        """Análise estatística avançada"""
        if not hasattr(self, 'df'):
            print("❌ Primeiro gere o histórico (opção 1)")
            return
        
        print("\n📊 ANÁLISE ESTATÍSTICA AVANÇADA")
        print("="*50)
        
        # 1. Frequência básica
        todos_numeros = self.df[[f'N{i}' for i in range(1, 16)]].values.flatten()
        freq_series = pd.Series(todos_numeros).value_counts().sort_index()
        
        print("\n1️⃣ FREQUÊNCIA POR NÚMERO:")
        for num in range(1, 26):
            qtd = freq_series.get(num, 0)
            percentual = (qtd / len(self.df)) * 100
            barra = '█' * int(percentual / 2)
            print(f"  Nº {num:2d}: {qtd:4d} vezes | {percentual:5.1f}% {barra}")
        
        # 2. Top mais e menos sorteados
        print("\n2️⃣ TOP 5 MAIS SORTEADOS:")
        for num, qtd in freq_series.nlargest(5).items():
            print(f"  Nº {num:2d}: {qtd:4d} vezes")
        
        print("\n3️⃣ TOP 5 MENOS SORTEADOS:")
        for num, qtd in freq_series.nsmallest(5).items():
            print(f"  Nº {num:2d}: {qtd:4d} vezes")
        
        # 3. Atrasos atuais
        print("\n4️⃣ ATRASOS ATUAIS (últimos 20 concursos):")
        ultimos_20 = self.df[[f'N{i}' for i in range(1, 16)]].tail(20).values
        
        atrasos = {}
        for num in range(1, 26):
            atraso = 0
            for concurso in reversed(ultimos_20):
                if num in concurso:
                    break
                atraso += 1
            atrasos[num] = atraso
        
        for num, atraso in sorted(atrasos.items(), key=lambda x: x[1], reverse=True)[:10]:
            if atraso >= 10:
                print(f"  Nº {num:2d}: {atraso:3d} concursos sem aparecer ⚠️")
        
        # 4. Distribuição Par/Ímpar
        print("\n5️⃣ DISTRIBUIÇÃO PAR/ÍMPAR (média histórica):")
        proporcoes = []
        for _, row in self.df.iterrows():
            numeros_concurso = [row[f'N{i}'] for i in range(1, 16)]
            pares = sum(1 for n in numeros_concurso if n % 2 == 0)
            proporcoes.append(pares)
        
        media_pares = np.mean(proporcoes)
        print(f"  Média de números pares por concurso: {media_pares:.1f}")
        print(f"  (Distribuição ideal: 7-8 pares, 7-8 ímpares)")
        
        # 5. Soma dos números
        print("\n6️⃣ SOMA DOS NÚMEROS (por concurso):")
        somas = [sum([row[f'N{i}'] for i in range(1, 16)]) for _, row in self.df.iterrows()]
        print(f"  Média: {np.mean(somas):.1f}")
        print(f"  Mínimo: {np.min(somas)}")
        print(f"  Máximo: {np.max(somas)}")
        print(f"  (Faixa comum: 180-220)")
        
        return freq_series
    
    def sugerir_palpites(self, freq_series, n_palpites=5):
        """Gera palpites inteligentes baseados em estatísticas"""
        print(f"\n🎯 GERANDO {n_palpites} PALPITES INTELIGENTES")
        print("="*50)
        
        # Calcula probabilidades ponderadas
        pesos = {}
        for num in range(1, 26):
            freq = freq_series.get(num, 0)
            peso_base = freq / len(self.df) if len(self.df) > 0 else 0.04
            
            # Ajusta por atraso (números muito atrasados têm peso maior)
            ultimos_30 = self.df[[f'N{i}' for i in range(1, 16)]].tail(30).values
            atraso = 0
            for concurso in reversed(ultimos_30):
                if num in concurso:
                    break
                atraso += 1
            
            # Fórmula: base + ajuste por atraso
            peso = peso_base * (1 + min(atraso / 50, 0.5))  # Até 50% de aumento para atrasos
            
            pesos[num] = peso
        
        # Normaliza pesos
        total_pesos = sum(pesos.values())
        probabilidades = {num: peso/total_pesos for num, peso in pesos.items()}
        
        for p in range(n_palpites):
            print(f"\n🔮 PALPITE {p+1}:")
            
            # Seleciona 15 números baseado nas probabilidades
            numeros = list(probabilidades.keys())
            probs = list(probabilidades.values())
            
            palpite = set()
            tentativas = 0
            
            while len(palpite) < 15 and tentativas < 100:
                num = np.random.choice(numeros, p=probs)
                palpite.add(num)
                tentativas += 1
            
            # Completa se necessário
            if len(palpite) < 15:
                for num in range(1, 26):
                    if num not in palpite:
                        palpite.add(num)
                    if len(palpite) == 15:
                        break
            
            palpite_ordenado = sorted(palpite)
            
            # Estatísticas do palpite
            pares = sum(1 for n in palpite_ordenado if n % 2 == 0)
            soma_total = sum(palpite_ordenado)
            primos = len([n for n in palpite_ordenado if n in [2,3,5,7,11,13,17,19,23]])
            
            print(f"  Números: {palpite_ordenado}")
            print(f"  Estatísticas: {pares} pares | {15-pares} ímpares | {primos} primos")
            print(f"  Soma: {soma_total} (ideal: 180-220)")
            
            # Verifica se segue padrões históricos
            if 7 <= pares <= 8 and 180 <= soma_total <= 220:
                print(f"  ✅ BOA DISTRIBUIÇÃO!")
            else:
                print(f"  ⚠️  Distribuição atípica")
    
    def criar_grafico(self, freq_series):
        """Cria gráfico de frequência"""
        try:
            import matplotlib.pyplot as plt
            
            plt.figure(figsize=(12, 6))
            
            # Gráfico de barras
            bars = plt.bar(range(1, 26), [freq_series.get(i, 0) for i in range(1, 26)])
            
            # Destaca os mais frequentes
            for i, bar in enumerate(bars):
                if freq_series.get(i+1, 0) > freq_series.mean():
                    bar.set_color('green')
                elif freq_series.get(i+1, 0) < freq_series.mean():
                    bar.set_color('red')
            
            plt.xlabel('Número', fontsize=12)
            plt.ylabel('Frequência', fontsize=12)
            plt.title(f'Frequência dos Números - {len(self.df)} Concursos', fontsize=14, fontweight='bold')
            plt.xticks(range(1, 26))
            plt.grid(True, alpha=0.3, linestyle='--')
            
            # Linha da média
            media = freq_series.mean()
            plt.axhline(y=media, color='blue', linestyle='--', alpha=0.7, label=f'Média: {media:.1f}')
            plt.legend()
            
            plt.tight_layout()
            
            # Salva
            os.makedirs('data', exist_ok=True)
            plt.savefig('data/frequencia_numeros.png', dpi=150, bbox_inches='tight')
            plt.show()
            
            print("\n📈 Gráfico salvo: data/frequencia_numeros.png")
            
        except Exception as e:
            print(f"⚠️  Não foi possível criar gráfico: {e}")

def main():
    """Função principal"""
    print("\n" + "="*60)
    print("         🎰 ANALISADOR LOTOFÁCIL - PYTHON 3.14")
    print("="*60)
    
    # Verifica dependências
    try:
        import pandas as pd
        import numpy as np
        print(f"✅ pandas: {pd.__version__}")
        print(f"✅ numpy: {np.__version__}")
    except ImportError as e:
        print(f"❌ Erro: {e}")
        print("💡 Execute: pip install numpy pandas matplotlib")
        return
    
    # Cria analisador
    analyzer = LotofacilAnalyzer()
    
    # Menu
    while True:
        print("\n" + "="*50)
        print("📋 MENU PRINCIPAL:")
        print("1. Gerar histórico de concursos")
        print("2. Analisar estatísticas")
        print("3. Sugerir palpites")
        print("4. Criar gráfico")
        print("5. Sair")
        print("="*50)
        
        try:
            opcao = input("\n👉 Escolha uma opção (1-5): ").strip()
            
            if opcao == "1":
                n = input("Quantos concursos gerar? (padrão: 200): ").strip()
                n = int(n) if n.isdigit() else 200
                analyzer.gerar_historico(n)
                
            elif opcao == "2":
                freq = analyzer.analisar_estatisticas()
                analyzer.freq_series = freq
                
            elif opcao == "3":
                if hasattr(analyzer, 'freq_series'):
                    n = input("Quantos palpites gerar? (padrão: 5): ").strip()
                    n = int(n) if n.isdigit() else 5
                    analyzer.sugerir_palpites(analyzer.freq_series, n)
                else:
                    print("❌ Primeiro execute a análise (opção 2)")
                    
            elif opcao == "4":
                if hasattr(analyzer, 'freq_series'):
                    analyzer.criar_grafico(analyzer.freq_series)
                else:
                    print("❌ Primeiro execute a análise (opção 2)")
                    
            elif opcao == "5":
                print("\n👋 Até logo! Boa sorte nos seus jogos!")
                print("💡 Lembre-se: Loteria é entretenimento, jogue com responsabilidade!")
                break
                
            else:
                print("❌ Opção inválida!")
                
        except KeyboardInterrupt:
            print("\n\n👋 Interrompido pelo usuário")
            break
        except Exception as e:
            print(f"\n❌ Erro: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    main()