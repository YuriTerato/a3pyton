# Análise de Conversas do WhatsApp

## Descrição

Aplicação em Python, feita para rodar no console, que lê um arquivo de conversa em grupo exportado do WhatsApp, transforma em um DataFrame do Pandas (data, hora, remetente e mensagem) e permite fazer algumas análises e gráficos.

## Integrantes

Yuri Ramos

## Funcionalidades

- Leitura do arquivo `.txt` exportado do WhatsApp pelo iPhone
- Exibição da tabela completa com data, hora, remetente e mensagem
- Resumo das conversas: total de mensagens por remetente, do maior para o menor
- Histórico do remetente: todas as mensagens dele com data e hora
- Gráfico do histórico do remetente: quantidade de mensagens por dia
- Gráfico de pizza: percentual de mensagens de cada remetente
- Gráfico de linhas: mensagens ao longo do tempo, uma cor para cada remetente

## Tecnologias

- Python
- Pandas
- Matplotlib
- Expressões regulares (módulo `re`)

## Como exportar a conversa do WhatsApp (iPhone)

1. Abra a conversa em grupo no WhatsApp.
2. Toque no nome do grupo, na parte de cima da tela.
3. Role até o final e toque em "Exportar conversa".
4. Escolha "Sem mídia".
5. Envie o arquivo `.txt` gerado para você mesmo (e-mail, iCloud, etc) e salve no computador.

As linhas do arquivo ficam neste formato: `[12/03/2024 14:35:10] Nome: mensagem`. Mensagens do sistema (criptografia, "criou o grupo", etc) são ignoradas.

## Como instalar e executar

1. Clonar o repositório
2. Criar e ativar um ambiente virtual (opcional, mas recomendado):
   ```bash
   python -m venv venv
   venv\Scripts\activate      # Windows
   source venv/bin/activate   # Linux/Mac
   ```
3. Instalar as dependências:
   ```bash
   pip install -r requirements.txt
   ```
4. Rodar a aplicação:
   ```bash
   python main.py
   ```

## Como usar

1. Ao iniciar, informe o caminho do arquivo `.txt` da conversa. O projeto já inclui um arquivo no formato da exportação do iPhone, `_chat.txt` (grupo com 4 pessoas), para testar.
2. A tabela completa da conversa é exibida.
3. Escolha uma opção no menu:
   - **1**, resumo das conversas
   - **2**, histórico de um remetente (escolha o número dele na lista)
   - **3**, gráfico de mensagens por dia de um remetente
   - **4**, gráfico de pizza
   - **5**, gráfico de linhas
   - **6**, mostrar a tabela completa de novo
   - **0**, sair
4. Os gráficos abrem em uma janela, feche a janela para voltar ao menu.

## Estrutura do projeto

```
analise_whatsapp/
├── main.py                  # leitura do arquivo, dataframe, menu e graficos
├── _chat.txt     # conversa de grupo (4 pessoas) no formato do iPhone
├── requirements.txt
└── README.md
```
