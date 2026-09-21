---

## 🚀 Instalação

Para rodar o projeto, você precisa ter o Python 3.10 ou superior e o pip instalados. O primeiro passo é clonar o repositório com o comando `git clone https://github.com/seu-usuario/lotofacil.git` e entrar na pasta com `cd lotofacil`. Em seguida, crie um ambiente virtual com `python -m venv venv` e ative-o — no Windows use `.\venv\Scripts\activate` e no Linux/Mac use `source venv/bin/activate`. Depois, instale todas as dependências com `pip install -r requirements.txt`. Agora coloque o arquivo `historico.csv` dentro da pasta `data/`, garantindo que ele contenha as colunas `Bola1`, `Bola2`, ..., `Bola15` com os números sorteados. Para iniciar o backend, execute `python app.py` — a API ficará disponível em `http://localhost:5000`. Por fim, abra o arquivo `index.html` diretamente no navegador ou sirva-o com `python -m http.server 8000` e acesse `http://localhost:8000`.

---

## 🎮 Como Usar

Cadastre-se na página inicial clicando em "Cadastrar", faça login com seu e-mail e senha, clique em "Gerar Novo Palpite" para receber uma combinação otimizada, visualize a cartela com os números destacados e, se quiser, veja as estatísticas do palpite (pares, ímpares, soma, etc.).

---

## 🧠 Lógica do Algoritmo

O algoritmo combina quatro pilares estatísticos para calcular a probabilidade de cada número: frequência histórica (35%), atraso atual (30%), tendência recente (20%) e distribuição ideal (15%). Além disso, o sistema aplica filtros para garantir que o palpite final tenha 7 ou 8 números pares, soma entre 180 e 220 e distribuição equilibrada entre as cinco faixas (1-5, 6-10, 11-15, 16-20, 21-25). Dessa forma, os palpites gerados seguem os padrões mais recorrentes nos sorteios reais, aumentando as chances estatísticas de acertos menores (11, 12 e 13 pontos).

---

## 🔒 Segurança

As senhas são armazenadas com hash bcrypt (nunca em texto puro), a autenticação é feita via JWT com expiração configurável, as rotas são protegidas por middleware que valida o token e recomenda-se usar HTTPS em produção e variáveis de ambiente para a chave secreta.

---

## 🤝 Contribuição

Contribuições são bem-vindas! Faça um fork do projeto, crie uma branch para sua feature (`git checkout -b feature/nova-funcionalidade`), commit suas mudanças (`git commit -m 'Adiciona nova funcionalidade'`), push para a branch (`git push origin feature/nova-funcionalidade`) e abra um Pull Request.

---

## 📄 Licença

Este projeto está licenciado sob a MIT License. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

---

## ⚠️ Aviso Legal

Este software é uma ferramenta de análise estatística e não garante ganhos em loterias. A Lotofácil é um jogo de azar e os resultados são aleatórios. Use este sistema como auxílio, mas jogue com responsabilidade e apenas com valores que você pode perder.

---

Desenvolvido com ❤️ por [MICAEL HEBER] (https://github.com/seu-usuario](https://github.com/Micael-Heber))
