symptom_choices = [
    ('AN', 'Anosmia (Perda do olfato)'),
    ('CA', 'Cansaço'),
    ('CM', 'Confusão mental'), # Formulário de Maragogi
    ('CN', 'Congestão nasal'),
    ('CJ', 'Conjuntivite'), # Formulário de Maragogi
    ('RN', 'Coriza'),
    ('DI', 'Diarreia'),
    ('SB', 'Dificuldade respiratória'),
    ('ST', 'Dor de garganta'),
    ('DC', 'Dor de cabeça'),
    ('AP', 'Dores no corpo'),
    ('FA', 'Falta de apetite'), # famoso fastio
    ('FV', 'Febre'),
    ('NA', 'Náusea'),
    ('TP', 'Tosse produtiva'),
    ('TS', 'Tosse seca'),
    ('VO', 'Vômitos'),
]

maragogi_symptom_score = {
    'FV': 5,
    'DC': 1,
    'CN': 1,
    'ST': 1,
    'TS': 2,
    'SB': 10,
    'CM': 2,
    'CJ': 1,
    'AN': 3,

}

# Formulário de Maragogi

tests_choices = (
    ('RT', 'RT PCR Covid-19'),
    ('TR', 'Teste Rápido'),
    ('AD', 'Agendado para o dia'),
    ('N', 'Não'),
    ('A', 'Antígeno'),
    ('S', 'Sorologia'),
)

#

intensity_choices = [
    ('', 'Não apresenta'),
    ('L', 'Leve'),
    ('M', 'Moderada'),
    ('H', 'Grave'),
]

gender_choices = [
    ('F', 'Feminino'),
    ('M', 'Masculino'),
    ('N', 'Não quer declarar')
]

address_type_choices = [
    ('HM', 'Residencial'),
    ('WK', 'Trabalho'),
    ('OT', 'Outro'),
]

# drugs = [
#     ('', 'Anti hipertensivo'),
#     ('', 'Imunossupressores'),
#     ('', 'Anti diabéticos'),
#     ('', 'Antibióticos'),
#     ('', 'Corticoide'),
#     ('', 'Anti inflamatório')
# ]

comorbidity_choices = [
    ('Y', 'Artrite reumatóide'),        # 0
    ('A', 'Asma'),                      # 1
    ('C', 'Bronquite crônica'),         # 2
    ('N', 'Câncer'),                    # 3
    ('E', 'Demência'),                  # 4
    ('D', 'Diabetes'),                  # 5
    ('H', 'Doença cardíacas'),          # 6
    ('L', 'Doença crônica no fígado'),  # 7
    ('R', 'Doença renal crônica'),      # 8
    ('W', 'Doenças reumáticas'),        # 9
    ('P', 'Doença pulmonar crônica'),   # 10
    ('I', 'Imunosuprimido'),            # 11
    ('T', 'Hipertensão'),               # 12
    ('V', 'HIV+'),                      # 13
    ('B', 'Obesidade'),                 # 14
    ('U', 'Portador de Lúpus'),         # 15
    ('F', 'Gestação de risco'),         # 16
    ('G', 'Cromossômica')               # 17
]

country_choices = [
    ('AFE', 'Afeganistão'),
    ('AFR', 'África do Sul'),
    ('AUS', 'Áustria'),
    ('ALB', 'Albânia'),
    ('ALE', 'Alemanha'),
    ('AND', 'Andorra'),
    ('ANG', 'Angola'),
    ('ANT', 'Antígua e Barbuda'),
    ('ARG', 'Argentina'),
    ('ARL', 'Argélia'),
    ('ARM', 'Armênia'),
    ('ARA', 'Arábia Saudita'),
    ('AUL', 'Austrália'),
    ('AZE', 'Azerbaijão'),
    ('BAH', 'Bahamas'),
    ('BAN', 'Bangladesh'),
    ('BAR', 'Barbados'),
    ('BAM', 'Barém'),
    ('BEL', 'Belize'),
    ('BEN', 'Benin'),
    ('BIE', 'Bielorrússia'),
    ('BOL', 'Bolívia'),
    ('BOT', 'Botsuana'),
    ('BRA', 'Brasil'),
    ('BRU', 'Brunei Darussalam'),
    ('BUL', 'Bulgária'),
    ('BUR', 'Burkina Faso'),
    ('BUD', 'Burundi'),
    ('BUT', 'Butão'),
    ('BEG', 'Bélgica'),
    ('BOS', 'Bósnia e Herzegovina'),
    ('CAB', 'Cabo Verde'),
    ('CAM', 'Camarões'),
    ('CAJ', 'Camboja'),
    ('CAN', 'Canadá'),
    ('CAT', 'Catar'),
    ('CAZ', 'Cazaquistão'),
    ('CHA', 'Chade'),
    ('CHL', 'Chile'),
    ('CHI', 'China'),
    ('CHP', 'Chipre'),
    ('CIN', 'Cingapura'),
    ('COL', 'Colômbia'),
    ('COM', 'Comores'),
    ('CON', 'Congo'),
    ('COS', 'Costa Rica'),
    ('COT', 'Costa do Marfim'),
    ('CRO', 'Croácia'),
    ('CUB', 'Cuba'),
    ('CZE', 'Czechia'),
    ('DIN', 'Dinamarca'),
    ('DJI', 'Djibuti'),
    ('DOM', 'Dominica'),
    ('EGI', 'Egito'),
    ('ELS', 'El Salvador'),
    ('EMI', 'Emirados Árabes Unidos'),
    ('EQU', 'Equador'),
    ('ERI', 'Eritreia'),
    ('ESL', 'Eslováquia'),
    ('ESV', 'Eslovênia'),
    ('ESP', 'Espanha'),
    ('EST', 'Estados Unidos da America'),
    ('ESN', 'Estônia'),
    ('ESW', 'Eswatini'),
    ('ETI', 'Etiópia'),
    ('FED', 'Federação Russa'),
    ('FIJ', 'Fiji'),
    ('FIL', 'Filipinas'),
    ('FIN', 'Finlândia'),
    ('FRA', 'França'),
    ('GAB', 'Gabão'),
    ('GAN', 'Gana'),
    ('GAM', 'Gâmbia'),
    ('GEO', 'Geórgia'),
    ('GRA', 'Granada'),
    ('GRÉ', 'Grécia'),
    ('GUA', 'Guatemala'),
    ('GUI', 'Guiana'),
    ('GUN', 'Guiné'),
    ('GUE', 'Guiné Equatorial'),
    ('GUB', 'Guiné-Bissau'),
    ('HAI', 'Haiti'),
    ('HON', 'Honduras'),
    ('HUN', 'Hungria'),
    ('IND', 'Índia'),
    ('ILC', 'Ilhas Cook'),
    ('ILM', 'Ilhas Marshall'),
    ('ILS', 'Ilhas Salomão'),
    ('INN', 'Indonésia'),
    ('IRQ', 'Iraque'),
    ('IRL', 'Irlanda'),
    ('IRA', 'Irã'),
    ('ISL', 'Islândia'),
    ('ISR', 'Israel'),
    ('ITA', 'Itália'),
    ('IEM', 'Iémen'),
    ('JAM', 'Jamaica'),
    ('JAP', 'Japão'),
    ('JOR', 'Jordânia'),
    ('KIR', 'Kiribati'),
    ('KUW', 'Kuwait'),
    ('LES', 'Lesoto'),
    ('LET', 'Letônia'),
    ('LIB', 'Libéria'),
    ('LIT', 'Lituânia'),
    ('LUX', 'Luxemburgo'),
    ('LIB', 'Líbano'),
    ('LIA', 'Líbia'),
    ('MAC', 'Macedônia do Norte'),
    ('MAD', 'Madagáscar'),
    ('MAW', 'Malawi'),
    ('MAD', 'Maldivas'),
    ('MAL', 'Mali'),
    ('MAT', 'Malta'),
    ('MAS', 'Malásia'),
    ('MAR', 'Marrocos'),
    ('MAU', 'Mauritânia'),
    ('MAR', 'Maurícia'),
    ('MIC', 'Micronésia'),
    ('MON', 'Mongólia'),
    ('MOT', 'Montenegro'),
    ('MOC', 'Moçambique'),
    ('MYA', 'Myanmar'),
    ('MEX', 'México'),
    ('MOO', 'Mônaco'),
    ('NAM', 'Namíbia'),
    ('NAU', 'Nauru'),
    ('NEP', 'Nepal'),
    ('NIC', 'Nicarágua'),
    ('NIG', 'Nigéria'),
    ('NIG', 'Níger'),
    ('NIU', 'Niue'),
    ('NOR', 'Noruega'),
    ('NOV', 'Nova Zelândia'),
    ('OMA', 'Omã'),
    ('PAL', 'Palau'),
    ('PAN', 'Panamá'),
    ('PAP', 'Papua Nova Guiné'),
    ('PAQ', 'Paquistão'),
    ('PAR', 'Paraguai'),
    ('PAI', 'Países Baixos'),
    ('PER', 'Peru'),
    ('POL', 'Polônia'),
    ('POR', 'Portugal'),
    ('QUI', 'Quirguistão'),
    ('QUE', 'Quênia'),
    ('REI', 'Reino Unido'),
    ('REP', 'República Centro-Africana'),
    ('RED', 'República Democrática Popular do Laos'),
    ('RDC', 'República Democrática do Congo'),
    ('RDM', 'República Dominicana'),
    ('RPD', 'República Popular Democrática da Coreia'),
    ('RET', 'República Togolesa'),
    ('RUT', 'República Unida da Tanzânia'),
    ('RCA', 'República da Coreia'),
    ('REM', 'República da Moldávia'),
    ('RAS', 'República Árabe da Síria'),
    ('ROM', 'Romênia'),
    ('RUA', 'Ruanda'),
    ('SAM', 'Samoa'),
    ('SMO', 'San Marino'),
    ('SAN', 'Santa Lúcia'),
    ('SEN', 'Senegal'),
    ('SER', 'Serra Leoa'),
    ('SEY', 'Seychelles'),
    ('SOM', 'Somália'),
    ('SRI', 'Sri Lanka'),
    ('SUD', 'Sudão'),
    ('SUS', 'Sudão do Sul'),
    ('SUR', 'Suriname'),
    ('SUE', 'Suécia'),
    ('SUI', 'Suíça'),
    ('SAC', 'São Cristóvão e Nevis'),
    ('SAT', 'São Tomé e Príncipe'),
    ('SAV', 'São Vicente e Granadinas'),
    ('SEV', 'Sérvia'),
    ('TAI', 'Tailândia'),
    ('TAJ', 'Tajiquistão'),
    ('TIM', 'Timor-Leste'),
    ('TON', 'Tonga'),
    ('TRI', 'Trindade e Tobago'),
    ('TUN', 'Tunísia'),
    ('TUR', 'Turquemenistão'),
    ('TUQ', 'Turquia'),
    ('TUV', 'Tuvalu'),
    ('UCR', 'Ucrânia'),
    ('UGA', 'Uganda'),
    ('URU', 'Uruguai'),
    ('USB', 'Usbequistão'),
    ('VAN', 'Vanuatu'),
    ('VEN', 'Venezuela'),
    ('VIE', 'Vietnã'),
    ('ZIM', 'Zimbábue'),
    ('ZAM', 'Zâmbia'),
]

exposure_choices = [
    ('confirmed_cases', 'Contato com casos confirmados nos últimos 14 dias'),
    ('suspect_cases', 'Contato com casos suspeitos nos últimos 14 dias'),
    ('foreign', 'Contato com pessoas que estiveram em locais com casos confirmados'),
]

result_choices = [
    ('SR', 'Sem resultado'),
    ('PO', 'Positivo'),
    ('NE', 'Negativo'),
    ('IN', 'Inconclusivo'),
]

status_choices = (
    ('I', 'Imune'),
    ('N', 'Normal'),
    ('H', 'Hospitalizado'),
    ('U', 'UTI'),
    ('R', 'Recuperado'),
    ('M', 'Morto'),
)

action_choices = (
    ('C','CREATE'),
    ('D','DELETE'),
    ('U','UPDATE'),
)

model_choices = (
    ('PR','PROFILE'),
    ('AD','ADDRESS'),
    ('MO','MONITORING'),
    ('SY','SYMPTOM'),
    ('TR','TRIP'),
    ('RE','REQUEST'),
    ('HC', 'HEALTH CARE STATUS')
)

state_choices = (
    ('AL', 'Alagoas'),
    ('PE', 'Pernambuco'),
    ('GO', 'Goiás')
)

city_choices = (
    ('ALTO PARAISO DE GOIAS', 'ALTO PARAISO DE GOIAS'),
	('MACEIO', 'MACEIO'),
	('IBIMIRIM', 'IBIMIRIM'),
	('PALMEIRA DOS INDIOS', 'PALMEIRA DOS INDIOS'),
	('CABO DE SANTO AGOSTINHO', 'CABO DE SANTO AGOSTINHO'),
	('CARUARU', 'CARUARU'),
	('MATRIZ DE CAMARAGIBE', 'MATRIZ DE CAMARAGIBE'),
	('PETROLINA', 'PETROLINA'),
	('ARAPIRACA', 'ARAPIRACA'),
	('ILHA DE ITAMARACA', 'ILHA DE ITAMARACA'),
	('ALIANCA', 'ALIANCA'),
	('PAUDALHO', 'PAUDALHO'),
	('GRAVATA', 'GRAVATA'),
	('FLORES', 'FLORES'),
	('INAJA', 'INAJA'),
	('SAIRE', 'SAIRE'),
	('POCO DAS TRINCHEIRAS', 'POCO DAS TRINCHEIRAS'),
	('PORTO CALVO', 'PORTO CALVO'),
	('PORTO DE PEDRAS', 'PORTO DE PEDRAS'),
	('PAULISTA', 'PAULISTA'),
	('AFOGADOS DA INGAZEIRA', 'AFOGADOS DA INGAZEIRA'),
	('DELMIRO GOUVEIA', 'DELMIRO GOUVEIA'),
	('LIMOEIRO DE ANADIA', 'LIMOEIRO DE ANADIA'),
	('FLORESTA', 'FLORESTA'),
	('SERRA TALHADA', 'SERRA TALHADA'),
	('PIRANHAS', 'PIRANHAS'),
	('GLORIA DO GOITA', 'GLORIA DO GOITA'),
	('PORTO REAL DO COLEGIO', 'PORTO REAL DO COLEGIO'),
	('QUEBRANGULO', 'QUEBRANGULO'),
	('JABOATAO DOS GUARARAPES', 'JABOATAO DOS GUARARAPES'),
	('QUIPAPA', 'QUIPAPA'),
	('GARANHUNS', 'GARANHUNS'),
	('AFRANIO', 'AFRANIO'),
	('AGUA BRANCA', 'AGUA BRANCA'),
	('DOIS RIACHOS', 'DOIS RIACHOS'),
	('CACIMBINHAS', 'CACIMBINHAS'),
	('JEQUIA DA PRAIA', 'JEQUIA DA PRAIA'),
	('RECIFE', 'RECIFE'),
	('SANTA MARIA DO CAMBUCA', 'SANTA MARIA DO CAMBUCA'),
	('AGUAS BELAS', 'AGUAS BELAS'),
	('BUENOS AIRES', 'BUENOS AIRES'),
	('SANTA MARIA DA BOA VISTA', 'SANTA MARIA DA BOA VISTA'),
	('IPOJUCA', 'IPOJUCA'),
	('JUPI', 'JUPI'),
	('FREI MIGUELINHO', 'FREI MIGUELINHO'),
	('LIMOEIRO', 'LIMOEIRO'),
	('VICENCIA', 'VICENCIA'),
	('CUPIRA', 'CUPIRA'),
	('PANELAS', 'PANELAS'),
	('JATAUBA', 'JATAUBA'),
	('CHA DE ALEGRIA', 'CHA DE ALEGRIA'),
	('TRACUNHAEM', 'TRACUNHAEM'),
	('SALGADINHO', 'SALGADINHO'),
	('LAGOA DO OURO', 'LAGOA DO OURO'),
	('CASINHAS', 'CASINHAS'),
	('IATI', 'IATI'),
	('NAZARE DA MATA', 'NAZARE DA MATA'),
	('VERTENTE DO LERIO', 'VERTENTE DO LERIO'),
	('ITAMBE', 'ITAMBE'),
	('CATENDE', 'CATENDE'),
	('CAPOEIRAS', 'CAPOEIRAS'),
	('MACHADOS', 'MACHADOS'),
	('CARNAUBEIRA DA PENHA', 'CARNAUBEIRA DA PENHA'),
	('LAGOA DOS GATOS', 'LAGOA DOS GATOS'),
	('BONITO', 'BONITO'),
	('FLEXEIRAS', 'FLEXEIRAS'),
	('SATUBA', 'SATUBA'),
	('SAO JOAO', 'SAO JOAO'),
	('SANTA TEREZINHA', 'SANTA TEREZINHA'),
	('OURICURI', 'OURICURI'),
	('BOM CONSELHO', 'BOM CONSELHO'),
	('PASSO DE CAMARAGIBE', 'PASSO DE CAMARAGIBE'),
	('CARNAIBA', 'CARNAIBA'),
	('JATOBA', 'JATOBA'),
	('VENTUROSA', 'VENTUROSA'),
	('CAMPESTRE', 'CAMPESTRE'),
	('IGARASSU', 'IGARASSU'),
	('GRANITO', 'GRANITO'),
	('JAQUEIRA', 'JAQUEIRA'),
	('GOIANA', 'GOIANA'),
	('ABREU E LIMA', 'ABREU E LIMA'),
	('CORTES', 'CORTES'),
	('VITORIA DE SANTO ANTAO', 'VITORIA DE SANTO ANTAO'),
	('SAO JOSE DA COROA GRANDE', 'SAO JOSE DA COROA GRANDE'),
	('COITE DO NOIA', 'COITE DO NOIA'),
	('SAO LUIS DO QUITUNDE', 'SAO LUIS DO QUITUNDE'),
	('SAO MIGUEL DOS CAMPOS', 'SAO MIGUEL DOS CAMPOS'),
	('JOAO ALFREDO', 'JOAO ALFREDO'),
	('PENEDO', 'PENEDO'),
	('MARAGOGI', 'MARAGOGI'),
	('RIACHO DAS ALMAS', 'RIACHO DAS ALMAS'),
	('POCAO', 'POCAO'),
	('CARPINA', 'CARPINA'),
	('BELO JARDIM', 'BELO JARDIM'),
	('BOCA DA MATA', 'BOCA DA MATA'),
	('BARRA DE SAO MIGUEL', 'BARRA DE SAO MIGUEL'),
	('MATA GRANDE', 'MATA GRANDE'),
	('CORURIPE', 'CORURIPE'),
	('BARRA DE SANTO ANTONIO', 'BARRA DE SANTO ANTONIO'),
	('BODOCO', 'BODOCO'),
	('PALMARES', 'PALMARES'),
	('SAO LOURENCO DA MATA', 'SAO LOURENCO DA MATA'),
	('PRIMAVERA', 'PRIMAVERA'),
	('RIO FORMOSO', 'RIO FORMOSO'),
	('POMBOS', 'POMBOS'),
	('MOREILANDIA', 'MOREILANDIA'),
	('PESQUEIRA', 'PESQUEIRA'),
	('FELIZ DESERTO', 'FELIZ DESERTO'),
	('TRINDADE', 'TRINDADE'),
	('LAJEDO', 'LAJEDO'),
	('VICOSA', 'VICOSA'),
	('PAULO JACINTO', 'PAULO JACINTO'),
	('PIACABUCU', 'PIACABUCU'),
	('PILAR', 'PILAR'),
	('PINDOBA', 'PINDOBA'),
	('BEZERROS', 'BEZERROS'),
	('LAGOA DO CARRO', 'LAGOA DO CARRO'),
	('SURUBIM', 'SURUBIM'),
	('ARARIPINA', 'ARARIPINA'),
	('PARANATAMA', 'PARANATAMA'),
	('TUPANATINGA', 'TUPANATINGA'),
	('PAO DE ACUCAR', 'PAO DE ACUCAR'),
	('SAO JOSE DO EGITO', 'SAO JOSE DO EGITO'),
	('DORMENTES', 'DORMENTES'),
	('MANARI', 'MANARI'),
	('SANTA CRUZ DO CAPIBARIBE', 'SANTA CRUZ DO CAPIBARIBE'),
	('BREJO DA MADRE DE DEUS', 'BREJO DA MADRE DE DEUS'),
	('ARCOVERDE', 'ARCOVERDE'),
	('OLINDA', 'OLINDA'),
	('OLHO DAGUA DAS FLORES', 'OLHO DAGUA DAS FLORES'),
	('CAJUEIRO', 'CAJUEIRO'),
	('BUIQUE', 'BUIQUE'),
	('SANTA FILOMENA', 'SANTA FILOMENA'),
	('XEXEU', 'XEXEU'),
	('IPUBI', 'IPUBI'),
	('CAMARAGIBE', 'CAMARAGIBE'),
	('MESSIAS', 'MESSIAS'),
	('EXU', 'EXU'),
	('TEREZINHA', 'TEREZINHA'),
	('OROBO', 'OROBO'),
	('TABIRA', 'TABIRA'),
	('CONDADO', 'CONDADO'),
	('ITAPETIM', 'ITAPETIM'),
	('SALGUEIRO', 'SALGUEIRO'),
	('ESCADA', 'ESCADA'),
	('LAGOA DO ITAENGA', 'LAGOA DO ITAENGA'),
	('PETROLANDIA', 'PETROLANDIA'),
	('COLONIA LEOPOLDINA', 'COLONIA LEOPOLDINA'),
	('SERTANIA', 'SERTANIA'),
	('BELO MONTE', 'BELO MONTE'),
	('MURICI', 'MURICI'),
	('BRANQUINHA', 'BRANQUINHA'),
	('FEIRA NOVA', 'FEIRA NOVA'),
	('RIO LARGO', 'RIO LARGO'),
	('CANHOTINHO', 'CANHOTINHO'),
	('JACARE DOS HOMENS', 'JACARE DOS HOMENS'),
	('JUREMA', 'JUREMA'),
	('MARIBONDO', 'MARIBONDO'),
	('SALOA', 'SALOA'),
	('RIBEIRAO', 'RIBEIRAO'),
	('CUMARU', 'CUMARU'),
	('CABROBO', 'CABROBO'),
	('CHA GRANDE', 'CHA GRANDE'),
	('PASSIRA', 'PASSIRA'),
	('TEOTONIO VILELA', 'TEOTONIO VILELA'),
	('SAO BENTO DO UNA', 'SAO BENTO DO UNA'),
	('AGRESTINA', 'AGRESTINA'),
	('BELEM DE MARIA', 'BELEM DE MARIA'),
	('TRIUNFO', 'TRIUNFO'),
	('TAQUARANA', 'TAQUARANA'),
	('MORENO', 'MORENO'),
	('SAO CAITANO', 'SAO CAITANO'),
	('TIMBAUBA', 'TIMBAUBA'),
	('SAO JOSE DA TAPERA', 'SAO JOSE DA TAPERA'),
	('CAETES', 'CAETES'),
	('CAMPO ALEGRE', 'CAMPO ALEGRE'),
	('BREJAO', 'BREJAO'),
	('CALCADO', 'CALCADO'),
	('CUSTODIA', 'CUSTODIA'),
	('BARRA DE GUABIRABA', 'BARRA DE GUABIRABA'),
	('AGUA PRETA', 'AGUA PRETA'),
	('ATALAIA', 'ATALAIA'),
	('LAGOA DA CANOA', 'LAGOA DA CANOA'),
	('ANGELIM', 'ANGELIM'),
	('TORITAMA', 'TORITAMA'),
	('SANTANA DO IPANEMA', 'SANTANA DO IPANEMA'),
	('SANTANA DO MUNDAU', 'SANTANA DO MUNDAU'),
	('OLIVENCA', 'OLIVENCA'),
	('SERRITA', 'SERRITA'),
	('OURO BRANCO', 'OURO BRANCO'),
	('FERREIROS', 'FERREIROS'),
	('SAO BRAS', 'SAO BRAS'),
	('MARECHAL DEODORO', 'MARECHAL DEODORO'),
	('BOM JARDIM', 'BOM JARDIM'),
	('TERRA NOVA', 'TERRA NOVA'),
	('SANTA CRUZ DA BAIXA VERDE', 'SANTA CRUZ DA BAIXA VERDE'),
	('JUNQUEIRO', 'JUNQUEIRO'),
	('LAGOA GRANDE', 'LAGOA GRANDE'),
	('ESTRELA DE ALAGOAS', 'ESTRELA DE ALAGOAS'),
	('ANADIA', 'ANADIA'),
	('PARICONHA', 'PARICONHA'),
	('TRAIPU', 'TRAIPU'),
	('IGREJA NOVA', 'IGREJA NOVA'),
	('UNIAO DOS PALMARES', 'UNIAO DOS PALMARES'),
	('CALUMBI', 'CALUMBI'),
	('TUPARETAMA', 'TUPARETAMA'),
	('CEDRO', 'CEDRO'),
	('CORRENTES', 'CORRENTES'),
	('ALAGOINHA', 'ALAGOINHA'),
	('SAO JOAQUIM DO MONTE', 'SAO JOAQUIM DO MONTE'),
	('PEDRA', 'PEDRA'),
	('AMARAJI', 'AMARAJI'),
	('BARREIROS', 'BARREIROS'),
	('CAMUTANGA', 'CAMUTANGA'),
	('TAMANDARE', 'TAMANDARE'),
	('BATALHA', 'BATALHA'),
	('MACAPARANA', 'MACAPARANA'),
	('CARNEIROS', 'CARNEIROS'),
	('TACARATU', 'TACARATU'),
	('IBIRAJUBA', 'IBIRAJUBA'),
	('SENADOR RUI PALMEIRA', 'SENADOR RUI PALMEIRA'),
	('SAO JOSE DA LAJE', 'SAO JOSE DA LAJE'),
	('ITAQUITINGA', 'ITAQUITINGA'),
	('SAO VICENTE FERRER', 'SAO VICENTE FERRER'),
	('BREJINHO', 'BREJINHO'),
	('INGAZEIRA', 'INGAZEIRA'),
	('MINADOR DO NEGRAO', 'MINADOR DO NEGRAO'),
	('VERDEJANTE', 'VERDEJANTE'),
	('MONTEIROPOLIS', 'MONTEIROPOLIS'),
	('INHAPI', 'INHAPI'),
	('SAO MIGUEL DOS MILAGRES', 'SAO MIGUEL DOS MILAGRES'),
	('ITAIBA', 'ITAIBA'),
	('ITAPISSUMA', 'ITAPISSUMA'),
	('MAJOR ISIDORO', 'MAJOR ISIDORO'),
	('VERTENTES', 'VERTENTES'),
	('CAMOCIM DE SAO FELIX', 'CAMOCIM DE SAO FELIX'),
	('TACAIMBO', 'TACAIMBO'),
	('OROCO', 'OROCO'),
	('QUIXABA', 'QUIXABA'),
	('SANTA CRUZ', 'SANTA CRUZ'),
	('SAO SEBASTIAO', 'SAO SEBASTIAO'),
	('BELEM DE SAO FRANCISCO', 'BELEM DE SAO FRANCISCO'),
	('SAO BENEDITO DO SUL', 'SAO BENEDITO DO SUL'),
	('CACHOEIRINHA', 'CACHOEIRINHA'),
	('ARACOIABA', 'ARACOIABA'),
	('COQUEIRO SECO', 'COQUEIRO SECO'),
	('JAPARATINGA', 'JAPARATINGA'),
	('GIRAU DO PONCIANO', 'GIRAU DO PONCIANO'),
	('SANHARO', 'SANHARO'),
	('SOLIDAO', 'SOLIDAO'),
	('FERNANDO DE NORONHA', 'FERNANDO DE NORONHA'),
	('MAR VERMELHO', 'MAR VERMELHO'),
	('SIRINHAEM', 'SIRINHAEM'),
	('SAO JOSE DO BELMONTE', 'SAO JOSE DO BELMONTE'),
	('JUCATI', 'JUCATI'),
	('BETANIA', 'BETANIA'),
	('IGACI', 'IGACI'),
	('JOAQUIM NABUCO', 'JOAQUIM NABUCO'),
	('ALTINHO', 'ALTINHO'),
	('MIRANDIBA', 'MIRANDIBA'),
	('ITACURUBA', 'ITACURUBA'),
	('CRAIBAS', 'CRAIBAS'),
	('CAMPO GRANDE', 'CAMPO GRANDE'),
	('PALMEIRINA', 'PALMEIRINA'),
	('IBATEGUARA', 'IBATEGUARA'),
	('MARAVILHA', 'MARAVILHA'),
	('GAMELEIRA', 'GAMELEIRA'),
	('JOAQUIM GOMES', 'JOAQUIM GOMES'),
	('MARAIAL', 'MARAIAL'),
	('CAPELA', 'CAPELA'),
	('JUNDIA', 'JUNDIA'),
	('CANAPI', 'CANAPI'),
	('NOVO LINO', 'NOVO LINO'),
	('PARIPUEIRA', 'PARIPUEIRA'),
	('TAQUARITINGA DO NORTE', 'TAQUARITINGA DO NORTE'),
	('PARNAMIRIM', 'PARNAMIRIM'),
	('IGUARACI', 'IGUARACI'),
	('ROTEIRO', 'ROTEIRO'),
	('SANTA LUZIA DO NORTE', 'SANTA LUZIA DO NORTE'),
	('CHA PRETA', 'CHA PRETA'),
	('PALESTINA', 'PALESTINA'),
	('OLHO DAGUA GRANDE', 'OLHO DAGUA GRANDE'),
	('FEIRA GRANDE', 'FEIRA GRANDE'),
	('TANQUE DARCA', 'TANQUE DARCA'),
	('OLHO DAGUA DO CASADO', 'OLHO DAGUA DO CASADO'),
	('JACUIPE', 'JACUIPE'),
	('JARAMATAIA', 'JARAMATAIA'),
	('BELEM', 'BELEM'),
)

ethnicity_choices = (
    ('A', 'Amarela'),
    ('B', 'Branca'),
    ('I', 'Indígena'),
    ('P', 'Parda'),
    ('p', 'Preta'),
)

pregnancy_choices = (
    ('1', '1º trimestre'),
    ('2', '2º trimestre'),
    ('3', '3º trimestre'),
    ('4', 'Idade gestacional ignorada'),
    ('5', 'Não'),
    ('6', 'Não se aplica'),
)

schooling_choices = (
    ('0', 'Sem escolaridade/analfabeto'),
    ('1', 'Fundamental 1º ciclo (1ª a 5ª série)'),
    ('2', 'Fundamental 2º ciclo (6ª a 9ª série)'),
    ('3', 'Médio (1º ao 3º ano'),
    ('4', 'Superior'),
    ('5', 'Não se aplica'),
)

zone_choices = (
    ('1', 'Urbana'),
    ('2', 'Rural'),
    ('3', 'Periurbana'),
)

maragogi_symptoms_choices = (
    ('1', 'Febre'),
    ('2', 'Tosse'),
    ('3', 'Dor de garganta'),
    ('4', 'Dispneia'),
    ('5', 'Desconforto respiratório'),
    ('6', 'Saturação O2 < 95%'),
    ('7', 'Diarreia'),
    ('8', 'Vômito'),
)

maragogi_comorbidities_choices = (
    ('1', 'Puérpera (até 45 dias do parto)'),
    ('2', 'Síndrome de Down'),
    ('3', 'Diabetes mellitus'),
    ('4', 'Imunodeficiência/Imunodepressão'),
    ('5', 'Doença cardiovascular crônica'),
    ('6', 'Doença hepática crônica'),
    ('7', 'Doença neurológica crônica'),
    ('8', 'Doença renal crônica'),
    ('9', 'Doença Hematológica crônica'),
    ('a', 'Asma'),
    ('b', 'Outra pneumopatia crônica', 0),
    ('c', 'Obesidade'),
    ('d', 'Outro'),
)

antiviral_choices = (
    ('1', 'Oseltamivir'),
    ('2', 'Zanamivir'),
    ('3', 'Outro'),
)

ventilatory_support_choices = (
    ('1', 'Sim, invasivo'),
    ('2', 'Sim, não invasivo'),
    ('3', 'Não'),
)

chest_x_ray_choices = (
    ('1', 'Normal'),
    ('2', 'Infiltrado intersticial'),
    ('3', 'Consolidação'),
    ('4', 'Misto'),
    ('5', 'Outro'),
    ('6', 'Não realizado'),
)

sample_type_choices = (
    ('1', 'Secreção de Naso-orofaringe'),
    ('2', 'Lavado Broco-alveolar'),
    ('3', 'Tecido post-mortem'),
    ('4', 'Outro'),
)

if_result_choices = (
    ('1', 'Positivo'),
    ('2', 'Negativo'),
    ('3', 'Inconclusivo'),
    ('4', 'Não realizado'),
    ('5', 'Aguardando resultado'),
)

influenza_result_choices = (
    ('1', 'Positivo para influenza A'),
    ('2', 'Positivo para influenza B'),
    ('3', 'Negativo'),
)

if_other_respiratory_viruses_choices = (
    ('1', 'Vírus sincicial respiratório'),
    ('2', 'Parainfluenza 1'),
    ('3', 'Parainfluenza 2'),
    ('4', 'Parainfluenza 3'),
    ('5', 'Adenovírus'),
)

rt_pcr_result_choices = (
    ('1', 'Detectável'),
    ('2', 'Não detectável'),
    ('3', 'Inconclusivo'),
    ('4', 'Não realizado'),
    ('5', 'Aguardando resultado'),
)

rt_pcr_influenza_a_subtype_choices = (
    ('1', 'Influenza A (H1N1) pdm09'),
    ('2', 'Influenza A/H3N2'),
    ('3', 'Influenza A não subtipado'),
    ('4', 'Influenza A não subtipável'),
    ('5', 'Inconclusivo'),
    ('6', 'Outro'),
)

rt_pcr_influenza_b_lineage_choices = (
    ('1', 'Victoria'),
    ('2', 'Yamagatha'),
    ('3', 'Não realizado'),
    ('4', 'Inconclusivo'),
    ('5', 'Outro'),
)

rt_pcr_other_respiratory_viruses_choices = (
    ('1', 'Vírus sincicial respiratório'),
    ('2', 'Parainfluenza 1'),
    ('3', 'Parainfluenza 2'),
    ('4', 'Parainfluenza 3'),
    ('5', 'Parainfluenza 4'),
    ('6', 'Adenovírus'),
    ('7', 'Metapneumovírus'),
    ('8', 'Bocavírus'),
    ('9', 'Rinovírus'),
    ('A', 'Outro vírus respiratório')
)

final_classification_choices = (
    ('1', 'SRAG por influenza'),
    ('2', 'SRAG por outro vírus respiratório'),
    ('3', 'Outro'),
    ('4', 'SRAG não especificado'),
)

closure_criteria_choices = (
    ('1', 'Laboratorial'),
    ('2', 'Vínculo-Epidemiológico'),
    ('3', 'Clínico'),
)

case_evolution_choices = (
    ('1', 'Cura'),
    ('2', 'Óbito'),
)

medical_referral_choices = (
#    ('1', 'Internado'),
    ('2', 'Isolamento'),
    ('3', 'Não está doente'),
)

medical_referral_status_choices = (
    ('1', 'Casa'),
#    ('2', 'Leito comum'),
#    ('3', 'UTI'),
)

hospitalization_choices = (
    ('2', 'Leito comum'),
    ('3', 'UTI'),
)

prescription_choices = (
    ('1', 'Anitta'),
    ('2', 'Antibiótico de cobertura'),
    ('3', 'Antitérmico'),
    ('4', 'Entubação'),
    ('5', 'Hidroxicloroquina/Azitromicina'),
    ('6', 'Ivermectina'),
    ('7', 'Tamiflu'),
    ('8', 'Ventilação'),
    ('9', 'Outro(s)'),
)

profession_choices = (
    ('', 'Nenhuma'),
)