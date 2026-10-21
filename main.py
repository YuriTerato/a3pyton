import os
import re
import pandas as pd
import matplotlib.pyplot as plt

# Formato iPhone: [12/03/2024 14:35:10] Nome: mensagem
PADRAO_MENSAGEM = r'^\[(\d{1,2}/\d{1,2}/\d{2,4}),?\s+(\d{1,2}:\d{2})(?::\d{2})?\]\s*([^:]+?):\s(.*)$'
PADRAO_INICIO = r'^\[\d{1,2}/\d{1,2}/\d{2,4}'


def ler_conversa(caminho):
    datas = []
    horas = []
    remetentes = []
    mensagens = []
    ultima_valida = False

    with open(caminho, encoding='utf-8') as arquivo:
        for linha in arquivo:
            linha = linha.replace('\ufeff', '').rstrip().lstrip('\u200e')

            if re.match(PADRAO_INICIO, linha):
                resultado = re.match(PADRAO_MENSAGEM, linha)
                ultima_valida = False

                if resultado:
                    texto = resultado.group(4)

                    # o iPhone marca mensagens do sistema e anexos com um caractere invisivel
                    if texto.startswith('\u200e'):
                        eh_midia = 'anexado' in texto or 'ocultad' in texto or 'omitid' in texto
                        if not eh_midia:
                            continue

                    datas.append(resultado.group(1))
                    horas.append(resultado.group(2))
                    remetentes.append(resultado.group(3).strip())
                    mensagens.append(texto.replace('\u200e', ''))
                    ultima_valida = True

            elif ultima_valida:
                # continuacao de uma mensagem com mais de uma linha
                mensagens[-1] = mensagens[-1] + ' ' + linha

    df = pd.DataFrame({
        'data': datas,
        'hora': horas,
        'remetente': remetentes,
        'mensagem': mensagens
    })
    df['data'] = pd.to_datetime(df['data'], dayfirst=True, format='mixed')
    return df


def mostrar_tabela(df):
    print(df.to_string(formatters={'data': lambda d: d.strftime('%d/%m/%Y')}))


def resumo_conversas(df):
    contagem = df['remetente'].value_counts()

    print('Resumo das conversas')
    print('--------------------')
    for remetente, total in contagem.items():
        print(f'{remetente}: {total} mensagens')


def escolher_remetente(df):
    remetentes = df['remetente'].value_counts().index.tolist()

    print('Remetentes:')
    for i in range(len(remetentes)):
        print(f'{i + 1} - {remetentes[i]}')

    escolha = input('Escolha o numero do remetente: ')

    if not escolha.isdigit() or int(escolha) < 1 or int(escolha) > len(remetentes):
        print('Opcao invalida.')
        return None

    return remetentes[int(escolha) - 1]


def historico_remetente(df):
    remetente = escolher_remetente(df)
    if remetente is None:
        return

    filtro = df[df['remetente'] == remetente]

    print(f'Historico de {remetente} ({len(filtro)} mensagens)')
    print(filtro[['data', 'hora', 'mensagem']].to_string(
        index=False,
        formatters={'data': lambda d: d.strftime('%d/%m/%Y')}
    ))


def grafico_historico_remetente(df):
    remetente = escolher_remetente(df)
    if remetente is None:
        return

    filtro = df[df['remetente'] == remetente]
    por_dia = filtro.groupby('data').size()
    por_dia.index = por_dia.index.strftime('%d/%m/%Y')

    por_dia.plot(kind='bar')
    plt.title(f'Mensagens por dia, {remetente}')
    plt.xlabel('Data')
    plt.ylabel('Quantidade de mensagens')
    plt.tight_layout()
    plt.show()


def grafico_pizza(df):
    contagem = df['remetente'].value_counts()

    contagem.plot(kind='pie', autopct='%1.1f%%')
    plt.title('Percentual de mensagens por remetente')
    plt.ylabel('')
    plt.show()


def grafico_linhas(df):
    por_dia = df.groupby(['data', 'remetente']).size().unstack(fill_value=0)
    por_dia.index = por_dia.index.strftime('%d/%m/%Y')

    por_dia.plot(kind='line', marker='o')
    plt.title('Mensagens ao longo do tempo')
    plt.xlabel('Data')
    plt.ylabel('Quantidade de mensagens')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


def main():
    while True:
        caminho = input('Caminho do arquivo da conversa (.txt): ').strip().strip('"')

        if os.path.exists(caminho):
            break

        print('Arquivo nao encontrado, tente novamente.')

    df = ler_conversa(caminho)

    if df.empty:
        print('Nenhuma mensagem encontrada nesse arquivo.')
        return

    print()
    mostrar_tabela(df)

    continuar = True

    while continuar:
        print()
        print('================================')
        print(' ANALISE DE CONVERSA WHATSAPP')
        print('================================')
        print('1 - Resumo das conversas')
        print('2 - Historico do remetente')
        print('3 - Grafico do historico do remetente')
        print('4 - Grafico de pizza')
        print('5 - Grafico de linhas')
        print('6 - Mostrar tabela completa')
        print('0 - Sair')
        opcao = input('Escolha uma opcao: ')

        if opcao == '1':
            resumo_conversas(df)
        elif opcao == '2':
            historico_remetente(df)
        elif opcao == '3':
            grafico_historico_remetente(df)
        elif opcao == '4':
            grafico_pizza(df)
        elif opcao == '5':
            grafico_linhas(df)
        elif opcao == '6':
            mostrar_tabela(df)
        elif opcao == '0':
            continuar = False
        else:
            print('Opcao invalida.')


if __name__ == '__main__':
    main()
