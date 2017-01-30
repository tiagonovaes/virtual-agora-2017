from __future__ import unicode_literals

from django.db import models

# Create your models here.
class TextoPreproc(models.Model):
    vertice = models.CharField('Vertice', max_length=50)
    vertice_num = models.IntegerField()

    def __str__(self):
        return self.vertice


class DadosPreproc(models.Model):
     palavras_texto_original = models.CharField('PalavrasTO', max_length=10)
     palavras_texto_lematizado = models.CharField('PalavrasTL', max_length=10)
     palavras_texto_lematizado_ssw = models.CharField('PalavrasTLSSW', max_length=10)
     quantidade_de_sentencas = models.IntegerField('q_sen')
     palavras_por_sentenca_lssw = models.IntegerField('ppsl')
     palavras_por_sentenca_org = models.IntegerField('ppso')
     nome_rel_protofrase = models.CharField('nome_rel_pfs', max_length=100)

     def __str__(self):
        return self.palavras_texto_original

class ListaVertices(models.Model):
     node = models.CharField('Node', max_length=50)
     index = models.IntegerField('index', default=-1)

     def __str__(self):
        return self.node

class ListaDeAdjacencias(models.Model):
     vertice_i = models.CharField('vi', max_length=50)
     vertice_f = models.CharField('vf', max_length=50)
     peso = models.IntegerField('peso')

     def __str__(self):
        return self.vertice_i

class TabelaRanking(models.Model):
     vertice_nome =  models.CharField('V_nome', max_length=60)
     vertice_numero = models.IntegerField('V_numero')
     grau = models.IntegerField('Grau')
     betweenness = models.FloatField('Betweenness')
     closeness = models.FloatField('Closeness')
#     betweenness = models.DecimalField('Betweenness',max_digits=10, decimal_places=5)
#     closeness = models.DecimalField('Closeness',max_digits=10, decimal_places=5)

     def __str__(self):
        return self.vertice_nome

class ProtoFrase(models.Model):
     vertice_inicial = models.CharField('vi', max_length=50)
     protofrase = models.TextField('pf')

     def __str__(self):
        return self.vertice_inicial

class Sorteio(models.Model):
    vertice = models.CharField('vertice_s', max_length=50)
    posicao = models.IntegerField('posicao')

    def __str__(self):
        return self.vertice

class DadosProtofrases(models.Model):
    protofrase = models.TextField('dpf')
    repeticao = models.IntegerField('rep')

    def __str__(self):
        return self.protofrase

class DadosMapeamentoEExtracao(models.Model):
    arquivo = models.CharField('arq', max_length=100)
    protofrase = models.TextField('dpf')
    num_sent_docPreproc = models.IntegerField('nsdp')
    num_sent_docPreprocLemCSW = models.IntegerField('nsdplc')
    num_sent_docPreprocLemSSW = models.IntegerField('nsdpls')
    extracaoParagrafosEtapa1 = models.TextField('etapa1')


    def __str__(self):
        return self.arquivo


class MapeamentoEExtracaoTextos(models.Model):
    paragrafo = models.IntegerField('par')
    doc_preproc = models.TextField('d_p')
    doc_preprocLemCSSW = models.TextField('d_plc')
    doc_preprocLemSSW = models.TextField('d_pls')

    def __str__(self):
        return self.doc_preproc


class ParagrafosExtraidos(models.Model):
    paragrafo = models.TextField('Paragrafo')
    protofrase = models.TextField('Proto-Frase_atual')
    arquivo = models.TextField('arquivo')
    dataHora = models.TextField('Data_Hora')
    etapa = models.IntegerField('etapa')
    protofrase_original = models.TextField('proto-frase_original')


    def __str__(self):
        return self.paragrafo
