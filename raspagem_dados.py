from requests import get
import csv
from bs4 import BeautifulSoup


def append_list_as_row(file_name, list_of_elem):
    # Open file in append mode
    with open(file_name, 'a+', newline='') as write_obj:
        # Create a writer object from csv module
        csv_writer = csv.writer(write_obj)
        # Add contents of list as last row in the csv file
        csv_writer.writerow(list_of_elem)

nome_colunas = ['Nome Empresa', 'Setor', 'Endereço', 'CEP', "Cidade", "Estado", "Nome Contato", "Telefone", "E-mail"]

append_list_as_row('empresas_associadas.csv', nome_colunas)
append_list_as_row('empresas_nao_associadas.csv', nome_colunas)

# ---------------------------------------------------------------------------------------------------------------------------------

nome_setor = ['AÇÚCAR%20E%20ÁLCOOL', 'AEROESPACIAL', 'AGRICULTURA',
              'ALIMENTÍCIO', 'BARES,%20RESTAURANTES%20E%20SIMILARES', 'BORRACHA',
              'CELULOSE%20E%20PAPEL', 'CERÂMICO', 'CIMENTO%20E%20MINERAÇÃO', 
              'COMBATE%20A%20INCÊNDIO', 'CONSTRUÇÃO%20CIVIL', 'COURO%20E%20CALÇADO',
              'EQUIPAMENTOS%20ÓPTICOS', 'FARMACÊUTICO', 'FERRAMENTAS',
              'FUNDIÇÃO', 'GERAÇÃO%20DE%20ENERGIA', 'GINÁSTICA',
              'GRÁFICO', 'IRRIGAÇÃO', 'JARDINAGEM', 'JÓIAS%20E%20BIJUTERIAS',
              'LAVANDERIA%20INDUSTRIAL', 'LIMPEZA%20INDUSTRIAL', 
              'MADEIRA', 'MÁQUINAS%20FERROVIÁRIAS', 'MÁQUINAS%20RODOVIÁRIAS',
              'MÁQUINAS-FERRAMENTA', 'MÁRMORE%20E%20GRANITO', 'MUNIÇÕES',
              'NAVAL%20E%20OFFSHORE', 'PARQUE%20DE%20DIVERSÃO%20E%20TEMÁTICO',
              'PECUÁRIA', 'PETRÓLEO%20E%20PETROQUÍMICA', 'PLÁSTICO', 'POSTOS%20DE%20ABASTECIMENTO%20E%20SERVIÇOS',
              'PROTEÇÃO%20E%20TRATAMENTO%20SUPERFICIAL', 'QUÍMICO%20E%20DERIVADOS', 'RAÇÃO%20INDUSTRIAL', 'RECICLAGEM',
              'REPARO%20E%20MANUTENÇÃO%20AUTOMOTIVA', 'SANEAMENTO%20BÁSICO%20E%20AMBIENTAL', 'SIDERURGIA', 'TABACO', 
              'TÊXTIL', 'VIDRO', 'AGITADOR', 'AR%20COMPRIMIDO%20/%20VÁCUO', 'BOMBAS,%20MOTOBOMBAS%20E%20ACESSÓRIOS',
              'CALDEIRAS', 'CENTRÍFUGAS', 'COMPRESSORES%20E%20ACESSÓRIOS',
              'CONTROLE%20DE%20QUALIDADE,%20ENSAIOS%20E%20MEDIÇÃO', 'ELEMENTOS%20DE%20TRANSMISSÃO', 'EMBALAGEM',
              'EQUIPAMENTOS%20A%20LASER', 'FERRAMENTARIA%20E%20MODELAÇÃO', 'FILTROS%20INDUSTRIAIS', 'FORNOS%20E%20ESTUFAS%20INDUSTRIAIS',
              'GRAMPEADORES%20INDUSTRIAIS', 'HIDRÁULICA,%20PNEUMÁTICA%20E%20AUTOMAÇÃO', 'LUBRIFICAÇÃO', 'MÁQUINAS%20PORTÁTEIS',
              'MOINHOS', 'MOTORES', 'MOVIMENTAÇÃO%20E%20ARMAZENAGEM%20', 'PENEIRAS', 'PRESTAÇÃO%20DE%20SERVIÇOS', 'REFRIGERAÇÃO%20INDUSTRIAL',
              'SECADORES%20INDUSTRIAIS', 'SOLDA%20E%20CORTE%20DE%20CHAPAS%20METÁLICAS', 'TROCADORES%20DE%20CALOR', 'TUBULAÇÃO%20INDUSTRIAL',
              'VÁLVULAS%20INDUSTRIAIS', 'VEDAÇÕES', 'VENTILADORES']


# ---------------------------------------------------------------------------------------------------------------------------------

url_inicial = 'http://www.datamaq.org.br/SearchResult/AdditionalFilter?parentId=undefined&sectorName=undefined&isSegment=undefined'
response = get(url_inicial)
html_soup = BeautifulSoup(response.text, 'html.parser')

setores = html_soup.find_all("input", attrs={"onclick" : True})

listas_hash_setores = []
for item1 in setores:
    texto1 = []
    texto1.append(item1['onclick'])
    hash_setor = texto1[0].strip()[17:53].split()
    listas_hash_setores.append(hash_setor)


lista_hash = []
for sublista in listas_hash_setores:
    for item in sublista:
        lista_hash.append(item)


# for i in range(len(lista_hash)):
#     if i==50:
#         lista_hash.remove(lista_hash[i])

# for i in range(len(lista_hash)):
#     print(lista_hash[i])

for i in range(len(nome_setor)-1):
    url = f'http://www.datamaq.org.br/SearchResult/AccountIndustrialSectorList?industrialSectorId={lista_hash[i]}&sectorName={nome_setor[i]}'
    response = get(url)
    html_soup2 = BeautifulSoup(response.text, 'html.parser')

    empresas=html_soup2.find_all("tr",attrs={"onclick" : True})

    for item in empresas:
        texto =[]
        texto.append(item['onclick'])
        hash_empresa_inicial = texto[0].strip().split()
        lista_hash_empresa = []
        for a in range(len(hash_empresa_inicial)):
            if len(hash_empresa_inicial[a]) == 39:
                hash_empresa = hash_empresa_inicial[a][1:-2]
                lista_hash_empresa.append(hash_empresa)
        for k in range(len(lista_hash_empresa)):
            first_nome_empresa = item.td.text
            print(first_nome_empresa)
            nome_empresa = first_nome_empresa.replace(' ', '%20')
            associado = item.text
            if 'Sim' in associado:
                url_dados = f'http://www.datamaq.org.br/SearchResult/ShowManufacturer?sectorId={lista_hash[k]}&sectorName={nome_setor[i]}&entityId={lista_hash_empresa[k]}&entityIDName={nome_empresa}&sourceType=2&industrialInstallationProductId=&isSector=1'
                response = get(url_dados)
                html2_soup= BeautifulSoup(response.text, 'html.parser')
                dados = html2_soup.find_all('div', class_="row")
                setor = dados[0].find('div', class_="col")
                endereco = dados[2].find('div', class_="col")
                cep = dados[3].find('div', class_="col")
                cidade = dados[4].find('div', class_="col")
                estado = dados[5].find('div', class_="col")
                contato = dados[6].find('div', class_="col")
                telefone = dados[7].find('div', class_="col")
                email = dados[8].find('div', class_="col")

                dados_gerais_csv = [first_nome_empresa, setor.span.text, endereco.span.text, cep.span.text, cidade.span.text,
                estado.span.text, contato.span.text, telefone.span.text, email.a.text]
                append_list_as_row('empresas_associadas.csv', dados_gerais_csv)
            else:
                url_dados = f'http://www.datamaq.org.br/SearchResult/ShowManufacturer?sectorId={lista_hash[k]}&sectorName={nome_setor[i]}&entityId={lista_hash_empresa[k]}&entityIDName={nome_empresa}&sourceType=2&industrialInstallationProductId=&isSector=1'
                response = get(url_dados)
                html2_soup= BeautifulSoup(response.text, 'html.parser')
                dados = html2_soup.find_all('div', class_="row")
                setor = dados[0].find('div', class_="col")
                dados_gerais_csv = [first_nome_empresa, setor.span.text]
                append_list_as_row('empresas_nao_associadas.csv', dados_gerais_csv)

print("Raspagem finalizada")


