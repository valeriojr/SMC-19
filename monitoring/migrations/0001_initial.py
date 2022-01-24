# Generated by Django 3.0.4 on 2020-05-07 16:58

import bitfield.models
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('prediction', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('primary', models.BooleanField(blank=True, default=False, verbose_name='Principal')),
                ('type', models.CharField(blank=True, choices=[('HM', 'Residencial'), ('WK', 'Trabalho'), ('OT', 'Outro')], default='', max_length=2, verbose_name='Tipo')),
                ('postal_code', models.CharField(blank=True, default='', max_length=8, verbose_name='CEP')),
                ('neighbourhood', models.CharField(blank=True, default='', max_length=100, verbose_name='Bairro')),
                ('street_name', models.CharField(blank=True, default='', max_length=100, verbose_name='Logradouro')),
                ('number', models.PositiveIntegerField(blank=True, default=0, null=True, verbose_name='Número')),
                ('complement', models.CharField(blank=True, default='', max_length=100, verbose_name='Complemento')),
                ('city', models.CharField(choices=[('MACEIO', 'MACEIO'), ('IBIMIRIM', 'IBIMIRIM'), ('PALMEIRA DOS INDIOS', 'PALMEIRA DOS INDIOS'), ('CABO DE SANTO AGOSTINHO', 'CABO DE SANTO AGOSTINHO'), ('CARUARU', 'CARUARU'), ('MATRIZ DE CAMARAGIBE', 'MATRIZ DE CAMARAGIBE'), ('PETROLINA', 'PETROLINA'), ('ARAPIRACA', 'ARAPIRACA'), ('ILHA DE ITAMARACA', 'ILHA DE ITAMARACA'), ('ALIANCA', 'ALIANCA'), ('PAUDALHO', 'PAUDALHO'), ('GRAVATA', 'GRAVATA'), ('FLORES', 'FLORES'), ('INAJA', 'INAJA'), ('SAIRE', 'SAIRE'), ('POCO DAS TRINCHEIRAS', 'POCO DAS TRINCHEIRAS'), ('PORTO CALVO', 'PORTO CALVO'), ('PORTO DE PEDRAS', 'PORTO DE PEDRAS'), ('PAULISTA', 'PAULISTA'), ('AFOGADOS DA INGAZEIRA', 'AFOGADOS DA INGAZEIRA'), ('DELMIRO GOUVEIA', 'DELMIRO GOUVEIA'), ('LIMOEIRO DE ANADIA', 'LIMOEIRO DE ANADIA'), ('FLORESTA', 'FLORESTA'), ('SERRA TALHADA', 'SERRA TALHADA'), ('PIRANHAS', 'PIRANHAS'), ('GLORIA DO GOITA', 'GLORIA DO GOITA'), ('PORTO REAL DO COLEGIO', 'PORTO REAL DO COLEGIO'), ('QUEBRANGULO', 'QUEBRANGULO'), ('JABOATAO DOS GUARARAPES', 'JABOATAO DOS GUARARAPES'), ('QUIPAPA', 'QUIPAPA'), ('GARANHUNS', 'GARANHUNS'), ('AFRANIO', 'AFRANIO'), ('AGUA BRANCA', 'AGUA BRANCA'), ('DOIS RIACHOS', 'DOIS RIACHOS'), ('CACIMBINHAS', 'CACIMBINHAS'), ('JEQUIA DA PRAIA', 'JEQUIA DA PRAIA'), ('RECIFE', 'RECIFE'), ('SANTA MARIA DO CAMBUCA', 'SANTA MARIA DO CAMBUCA'), ('AGUAS BELAS', 'AGUAS BELAS'), ('BUENOS AIRES', 'BUENOS AIRES'), ('SANTA MARIA DA BOA VISTA', 'SANTA MARIA DA BOA VISTA'), ('IPOJUCA', 'IPOJUCA'), ('JUPI', 'JUPI'), ('FREI MIGUELINHO', 'FREI MIGUELINHO'), ('LIMOEIRO', 'LIMOEIRO'), ('VICENCIA', 'VICENCIA'), ('CUPIRA', 'CUPIRA'), ('PANELAS', 'PANELAS'), ('JATAUBA', 'JATAUBA'), ('CHA DE ALEGRIA', 'CHA DE ALEGRIA'), ('TRACUNHAEM', 'TRACUNHAEM'), ('SALGADINHO', 'SALGADINHO'), ('LAGOA DO OURO', 'LAGOA DO OURO'), ('CASINHAS', 'CASINHAS'), ('IATI', 'IATI'), ('NAZARE DA MATA', 'NAZARE DA MATA'), ('VERTENTE DO LERIO', 'VERTENTE DO LERIO'), ('ITAMBE', 'ITAMBE'), ('CATENDE', 'CATENDE'), ('CAPOEIRAS', 'CAPOEIRAS'), ('MACHADOS', 'MACHADOS'), ('CARNAUBEIRA DA PENHA', 'CARNAUBEIRA DA PENHA'), ('LAGOA DOS GATOS', 'LAGOA DOS GATOS'), ('BONITO', 'BONITO'), ('FLEXEIRAS', 'FLEXEIRAS'), ('SATUBA', 'SATUBA'), ('SAO JOAO', 'SAO JOAO'), ('SANTA TEREZINHA', 'SANTA TEREZINHA'), ('OURICURI', 'OURICURI'), ('BOM CONSELHO', 'BOM CONSELHO'), ('PASSO DE CAMARAGIBE', 'PASSO DE CAMARAGIBE'), ('CARNAIBA', 'CARNAIBA'), ('JATOBA', 'JATOBA'), ('VENTUROSA', 'VENTUROSA'), ('CAMPESTRE', 'CAMPESTRE'), ('IGARASSU', 'IGARASSU'), ('GRANITO', 'GRANITO'), ('JAQUEIRA', 'JAQUEIRA'), ('GOIANA', 'GOIANA'), ('ABREU E LIMA', 'ABREU E LIMA'), ('CORTES', 'CORTES'), ('VITORIA DE SANTO ANTAO', 'VITORIA DE SANTO ANTAO'), ('SAO JOSE DA COROA GRANDE', 'SAO JOSE DA COROA GRANDE'), ('COITE DO NOIA', 'COITE DO NOIA'), ('SAO LUIS DO QUITUNDE', 'SAO LUIS DO QUITUNDE'), ('SAO MIGUEL DOS CAMPOS', 'SAO MIGUEL DOS CAMPOS'), ('JOAO ALFREDO', 'JOAO ALFREDO'), ('PENEDO', 'PENEDO'), ('MARAGOGI', 'MARAGOGI'), ('RIACHO DAS ALMAS', 'RIACHO DAS ALMAS'), ('POCAO', 'POCAO'), ('CARPINA', 'CARPINA'), ('BELO JARDIM', 'BELO JARDIM'), ('BOCA DA MATA', 'BOCA DA MATA'), ('BARRA DE SAO MIGUEL', 'BARRA DE SAO MIGUEL'), ('MATA GRANDE', 'MATA GRANDE'), ('CORURIPE', 'CORURIPE'), ('BARRA DE SANTO ANTONIO', 'BARRA DE SANTO ANTONIO'), ('BODOCO', 'BODOCO'), ('PALMARES', 'PALMARES'), ('SAO LOURENCO DA MATA', 'SAO LOURENCO DA MATA'), ('PRIMAVERA', 'PRIMAVERA'), ('RIO FORMOSO', 'RIO FORMOSO'), ('POMBOS', 'POMBOS'), ('MOREILANDIA', 'MOREILANDIA'), ('PESQUEIRA', 'PESQUEIRA'), ('FELIZ DESERTO', 'FELIZ DESERTO'), ('TRINDADE', 'TRINDADE'), ('LAJEDO', 'LAJEDO'), ('VICOSA', 'VICOSA'), ('PAULO JACINTO', 'PAULO JACINTO'), ('PIACABUCU', 'PIACABUCU'), ('PILAR', 'PILAR'), ('PINDOBA', 'PINDOBA'), ('BEZERROS', 'BEZERROS'), ('LAGOA DO CARRO', 'LAGOA DO CARRO'), ('SURUBIM', 'SURUBIM'), ('ARARIPINA', 'ARARIPINA'), ('PARANATAMA', 'PARANATAMA'), ('TUPANATINGA', 'TUPANATINGA'), ('PAO DE ACUCAR', 'PAO DE ACUCAR'), ('SAO JOSE DO EGITO', 'SAO JOSE DO EGITO'), ('DORMENTES', 'DORMENTES'), ('MANARI', 'MANARI'), ('SANTA CRUZ DO CAPIBARIBE', 'SANTA CRUZ DO CAPIBARIBE'), ('BREJO DA MADRE DE DEUS', 'BREJO DA MADRE DE DEUS'), ('ARCOVERDE', 'ARCOVERDE'), ('OLINDA', 'OLINDA'), ('OLHO DAGUA DAS FLORES', 'OLHO DAGUA DAS FLORES'), ('CAJUEIRO', 'CAJUEIRO'), ('BUIQUE', 'BUIQUE'), ('SANTA FILOMENA', 'SANTA FILOMENA'), ('XEXEU', 'XEXEU'), ('IPUBI', 'IPUBI'), ('CAMARAGIBE', 'CAMARAGIBE'), ('MESSIAS', 'MESSIAS'), ('EXU', 'EXU'), ('TEREZINHA', 'TEREZINHA'), ('OROBO', 'OROBO'), ('TABIRA', 'TABIRA'), ('CONDADO', 'CONDADO'), ('ITAPETIM', 'ITAPETIM'), ('SALGUEIRO', 'SALGUEIRO'), ('ESCADA', 'ESCADA'), ('LAGOA DO ITAENGA', 'LAGOA DO ITAENGA'), ('PETROLANDIA', 'PETROLANDIA'), ('COLONIA LEOPOLDINA', 'COLONIA LEOPOLDINA'), ('SERTANIA', 'SERTANIA'), ('BELO MONTE', 'BELO MONTE'), ('MURICI', 'MURICI'), ('BRANQUINHA', 'BRANQUINHA'), ('FEIRA NOVA', 'FEIRA NOVA'), ('RIO LARGO', 'RIO LARGO'), ('CANHOTINHO', 'CANHOTINHO'), ('JACARE DOS HOMENS', 'JACARE DOS HOMENS'), ('JUREMA', 'JUREMA'), ('MARIBONDO', 'MARIBONDO'), ('SALOA', 'SALOA'), ('RIBEIRAO', 'RIBEIRAO'), ('CUMARU', 'CUMARU'), ('CABROBO', 'CABROBO'), ('CHA GRANDE', 'CHA GRANDE'), ('PASSIRA', 'PASSIRA'), ('TEOTONIO VILELA', 'TEOTONIO VILELA'), ('SAO BENTO DO UNA', 'SAO BENTO DO UNA'), ('AGRESTINA', 'AGRESTINA'), ('BELEM DE MARIA', 'BELEM DE MARIA'), ('TRIUNFO', 'TRIUNFO'), ('TAQUARANA', 'TAQUARANA'), ('MORENO', 'MORENO'), ('SAO CAITANO', 'SAO CAITANO'), ('TIMBAUBA', 'TIMBAUBA'), ('SAO JOSE DA TAPERA', 'SAO JOSE DA TAPERA'), ('CAETES', 'CAETES'), ('CAMPO ALEGRE', 'CAMPO ALEGRE'), ('BREJAO', 'BREJAO'), ('CALCADO', 'CALCADO'), ('CUSTODIA', 'CUSTODIA'), ('BARRA DE GUABIRABA', 'BARRA DE GUABIRABA'), ('AGUA PRETA', 'AGUA PRETA'), ('ATALAIA', 'ATALAIA'), ('LAGOA DA CANOA', 'LAGOA DA CANOA'), ('ANGELIM', 'ANGELIM'), ('TORITAMA', 'TORITAMA'), ('SANTANA DO IPANEMA', 'SANTANA DO IPANEMA'), ('SANTANA DO MUNDAU', 'SANTANA DO MUNDAU'), ('OLIVENCA', 'OLIVENCA'), ('SERRITA', 'SERRITA'), ('OURO BRANCO', 'OURO BRANCO'), ('FERREIROS', 'FERREIROS'), ('SAO BRAS', 'SAO BRAS'), ('MARECHAL DEODORO', 'MARECHAL DEODORO'), ('BOM JARDIM', 'BOM JARDIM'), ('TERRA NOVA', 'TERRA NOVA'), ('SANTA CRUZ DA BAIXA VERDE', 'SANTA CRUZ DA BAIXA VERDE'), ('JUNQUEIRO', 'JUNQUEIRO'), ('LAGOA GRANDE', 'LAGOA GRANDE'), ('ESTRELA DE ALAGOAS', 'ESTRELA DE ALAGOAS'), ('ANADIA', 'ANADIA'), ('PARICONHA', 'PARICONHA'), ('TRAIPU', 'TRAIPU'), ('IGREJA NOVA', 'IGREJA NOVA'), ('UNIAO DOS PALMARES', 'UNIAO DOS PALMARES'), ('CALUMBI', 'CALUMBI'), ('TUPARETAMA', 'TUPARETAMA'), ('CEDRO', 'CEDRO'), ('CORRENTES', 'CORRENTES'), ('ALAGOINHA', 'ALAGOINHA'), ('SAO JOAQUIM DO MONTE', 'SAO JOAQUIM DO MONTE'), ('PEDRA', 'PEDRA'), ('AMARAJI', 'AMARAJI'), ('BARREIROS', 'BARREIROS'), ('CAMUTANGA', 'CAMUTANGA'), ('TAMANDARE', 'TAMANDARE'), ('BATALHA', 'BATALHA'), ('MACAPARANA', 'MACAPARANA'), ('CARNEIROS', 'CARNEIROS'), ('TACARATU', 'TACARATU'), ('IBIRAJUBA', 'IBIRAJUBA'), ('SENADOR RUI PALMEIRA', 'SENADOR RUI PALMEIRA'), ('SAO JOSE DA LAJE', 'SAO JOSE DA LAJE'), ('ITAQUITINGA', 'ITAQUITINGA'), ('SAO VICENTE FERRER', 'SAO VICENTE FERRER'), ('BREJINHO', 'BREJINHO'), ('INGAZEIRA', 'INGAZEIRA'), ('MINADOR DO NEGRAO', 'MINADOR DO NEGRAO'), ('VERDEJANTE', 'VERDEJANTE'), ('MONTEIROPOLIS', 'MONTEIROPOLIS'), ('INHAPI', 'INHAPI'), ('SAO MIGUEL DOS MILAGRES', 'SAO MIGUEL DOS MILAGRES'), ('ITAIBA', 'ITAIBA'), ('ITAPISSUMA', 'ITAPISSUMA'), ('MAJOR ISIDORO', 'MAJOR ISIDORO'), ('VERTENTES', 'VERTENTES'), ('CAMOCIM DE SAO FELIX', 'CAMOCIM DE SAO FELIX'), ('TACAIMBO', 'TACAIMBO'), ('OROCO', 'OROCO'), ('QUIXABA', 'QUIXABA'), ('SANTA CRUZ', 'SANTA CRUZ'), ('SAO SEBASTIAO', 'SAO SEBASTIAO'), ('BELEM DE SAO FRANCISCO', 'BELEM DE SAO FRANCISCO'), ('SAO BENEDITO DO SUL', 'SAO BENEDITO DO SUL'), ('CACHOEIRINHA', 'CACHOEIRINHA'), ('ARACOIABA', 'ARACOIABA'), ('COQUEIRO SECO', 'COQUEIRO SECO'), ('JAPARATINGA', 'JAPARATINGA'), ('GIRAU DO PONCIANO', 'GIRAU DO PONCIANO'), ('SANHARO', 'SANHARO'), ('SOLIDAO', 'SOLIDAO'), ('FERNANDO DE NORONHA', 'FERNANDO DE NORONHA'), ('MAR VERMELHO', 'MAR VERMELHO'), ('SIRINHAEM', 'SIRINHAEM'), ('SAO JOSE DO BELMONTE', 'SAO JOSE DO BELMONTE'), ('JUCATI', 'JUCATI'), ('BETANIA', 'BETANIA'), ('IGACI', 'IGACI'), ('JOAQUIM NABUCO', 'JOAQUIM NABUCO'), ('ALTINHO', 'ALTINHO'), ('MIRANDIBA', 'MIRANDIBA'), ('ITACURUBA', 'ITACURUBA'), ('CRAIBAS', 'CRAIBAS'), ('CAMPO GRANDE', 'CAMPO GRANDE'), ('PALMEIRINA', 'PALMEIRINA'), ('IBATEGUARA', 'IBATEGUARA'), ('MARAVILHA', 'MARAVILHA'), ('GAMELEIRA', 'GAMELEIRA'), ('JOAQUIM GOMES', 'JOAQUIM GOMES'), ('MARAIAL', 'MARAIAL'), ('CAPELA', 'CAPELA'), ('JUNDIA', 'JUNDIA'), ('CANAPI', 'CANAPI'), ('NOVO LINO', 'NOVO LINO'), ('PARIPUEIRA', 'PARIPUEIRA'), ('TAQUARITINGA DO NORTE', 'TAQUARITINGA DO NORTE'), ('PARNAMIRIM', 'PARNAMIRIM'), ('IGUARACI', 'IGUARACI'), ('ROTEIRO', 'ROTEIRO'), ('SANTA LUZIA DO NORTE', 'SANTA LUZIA DO NORTE'), ('CHA PRETA', 'CHA PRETA'), ('PALESTINA', 'PALESTINA'), ('OLHO DAGUA GRANDE', 'OLHO DAGUA GRANDE'), ('FEIRA GRANDE', 'FEIRA GRANDE'), ('TANQUE DARCA', 'TANQUE DARCA'), ('OLHO DAGUA DO CASADO', 'OLHO DAGUA DO CASADO'), ('JACUIPE', 'JACUIPE'), ('JARAMATAIA', 'JARAMATAIA'), ('BELEM', 'BELEM')], default='', max_length=30, verbose_name='Cidade')),
                ('people', models.PositiveIntegerField(blank=True, default=1, null=True, verbose_name='Quantidade de pessoas')),
            ],
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Monitoring',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(blank=True, choices=[('I', 'Imune'), ('N', 'Normal'), ('H', 'Hospitalizado'), ('U', 'UTI'), ('R', 'Recuperado'), ('M', 'Morto')], max_length=1, verbose_name='Status')),
                ('virus_exposure', bitfield.models.BitField([('confirmed_cases', 'Contato com casos confirmados nos últimos 14 dias'), ('suspect_cases', 'Contato com casos suspeitos nos últimos 14 dias'), ('foreign', 'Contato com pessoas que estiveram em locais com casos confirmados')], blank=True, default=0, verbose_name='Exposição COVID-19')),
                ('oxygen_saturation', models.FloatField(blank=True, default=100.0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)], verbose_name='Saturação de oxigênio (%)')),
                ('result', models.CharField(choices=[('SR', 'Sem resposta'), ('PO', 'Positivo'), ('NE', 'Negativo')], default='SR', max_length=2, verbose_name='Resultado do exame')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('professional', models.CharField(blank=True, default='', max_length=50, verbose_name='Nome do profissional')),
                ('community_health_agent_name', models.CharField(blank=True, default='', max_length=100, verbose_name='Nome do agente comunitário de saúde')),
                ('hypothesis', models.TextField(blank=True, default='', verbose_name='Hipótese diagnóstica')),
                ('tests', models.CharField(blank=True, choices=[('RT', 'RT PCR Covid-19'), ('TR', 'Teste Rápido'), ('AD', 'Agendado para o dia'), ('N', 'Não')], default='', max_length=2, verbose_name='Exames solicitados para COVID-19')),
                ('collection_date', models.DateField(blank=True, null=True, verbose_name='Data da coleta')),
                ('result_date', models.DateField(blank=True, null=True, verbose_name='Data do resultado')),
                ('test_location', models.CharField(blank=True, default='', max_length=50, verbose_name='Local do teste')),
                ('note', models.TextField(blank=True, default='', verbose_name='Observação')),
                ('score', models.PositiveIntegerField(blank=True, default=0, verbose_name='Pontuação')),
                ('medical_referral', models.CharField(blank=True, choices=[('1', 'Internado'), ('2', 'Isolamento'), ('3', 'Não está doente')], default='', max_length=1, verbose_name='Encaminhamento')),
                ('medical_referral_status', models.CharField(blank=True, choices=[('1', 'Casa'), ('2', 'Leito comum'), ('3', 'UTI')], default='', max_length=1, verbose_name='Situação')),
                ('medical_referral_duration', models.PositiveIntegerField(blank=True, default=0, verbose_name='Quantidade de dias')),
                ('prescription', models.CharField(blank=True, choices=[('1', 'Anitta'), ('2', 'Antibiótico de cobertura'), ('3', 'Antitérmico'), ('4', 'Entubação'), ('5', 'Hidroxicloroquina/Azitromicina'), ('6', 'Ivermectina'), ('7', 'Tamiflu'), ('8', 'Ventilação'), ('9', 'Outro(s)')], default='', max_length=1, verbose_name='Prescrição')),
                ('other_prescription', models.CharField(blank=True, default='', max_length=50, verbose_name='Outro')),
                ('health_center', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='prediction.HealthCenter', verbose_name='Unidade de saúde')),
            ],
            options={
                'ordering': ['-created'],
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=100, verbose_name='Nome completo')),
                ('mother_name', models.CharField(blank=True, default='', max_length=100, verbose_name='Nome da mãe')),
                ('birth_date', models.DateField(null=True, validators=[validators.prevent_future_date], verbose_name='Data de nascimento')),
                ('cns', models.CharField(blank=True, default='000000000000000', max_length=15, verbose_name='Cartão do SUS')),
                ('id_document', models.CharField(blank=True, default='000000000', max_length=15, verbose_name='RG')),
                ('cpf', models.CharField(blank=True, default='00000000000', max_length=11, null=True, validators=[validators.validate_cpf], verbose_name='CPF')),
                ('phone_number', models.CharField(blank=True, default='', max_length=20, verbose_name='Número de telefone')),
                ('gender', models.CharField(blank=True, choices=[('F', 'Feminino'), ('M', 'Masculino'), ('N', 'Não quer declarar')], default='', max_length=1, verbose_name='Sexo biológico')),
                ('age', models.PositiveIntegerField(default=0, verbose_name='Idade')),
                ('weight', models.FloatField(blank=True, default=0, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Peso (Kg)')),
                ('height', models.FloatField(blank=True, default=0, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Altura (m)')),
                ('smoker', models.BooleanField(blank=True, default=False, verbose_name='Fumante')),
                ('vaccinated', models.BooleanField(blank=True, default=False, verbose_name='Tomou vacina da gripe em 2020')),
                ('oxygen', models.BooleanField(blank=True, default=False, verbose_name='Precisou de oxigênio recentemente')),
                ('comorbidities', bitfield.models.BitField([('Y', 'Artrite reumatóide'), ('A', 'Asma'), ('C', 'Bronquite crônica'), ('N', 'Câncer'), ('E', 'Demência'), ('D', 'Diabetes'), ('H', 'Doença cardíacas'), ('L', 'Doença crônica no fígado'), ('R', 'Doença renal crônica'), ('W', 'Doenças reumáticas'), ('P', 'Doença pulmonar crônica'), ('I', 'Imunosuprimido'), ('T', 'Hipertensão'), ('V', 'HIV+'), ('B', 'Obesidade'), ('U', 'Portador de Lúpus')], default=0, verbose_name='Comorbidades')),
                ('familiar', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='monitoring.Profile')),
            ],
            options={
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='Trip',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('departure_date', models.DateField(blank=True, default=None, null=True, validators=[validators.prevent_future_date], verbose_name='Ida')),
                ('return_date', models.DateField(blank=True, default=None, null=True, validators=[validators.prevent_future_date], verbose_name='Volta')),
                ('state', models.CharField(default='', max_length=2, verbose_name='Estado')),
                ('county', models.CharField(default='', max_length=50, verbose_name='Município')),
                ('profile', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='monitoring.Profile')),
            ],
        ),
        migrations.CreateModel(
            name='Symptom',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('symptom', models.CharField(choices=[('AN', 'Anosmia (Perda do olfato)'), ('CA', 'Cansaço'), ('CM', 'Confusão mental'), ('CN', 'Congestão nasal'), ('CJ', 'Conjuntivite'), ('DI', 'Diarreia'), ('SB', 'Dificuldade respiratória'), ('ST', 'Dor de garganta'), ('DC', 'Dor de cabeça'), ('AP', 'Dores no corpo'), ('FA', 'Falta de apetite'), ('FV', 'Febre'), ('RN', 'Nariz escorrendo'), ('NA', 'Náusea'), ('TP', 'Tosse produtiva'), ('TS', 'Tosse seca'), ('VO', 'Vômitos')], default='', max_length=2, verbose_name='Tipo de sintoma')),
                ('intensity', models.CharField(blank=True, choices=[('', 'Não apresenta'), ('L', 'Leve'), ('M', 'Moderada'), ('H', 'Grave')], default='L', max_length=1, verbose_name='Intensidade')),
                ('onset', models.DateField(blank=True, null=True, validators=[validators.prevent_future_date], verbose_name='Data do surgimento')),
                ('monitoring', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='monitoring.Monitoring')),
            ],
        ),
        migrations.CreateModel(
            name='SARSHospitalized',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fill_date', models.DateField(auto_now_add=True, verbose_name='Data do preenchimento da ficha de notificação')),
                ('symptom_onset_date', models.DateField(blank=True, null=True, verbose_name='Data de 1ºs sintomas da SRAG')),
                ('ethnicity', models.CharField(blank=True, choices=[('A', 'Amarela'), ('B', 'Branca'), ('I', 'Indígena'), ('P', 'Parda'), ('p', 'Preta')], default='', max_length=1, verbose_name='Raça/Cor')),
                ('indian_ethnicity', models.CharField(blank=True, default='', max_length=50, verbose_name='Etnia indígena')),
                ('pregnancy', models.CharField(blank=True, choices=[('1', '1º trimestre'), ('2', '2º trimestre'), ('3', '3º trimestre'), ('4', 'Idade gestacional ignorada'), ('5', 'Não'), ('6', 'Não se aplica')], default='', max_length=1, verbose_name='Gestante')),
                ('schooling', models.CharField(blank=True, choices=[('0', 'Sem escolaridade/analfabeto'), ('1', 'Fundamental 1º ciclo (1ª a 5ª série)'), ('2', 'Fundamental 2º ciclo (6ª a 9ª série)'), ('3', 'Médio (1º ao 3º ano'), ('4', 'Superior'), ('5', 'Não se aplica')], default='', max_length=1, verbose_name='Escolaridade')),
                ('phone_number', models.CharField(blank=True, default='', max_length=11, verbose_name='Telefone')),
                ('zone', models.CharField(blank=True, choices=[('1', 'Urbana'), ('2', 'Rural'), ('3', 'Periurbana')], default='', max_length=1, verbose_name='Zona')),
                ('country', models.CharField(blank=True, choices=[('AFE', 'Afeganistão'), ('AFR', 'África do Sul'), ('AUS', 'Áustria'), ('ALB', 'Albânia'), ('ALE', 'Alemanha'), ('AND', 'Andorra'), ('ANG', 'Angola'), ('ANT', 'Antígua e Barbuda'), ('ARG', 'Argentina'), ('ARL', 'Argélia'), ('ARM', 'Armênia'), ('ARA', 'Arábia Saudita'), ('AUL', 'Austrália'), ('AZE', 'Azerbaijão'), ('BAH', 'Bahamas'), ('BAN', 'Bangladesh'), ('BAR', 'Barbados'), ('BAM', 'Barém'), ('BEL', 'Belize'), ('BEN', 'Benin'), ('BIE', 'Bielorrússia'), ('BOL', 'Bolívia'), ('BOT', 'Botsuana'), ('BRA', 'Brasil'), ('BRU', 'Brunei Darussalam'), ('BUL', 'Bulgária'), ('BUR', 'Burkina Faso'), ('BUD', 'Burundi'), ('BUT', 'Butão'), ('BEG', 'Bélgica'), ('BOS', 'Bósnia e Herzegovina'), ('CAB', 'Cabo Verde'), ('CAM', 'Camarões'), ('CAJ', 'Camboja'), ('CAN', 'Canadá'), ('CAT', 'Catar'), ('CAZ', 'Cazaquistão'), ('CHA', 'Chade'), ('CHL', 'Chile'), ('CHI', 'China'), ('CHP', 'Chipre'), ('CIN', 'Cingapura'), ('COL', 'Colômbia'), ('COM', 'Comores'), ('CON', 'Congo'), ('COS', 'Costa Rica'), ('COT', 'Costa do Marfim'), ('CRO', 'Croácia'), ('CUB', 'Cuba'), ('CZE', 'Czechia'), ('DIN', 'Dinamarca'), ('DJI', 'Djibuti'), ('DOM', 'Dominica'), ('EGI', 'Egito'), ('ELS', 'El Salvador'), ('EMI', 'Emirados Árabes Unidos'), ('EQU', 'Equador'), ('ERI', 'Eritreia'), ('ESL', 'Eslováquia'), ('ESV', 'Eslovênia'), ('ESP', 'Espanha'), ('EST', 'Estados Unidos da America'), ('ESN', 'Estônia'), ('ESW', 'Eswatini'), ('ETI', 'Etiópia'), ('FED', 'Federação Russa'), ('FIJ', 'Fiji'), ('FIL', 'Filipinas'), ('FIN', 'Finlândia'), ('FRA', 'França'), ('GAB', 'Gabão'), ('GAN', 'Gana'), ('GAM', 'Gâmbia'), ('GEO', 'Geórgia'), ('GRA', 'Granada'), ('GRÉ', 'Grécia'), ('GUA', 'Guatemala'), ('GUI', 'Guiana'), ('GUN', 'Guiné'), ('GUE', 'Guiné Equatorial'), ('GUB', 'Guiné-Bissau'), ('HAI', 'Haiti'), ('HON', 'Honduras'), ('HUN', 'Hungria'), ('IND', 'Índia'), ('ILC', 'Ilhas Cook'), ('ILM', 'Ilhas Marshall'), ('ILS', 'Ilhas Salomão'), ('INN', 'Indonésia'), ('IRQ', 'Iraque'), ('IRL', 'Irlanda'), ('IRA', 'Irã'), ('ISL', 'Islândia'), ('ISR', 'Israel'), ('ITA', 'Itália'), ('IEM', 'Iémen'), ('JAM', 'Jamaica'), ('JAP', 'Japão'), ('JOR', 'Jordânia'), ('KIR', 'Kiribati'), ('KUW', 'Kuwait'), ('LES', 'Lesoto'), ('LET', 'Letônia'), ('LIB', 'Libéria'), ('LIT', 'Lituânia'), ('LUX', 'Luxemburgo'), ('LIB', 'Líbano'), ('LIA', 'Líbia'), ('MAC', 'Macedônia do Norte'), ('MAD', 'Madagáscar'), ('MAW', 'Malawi'), ('MAD', 'Maldivas'), ('MAL', 'Mali'), ('MAT', 'Malta'), ('MAS', 'Malásia'), ('MAR', 'Marrocos'), ('MAU', 'Mauritânia'), ('MAR', 'Maurícia'), ('MIC', 'Micronésia'), ('MON', 'Mongólia'), ('MOT', 'Montenegro'), ('MOC', 'Moçambique'), ('MYA', 'Myanmar'), ('MEX', 'México'), ('MOO', 'Mônaco'), ('NAM', 'Namíbia'), ('NAU', 'Nauru'), ('NEP', 'Nepal'), ('NIC', 'Nicarágua'), ('NIG', 'Nigéria'), ('NIG', 'Níger'), ('NIU', 'Niue'), ('NOR', 'Noruega'), ('NOV', 'Nova Zelândia'), ('OMA', 'Omã'), ('PAL', 'Palau'), ('PAN', 'Panamá'), ('PAP', 'Papua Nova Guiné'), ('PAQ', 'Paquistão'), ('PAR', 'Paraguai'), ('PAI', 'Países Baixos'), ('PER', 'Peru'), ('POL', 'Polônia'), ('POR', 'Portugal'), ('QUI', 'Quirguistão'), ('QUE', 'Quênia'), ('REI', 'Reino Unido'), ('REP', 'República Centro-Africana'), ('RED', 'República Democrática Popular do Laos'), ('RDC', 'República Democrática do Congo'), ('RDM', 'República Dominicana'), ('RPD', 'República Popular Democrática da Coreia'), ('RET', 'República Togolesa'), ('RUT', 'República Unida da Tanzânia'), ('RCA', 'República da Coreia'), ('REM', 'República da Moldávia'), ('RAS', 'República Árabe da Síria'), ('ROM', 'Romênia'), ('RUA', 'Ruanda'), ('SAM', 'Samoa'), ('SMO', 'San Marino'), ('SAN', 'Santa Lúcia'), ('SEN', 'Senegal'), ('SER', 'Serra Leoa'), ('SEY', 'Seychelles'), ('SOM', 'Somália'), ('SRI', 'Sri Lanka'), ('SUD', 'Sudão'), ('SUS', 'Sudão do Sul'), ('SUR', 'Suriname'), ('SUE', 'Suécia'), ('SUI', 'Suíça'), ('SAC', 'São Cristóvão e Nevis'), ('SAT', 'São Tomé e Príncipe'), ('SAV', 'São Vicente e Granadinas'), ('SEV', 'Sérvia'), ('TAI', 'Tailândia'), ('TAJ', 'Tajiquistão'), ('TIM', 'Timor-Leste'), ('TON', 'Tonga'), ('TRI', 'Trindade e Tobago'), ('TUN', 'Tunísia'), ('TUR', 'Turquemenistão'), ('TUQ', 'Turquia'), ('TUV', 'Tuvalu'), ('UCR', 'Ucrânia'), ('UGA', 'Uganda'), ('URU', 'Uruguai'), ('USB', 'Usbequistão'), ('VAN', 'Vanuatu'), ('VEN', 'Venezuela'), ('VIE', 'Vietnã'), ('ZIM', 'Zimbábue'), ('ZAM', 'Zâmbia')], default='', max_length=3, verbose_name='País')),
                ('evolved_to_SARS', models.BooleanField(blank=True, default=False, verbose_name='Caso proveniente de surto de SG que evoluiu para SRAG')),
                ('SARS_from_hospital_internment', models.BooleanField(blank=True, default=False, verbose_name='Caso proveniente de surto de SG que evoluiu para SRAG')),
                ('contact_with_poultry_and_pigs', models.BooleanField(blank=True, default=True, verbose_name='Contato com aves ou suínos')),
                ('symptoms', bitfield.models.BitField((('1', 'Febre'), ('2', 'Tosse'), ('3', 'Dor de garganta'), ('4', 'Dispneia'), ('5', 'Desconforto respiratório'), ('6', 'Saturação O2 < 95%'), ('7', 'Diarreia'), ('8', 'Vômito')), blank=True, default=0, verbose_name='Sinais e sintomas')),
                ('other_symptoms', models.CharField(blank=True, default='', max_length=50, verbose_name='Outros sintomas')),
                ('comorbidities', bitfield.models.BitField((('1', 'Puérpera (até 45 dias do parto)'), ('2', 'Síndrome de Down'), ('3', 'Diabetes mellitus'), ('4', 'Imunodeficiência/Imunodepressão'), ('5', 'Doença cardiovascular crônica'), ('6', 'Doença hepática crônica'), ('7', 'Doença neurológica crônica'), ('8', 'Doença renal crônica'), ('9', 'Doença Hematológica crônica'), ('a', 'Asma'), ('b', 'Outra pneumopatia crônica', 0), ('c', 'Obesidade'), ('d', 'Outro')), blank=True, default=0, verbose_name='Fatores de risco/Comorbidades')),
                ('other_comorbidities', models.CharField(blank=True, default='', max_length=50, verbose_name='Outras comorbidades')),
                ('swine_flu_vaccine', models.BooleanField(verbose_name='Recebeu a vacina contra gripe suína na última campanha')),
                ('mother_vaccinated', models.BooleanField(blank=True, default=False, verbose_name='A mãe recebeu a vacina')),
                ('mother_vaccinated_date', models.DateField(blank=True, default=False, verbose_name='Data em que a mãe recebeu a vacina')),
                ('breastfeed', models.BooleanField(blank=True, default=False, verbose_name='A mãe amamenta a criança')),
                ('single_dose_date', models.DateField(blank=True, null=True, verbose_name='Data da dose única')),
                ('first_dose_date', models.DateField(blank=True, null=True, verbose_name='Data da 1ª dose')),
                ('second_dose_date', models.DateField(blank=True, null=True, verbose_name='Data da 2ª dose')),
                ('flu_antiviral_used', models.BooleanField(blank=True, default=False, verbose_name='Usou antiviral para gripe')),
                ('flu_antiviral', models.CharField(blank=True, choices=[('1', 'Oseltamivir'), ('2', 'Zanamivir'), ('3', 'Outro')], default='', max_length=1, verbose_name='Antiviral')),
                ('other_flu_antiviral', models.CharField(blank=True, default='', max_length=30, verbose_name='Outro antiviral')),
                ('flu_treatment_begin_date', models.DateField(blank=True, null=True, verbose_name='Data de início do tratamento')),
                ('internment', models.BooleanField(blank=True, default=False, verbose_name='Houve internação')),
                ('SARS_internment_date', models.DateField(blank=True, null=True, verbose_name='Data da internação por SRAG')),
                ('icu_internment', models.BooleanField(blank=True, default=False, verbose_name='Internado em UTI')),
                ('icu_internment_begin_date', models.DateField(blank=True, default=False, verbose_name='Data da entrada na UTI')),
                ('icu_internment_release_date', models.DateField(blank=True, default=False, verbose_name='Data da saída da UTI')),
                ('ventilatory_support', models.CharField(blank=True, choices=[('1', 'Sim, invasivo'), ('2', 'Sim, não invasivo'), ('3', 'Não')], default='', max_length=1, verbose_name='Uso de suporte ventilatório')),
                ('chest_x_ray', models.CharField(blank=True, choices=[('1', 'Normal'), ('2', 'Infiltrado intersticial'), ('3', 'Consolidação'), ('4', 'Misto'), ('5', 'Outro'), ('6', 'Não realizado')], default=True, max_length=1, verbose_name='Raio X do tórax')),
                ('other_chest_x_ray_result', models.CharField(blank=True, default='', max_length=30, verbose_name='Outro resultado')),
                ('chest_x_ray_date', models.DateField(blank=True, null=True, verbose_name='Data do raio X')),
                ('collected_sample', models.BooleanField(blank=True, default=False, verbose_name='Coletou amostra')),
                ('collection_date', models.DateField(blank=True, null=True, verbose_name='Data da coleta')),
                ('sample_type', models.CharField(blank=True, choices=[('1', 'Secreção de Naso-orofaringe'), ('2', 'Lavado Broco-alveolar'), ('3', 'Tecido post-mortem'), ('4', 'Outro')], default='', max_length=1, verbose_name='Tipo de amostra')),
                ('other_sample_type', models.CharField(blank=True, default='', max_length=20, verbose_name='Outro tipo')),
                ('gal', models.TextField(blank=True, default=True, verbose_name='Nº de requisição do GAL')),
                ('if_result', models.CharField(blank=True, choices=[('1', 'Positivo'), ('2', 'Negativo'), ('3', 'Inconclusivo'), ('4', 'Não realizado'), ('5', 'Aguardando resultado')], default='', max_length=1, verbose_name='Resultado da IF')),
                ('if_result_date', models.DateField(blank=True, null=True, verbose_name='Data do resultado da IF')),
                ('if_influenza_result', models.CharField(blank=True, choices=[('1', 'Positivo para influenza A'), ('2', 'Positivo para influenza B'), ('3', 'Negativo')], default='', max_length=1, verbose_name='Positivo para influenza')),
                ('if_respiratory_viruses', bitfield.models.BitField((('1', 'Vírus sincicial respiratório'), ('2', 'Parainfluenza 1'), ('3', 'Parainfluenza 2'), ('4', 'Parainfluenza 3'), ('5', 'Adenovírus')), blank=True, default=0, verbose_name='Outros vírus respiratórios')),
                ('if_other_respiratory_virus', models.CharField(blank=True, default='', max_length=30, verbose_name='Outro')),
                ('if_laboratory', models.CharField(blank=True, default='', max_length=30, verbose_name='Laboratório que realizou IF')),
                ('if_laboratory_cnes', models.CharField(blank=True, default='', max_length=7, verbose_name='Código (CNES)')),
                ('rt_pcr_result', models.CharField(blank=True, choices=[('1', 'Detectável'), ('2', 'Não detectável'), ('3', 'Inconclusivo'), ('4', 'Não realizado'), ('5', 'Aguardando resultado')], default='', max_length=1, verbose_name='Resultado da RT-PCR')),
                ('rt_pcr_result_date', models.DateField(blank=True, null=True, verbose_name='Data do resultado da RT-PCR')),
                ('rt_pcr_influenza_result', models.CharField(blank=True, choices=[('1', 'Positivo para influenza A'), ('2', 'Positivo para influenza B'), ('3', 'Negativo')], default='', max_length=1, verbose_name='Positivo para influenza')),
                ('rt_pcr_influenza_a_subtype', models.CharField(blank=True, choices=[('1', 'Influenza A (H1N1) pdm09'), ('2', 'Influenza A/H3N2'), ('3', 'Influenza A não subtipado'), ('4', 'Influenza A não subtipável'), ('5', 'Inconclusivo'), ('6', 'Outro')], default='', max_length=1, verbose_name='Subtipo influenza A')),
                ('other_rt_pcr_influenza_a_subtype', models.CharField(blank=True, default='', max_length=20, verbose_name='Outro subtipo')),
                ('rt_pcr_influenza_b_subtype', models.CharField(blank=True, choices=[('1', 'Victoria'), ('2', 'Yamagatha'), ('3', 'Não realizado'), ('4', 'Inconclusivo'), ('5', 'Outro')], default='', max_length=1, verbose_name='Subtipo influenza B')),
                ('other_rt_pcr_influenza_b_subtype', models.CharField(blank=True, default='', max_length=20, verbose_name='Outro subtipo')),
                ('rt_pcr_respiratory_viruses', bitfield.models.BitField((('1', 'Vírus sincicial respiratório'), ('2', 'Parainfluenza 1'), ('3', 'Parainfluenza 2'), ('4', 'Parainfluenza 3'), ('5', 'Parainfluenza 4'), ('6', 'Adenovírus'), ('7', 'Metapneumovírus'), ('8', 'Bocavírus'), ('9', 'Rinovírus'), ('A', 'Outro vírus respiratório')), blank=True, default=0, verbose_name='Outros vírus respiratórios')),
                ('rt_pcr_other_respiratory_virus', models.CharField(blank=True, default='', max_length=30, verbose_name='Outro')),
                ('rt_pcr_laboratory', models.CharField(blank=True, default='', max_length=30, verbose_name='Laboratório que realizou IF')),
                ('rt_pcr_laboratory_cnes', models.CharField(blank=True, default='', max_length=7, verbose_name='Código (CNES)')),
                ('final_classification', models.CharField(blank=True, choices=[('1', 'SRAG por influenza'), ('2', 'SRAG por outro vírus respiratório'), ('3', 'Outro'), ('4', 'SRAG não especificado')], default='', max_length=1, verbose_name='Classificação final do caso')),
                ('other_final_classification', models.CharField(blank=True, default='', max_length=20, verbose_name='Outro agente etiológico')),
                ('closure_criteria', models.CharField(blank=True, choices=[('1', 'Laboratorial'), ('2', 'Vínculo-Epidemiológico'), ('3', 'Clínico')], default='', max_length=1, verbose_name='Critério de encerramento')),
                ('release_or_death_date', models.DateField(blank=True, null=True, verbose_name='Data da alta ou óbito')),
                ('closure_date', models.DateField(blank=True, verbose_name='Data do encerramento')),
                ('notes', models.TextField(blank=True, default='', verbose_name='Observações')),
                ('crm', models.CharField(blank=True, default='', max_length=7, verbose_name='CRM')),
                ('address', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='monitoring.Address', verbose_name='Endereço')),
                ('health_center', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='prediction.HealthCenter', verbose_name='Unidade de saúde')),
                ('health_professional', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Profissional da saúde responsável')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='monitoring.Profile', verbose_name='Paciente')),
            ],
        ),
        migrations.CreateModel(
            name='Request',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('material', models.CharField(default='', max_length=100, verbose_name='Material requisitado')),
                ('quantity', models.PositiveIntegerField(default=0, verbose_name='Quantidade necessária')),
                ('name', models.CharField(default='', max_length=100, verbose_name='Nome')),
                ('cellphone', models.CharField(blank=True, default='', max_length=20, null=True, verbose_name='Telefone')),
                ('email', models.CharField(blank=True, default='', max_length=40, null=True, verbose_name='E-mail')),
                ('unidade', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='prediction.HealthCenter')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Neighbourhood',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='monitoring.City')),
            ],
        ),
        migrations.AddField(
            model_name='monitoring',
            name='profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='monitoring.Profile'),
        ),
        migrations.AddField(
            model_name='address',
            name='profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='monitoring.Profile'),
        ),
        migrations.CreateModel(
            name='ActionLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action', models.CharField(choices=[('C', 'CREATE'), ('D', 'DELETE'), ('U', 'UPDATE')], max_length=1)),
                ('model', models.CharField(choices=[('PR', 'PROFILE'), ('AD', 'ADDRESS'), ('MO', 'MONITORING'), ('SY', 'SYMPTOM'), ('TR', 'TRIP'), ('RE', 'REQUEST'), ('HC', 'HEALTH CARE STATUS')], max_length=2)),
                ('ip', models.CharField(max_length=50)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]