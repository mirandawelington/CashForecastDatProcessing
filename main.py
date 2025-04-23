import pandas as pd

# Carregar o arquivo CSV
df = pd.read_csv('data/CF01 Cash Forecast  by Bank (9).csv', low_memory=False)

# Filtrar o dataframe
df_opening_balance = df[df['Line Item'] == 'Opening balance'].copy()

# Separar a coluna 'Period' em três colunas: 'dia', 'mes' e 'ano'
df_opening_balance[['dia', 'mes', 'ano']] = df_opening_balance['Period'].str.split(' ', expand=True)

# Dicionário de mapeamento de meses em inglês para português
meses_map = {
    'Jan': 'Jan',
    'Feb': 'Fev',
    'Mar': 'Mar',
    'Apr': 'Abr',
    'May': 'Mai',
    'Jun': 'Jun',
    'Jul': 'Jul',
    'Aug': 'Ago',
    'Sep': 'Set',
    'Oct': 'Out',
    'Nov': 'Nov',
    'Dec': 'Dez'
}

# Substituir os meses em inglês pelos meses em português
df_opening_balance.loc[:, 'mes'] = df_opening_balance['mes'].map(meses_map)

# Excluir a coluna 'Period'
df_opening_balance = df_opening_balance.drop(columns=['Period'])

# Juntar as colunas 'dia', 'mes' e 'ano' em uma coluna chamada 'Period' separada por espaço
df_opening_balance['Period'] = df_opening_balance[['dia', 'mes', 'ano']].agg(' '.join, axis=1)

print(df_opening_balance.head())

# Função para filtrar dados com base na seleção do usuário
def filtrar_dados(df):
    # Solicitar ao usuário para selecionar o ano
    ano_selecionado = input("Digite o ano que deseja filtrar (ex: 21): ")

    # Solicitar ao usuário para selecionar os meses (separados por vírgula)
    meses_selecionados = input("Digite os meses que deseja filtrar (ex: Jan, Fev): ").split(', ')

    # Filtrar o DataFrame com base no ano e meses selecionados
    df_filtrado = df[(df['ano'] == ano_selecionado) & (df['mes'].isin(meses_selecionados))]

    return df_filtrado

# Chamar a função e gerar o relatório
df_filtrado = filtrar_dados(df_opening_balance)
print("Relatório filtrado:")
print(df_filtrado)

# Excluir as colunas 'dia', 'mes' e 'ano' após a filtragem
df_filtrado = df_filtrado.drop(columns=['dia', 'mes', 'ano'])

print(df_filtrado.head())

#Excluindo coluna Open balance
df_filtrado = df_filtrado.drop(columns=['Line Item'])


# Renomear a coluna 'Value' para 'Cash balance'
df_filtrado = df_filtrado.rename(columns={'Value': 'Cash balance'})

# Exportar o DataFrame para um arquivo Excel
df_filtrado.to_excel('resultado.xlsx', index=False)
