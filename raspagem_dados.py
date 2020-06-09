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

nome_colunas = ['Nome Empresa', 'Endereço', 'CEP', "Cidade", "Estado", "Nome Contato", "Telefone", "E-mail"]

append_list_as_row('empresas_associadas.csv', nome_colunas)
append_list_as_row('empresas_associadas.csv', nome_colunas[0])

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
			  'CALDEIRAS', 'COMPRESSORES%20E%20ACESSÓRIOS', 'CENTRÍFUGAS', 'COMPRESSORES%20E%20ACESSÓRIOS',
			  'CONTROLE%20DE%20QUALIDADE,%20ENSAIOS%20E%20MEDIÇÃO', 'ELEMENTOS%20DE%20TRANSMISSÃO', 'EMBALAGEM',
			  'EQUIPAMENTOS%20A%20LASER', 'FERRAMENTARIA%20E%20MODELAÇÃO', 'FILTROS%20INDUSTRIAIS', 'FORNOS%20E%20ESTUFAS%20INDUSTRIAIS',
			  'GRAMPEADORES%20INDUSTRIAIS', 'HIDRÁULICA,%20PNEUMÁTICA%20E%20AUTOMAÇÃO', 'LUBRIFICAÇÃO', 'MÁQUINAS%20PORTÁTEIS',
			  'MOINHOS', 'MOTORES', 'MOVIMENTAÇÃO%20E%20ARMAZENAGEM%20', 'PENEIRAS', 'PRESTAÇÃO%20DE%20SERVIÇOS', 'REFRIGERAÇÃO%20INDUSTRIAL',
			  'SECADORES%20INDUSTRIAIS', 'SOLDA%20E%20CORTE%20DE%20CHAPAS%20METÁLICAS', 'TROCADORES%20DE%20CALOR', 'TUBULAÇÃO%20INDUSTRIAL',
			  'VÁLVULAS%20INDUSTRIAIS', 'VEDAÇÕES', 'VENTILADORES']

url_inicial = 'http://www.datamaq.org.br/SearchResult/AdditionalFilter?parentId=undefined&sectorName=undefined&isSegment=undefined'
response = get(url_inicial)
html_soup = BeautifulSoup(response.text, 'html.parser')

setores = html_soup.find_all("input", attrs={"onclick" : True})

for setor in nome_setor:
	for item1 in setores:
		texto1 = []
		texto1.append(item1['onclick'])
		hash_setor = texto1[0].strip()[17:53]

		if hash_setor.startswith('r') or hash_setor.startswith('s'):
			pass

		else:
			url = f'http://www.datamaq.org.br/SearchResult/AccountIndustrialSectorList?industrialSectorId={hash_setor}&sectorName={setor}'
			response = get(url)
			html_soup2 = BeautifulSoup(response.text, 'html.parser')

			empresas=html_soup2.find_all("tr",attrs={"onclick" : True})

			for item in empresas:
				texto =[]
				texto.append(item['onclick'])
				hash_empresa = texto[0].strip()[78:114]
				nome_empresa = item.td.text
				associado = item.text

				if 'Sim' in associado:
					url_dados = f'http://www.datamaq.org.br/SearchResult/ShowManufacturer?sectorId={hash_setor}&sectorName={setor}&entityId={hash_empresa}&entityIDName={nome_empresa}&sourceType=2&industrialInstallationProductId=&isSector=1'
					response = get(url_dados)
					html2_soup= BeautifulSoup(response.text, 'html.parser')
					dados = html2_soup.find_all('div', class_="row")
					for i in range(0, 9):
						dado = dados[i].find('div', class_="col")
						if i==2:
							endereco = dado
						if i==3:
							cep = dado
						if i==4:
							cidade = dado
						if i==5:
							estado = dado
						if i==6:
							contato = dado
						if i==7:
							telefone = dado
						if i==8:
							email = dado
					dados_gerais_csv = [nome_empresa, endereco.span.text, cep.span.text, cidade.span.text,
					estado.span.text, contato.span.text, telefone.span.text, email.a.text]
					append_list_as_row('empresas_associadas.csv', dados_gerais_csv)
				else:
					dados_gerais_csv = [nome_empresa]
					append_list_as_row('empresas_nao_associadas.csv', dados_gerais_csv)
