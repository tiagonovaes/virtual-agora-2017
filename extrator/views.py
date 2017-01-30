# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.views import generic
from subprocess import call
from django.shortcuts import get_object_or_404, render,render_to_response,redirect
from django.contrib import messages
from .models import TextoPreproc, DadosPreproc, ListaVertices, TabelaRanking, ProtoFrase, Sorteio, ListaDeAdjacencias, DadosProtofrases, DadosMapeamentoEExtracao, MapeamentoEExtracaoTextos, ParagrafosExtraidos
from django.db import models
import os.path
import subprocess
import commands
import os
import time
import platform
import io
import textwrap
import nltk
import codecs
import time
import numpy
import collections
import networkx as nx
import graphviz as gv
import pylab as plt
from graphviz import Digraph
import matplotlib.pyplot as plt
from random import randint
import re
import time
import unicodedata
from unidecode import unidecode
from collections import OrderedDict
import operator
from django.db.models import Avg, Max, Min
from django.urls import reverse

# Create your views here.


class RelatorioPreprocHomeView(generic.ListView):
  template_name = 'extrator/relatoriopreproc.html'
  #model = Topic
  def get_queryset(self):
     #u = User.objects.get(user=self.request.user)
     return #Topic.objects.filter(published='Sim',projeto__sigla=u.user.user.projeto).distinct()



class ExtratorHomeView(generic.ListView):
  template_name = 'extrator/extrator_home.html'
  #model = Topic


  def get_queryset(self):

    return #Topic.objects.filter(published='Sim',projeto__sigla=u.user.user.projeto).distinct()

  def get_context_data(self, **kwargs):
    ### arquivos txt ####
    new =[]
    for file in os.listdir("extrator/arquivos/protofrases/"):
        if file.endswith(".txt"):
            new.append(file)
    #### protofrases do arquivo escolhido ####
    dadoM = DadosMapeamentoEExtracao.objects.get(id=1)
    arquivo = dadoM.arquivo
    lista = open("extrator/arquivos/protofrases/" + arquivo).readlines()
    count = 0
    new2 = []
    for i in lista:
        if count > 2:
            new2.append(i.strip())
        count = count + 1
    str1 = ' '.join(new2)

    context = super(ExtratorHomeView, self).get_context_data(**kwargs)
    context['vertices'] = ListaVertices.objects.all()
    context['arquivos'] = new
    context['proto_frases'] = new2


    #context['b'] = a

    return context

def inserir_dados_de_entrada(request):
    #CRIA/lÊ O ARQUIVO ONDE SERÁ INSERIDO OS DADOS DE ENTRADA
    ParagrafosExtraidos.objects.all().delete()
    if os.path.exists("extrator/arquivos/doc_original.txt"):
            programName = "notepad.exe"
            fileName = "extrator/arquivos/doc_original.txt"
            subprocess.Popen([programName, fileName])
            messages.success(request, "Arquivo de entrada criado e aberto com sucesso. Insira os dados e salve-o. ATENÇÃO: SALVAR ARQUIVO EM utf-8")

            dados_de_entrada = open("extrator/arquivos/doc_original.txt","r").read()
            return render(request, 'extrator/extrator_home.html', {'dados_de_entrada':dados_de_entrada })
    else:
        file_doc_original = open("extrator/arquivos/doc_original.txt","w")
        file_doc_original.close()
        programName = "notepad.exe"
        fileName = "extrator/arquivos/doc_original.txt"
        subprocess.Popen([programName, fileName])
        messages.success(request, "Arquivo de entrada criado e aberto com sucesso. Insira os dados e salve-o. ATENÇÃO: SALVAR ARQUIVO EM utf-8")
        return redirect(request.META['HTTP_REFERER'])


def pre_processamento(request):
    #Tokeniza o texto e escreve em documento único.
    thefile = open('extrator/arquivos/doc_preproc.txt', 'w')
    file_org = open("extrator/arquivos/doc_vet_preproc.txt","w")
    f = codecs.open("extrator/arquivos/doc_original.txt", "r", "utf-8-sig")
    fil = f.read()
    fil = re.sub(r'[\?\.\!\;]+(?=[\?\.\!\;])', '', fil)
    tokens = nltk.word_tokenize(fil)
    t = len(tokens)
    pontuacao = [".","!","(",")",":",";","<","=",">","?","[","]","{","|","}"]
    try:
       a = DadosPreproc.objects.get(id=1)
       a.palavras_texto_original = str(t)
       a.save()
    except:
       DadosPreproc.objects.create(id=1, palavras_texto_original=str(t))
    sentencas = 0
    for item in tokens:
        if item in pontuacao:
            item = "."
            sentencas = sentencas + 1
        item_l = item.lower()
        thefile.write(item_l.encode("utf-8") + " ")
        file_org.write(item_l.encode("utf-8") + "\n")
    thefile.close()
    file_org.close()

    try:
       a = DadosPreproc.objects.get(id=1)
       a.quantidade_de_sentencas = sentencas
       a.save()
    except:
       DadosPreproc.objects.create(id=1, quantidade_de_sentencas=sentencas)

    messages.success(request, "Documento preparado com sucesso!")
    return render(request, 'extrator/extrator_home_2.html', {'dados_de_entrada': None})



def lematizar(request):

    #Abre o Bash e executa o lematizador
    is32bit = (platform.architecture()[0] == '32bit')
    system32 = os.path.join(os.environ['SystemRoot'],
                        'SysNative' if is32bit else 'System32')
    bash = os.path.join(system32, 'bash.exe')
    start_time = time.time()
    p = subprocess.check_call('"%s" -c "cd Linguakit-master ; ./linguakit pt lem ../extrator/arquivos/doc_preproc.txt > ../extrator/arquivos/saida_lematizador.txt ; unix2dos ../extrator/arquivos/saida_lematizador.txt"' % bash, shell=True)
    temp =  time.time() - start_time
    #abre o texto já lematizado e cria dois novos arquivos: um com o texto original e outro com o texto lematizado

    file = open("extrator/arquivos/saida_lematizador.txt","r")
    file_c = open("extrator/arquivos/doc_lematizado_csw.txt","w")
    file_lem = open("extrator/arquivos/doc_vet_lematizado_csw.txt","w")



    for line in file:
        try:
            line.split(' ')[2]
            word_lem = line.split(' ')[1]
            file_c.write(word_lem + ' '),
            file_lem.write(word_lem + '\n'),

        except:

            word_lem = line.split(' ')[0]
            messages.warning(request, "Palavra " + word_lem + " não lematizada")
            file_c.write(word_lem + ' '),
            file_lem.write(word_lem + '\n'),


    file_lem.close()
    file_c.close()


    file_l = open("extrator/arquivos/doc_vet_lematizado_csw.txt","r")
    t = sum(1 for _ in file_l)
    try:
       a = DadosPreproc.objects.get(id=1)
       a.palavras_texto_lematizado = str(t)
       a.save()
    except:
       DadosPreproc.objects.create(id=1, palavras_texto_lematizado=str(t))

    messages.success(request, "Documento lematizado com sucesso! " + "Tempo: " + str(temp) + " segundos." )
    return render(request, 'extrator/extrator_home_2.html', {'dados_de_entrada': None})
    #return redirect('agoraunicamp:agora')


def ver_arquivo(request, arquivo):
    if arquivo == "excessao":
        arq = DadosPreproc.objects.get(id=1)
        arquivo = arq.nome_rel_protofrase
        programName = "notepad.exe"
        fileName = "extrator/arquivos/protofrases/" + arquivo
        subprocess.Popen([programName, fileName])
        messages.success(request, "Arquivo aberto com sucesso!")
        return render(request, 'extrator/extrator_home.html', {'dados_de_entrada': None, 'relatorio_preproc':None })

    if arquivo == "excessao2":
        arq = ParagrafosExtraidos.objects.first()
        arquivo = arq.arquivo
        programName = "notepad.exe"
        fileName = "extrator/arquivos/paragrafos/extracao_" + arquivo
        subprocess.Popen([programName, fileName])
        messages.success(request, "Arquivo aberto com sucesso!")
        return redirect(request.META['HTTP_REFERER'])


    if os.path.exists("extrator/arquivos/" + arquivo +".txt"):
        programName = "notepad.exe"
        fileName = "extrator/arquivos/" + arquivo
        subprocess.Popen([programName, fileName])
        messages.success(request, "Arquivo aberto com sucesso!")
        return render(request, 'extrator/extrator_home.html', {'dados_de_entrada': None, 'relatorio_preproc':None })
    else:
        messages.error(request, "Arquivo inexistente")
        return render(request, 'extrator/extrator_home.html', {'dados_de_entrada': None, 'relatorio_preproc':None })

def preparar_lista_stopwords(request):
    if os.path.exists("extrator/arquivos/stopwords.txt"):
        f = codecs.open("extrator/arquivos/stopwords.txt", "r", "utf-8-sig")
        fil = f.read()
        tokens = nltk.word_tokenize(fil)
        thefile = open('extrator/arquivos/stopwords.txt', 'w')
        for item in tokens:
            item_l = item.lower()
            thefile.write(item_l.encode("utf-8") + "\n")
        thefile.close()


        messages.success(request, "Lista preparada com sucesso.")
        return render(request, 'extrator/extrator_home_2.html', {'dados_de_entrada': None})
    else:
        messages.error(request, "Lista de stopwords não encontrada! Crie um arquivo txt de nome stopwords.txt na pasta arquivos do extrator.")
        return render(request, 'extrator/extrator_home_2.html', {'dados_de_entrada': None})


def eliminar_stopwords(request):
    if os.path.exists("extrator/arquivos/stopwords.txt"):
        a = 1
    else:
        messages.error(request, "Lista de stopwords não encontrada! Crie um arquivo txt de nome stopwords.txt na pasta arquivos do extrator.")
        return render(request, 'extrator/extrator_home_2.html', {'dados_de_entrada': None })

    stopwords = open("extrator/arquivos/stopwords.txt").readlines()
    lista = open("extrator/arquivos/doc_vet_lematizado_csw.txt").readlines()
    arq = open("extrator/arquivos/doc_vet_preproc_ssw.txt","w")
    arq1 = open("extrator/arquivos/doc_preproc_ssw.txt","w")
    new_list = []
    for w in lista:
        if w not in stopwords:
            new_list.append(w)
    for item in new_list:
        arq.write(item)
    arq.close()


    t = len(new_list)
    try:
       a = DadosPreproc.objects.get(id=1)
       a.palavras_texto_lematizado_ssw = str(t)
       a.save()
    except:
       DadosPreproc.objects.create(id=1, palavras_texto_lematizado_ssw=str(t))


    f = codecs.open("extrator/arquivos/doc_vet_preproc_ssw.txt", "r", "utf-8-sig")
    fil = f.read()
    tokens = nltk.word_tokenize(fil)

    for item in tokens:
        arq1.write(item.encode("utf-8") + " ")
    arq1.close()


    messages.success(request, "StopWords eliminados com sucesso.")
    return render(request, 'extrator/extrator_home_2.html', {'dados_de_entrada': None })

def salvar_dados(request):
    q = TextoPreproc.objects.all()
    q.delete()
    vertice = open("extrator/arquivos/doc_vet_preproc_ssw.txt").readlines()
    for w in vertice:
        ver = TextoPreproc(vertice=w, vertice_num=-1)
        ver.save()
    messages.success(request, "Dados salvos com sucesso.")
    return render(request, 'extrator/extrator_home_2.html', {'dados_de_entrada': None })


def gerar_relatorio(request):
    a = DadosPreproc.objects.get(id=1)
    arq = open("extrator/arquivos/relatorio_preproc.txt","w")

    arq.write("RELATÓRIO DA ETAPA DE PRÉ-PROCESSAMENTO \n\n")
    arq.write("Os dados de entrada contém " + str(a.quantidade_de_sentencas) + " parágrafos.\n")
    arq.write("Os dados de entrada possuem " + a.palavras_texto_original + " tokens.\n")
    arq.write("Os dados lematizados possuem " + a.palavras_texto_lematizado + " tokens.\n")

    new_list = []
    file = open("extrator/arquivos/saida_lematizador.txt","r")
    for line in file:
        try:
            line.split(' ')[2]
        except:
            word_lem = line.split(' ')[0]
            new_list.append(word_lem)

    if not new_list:
        arq.write("Não houve erros durante a lematização.\n")
    else:
        arq.write("Palavras não lematizadas: ")
        for i in new_list:
            arq.write(i + " " )
        arq.write("\n")
    arq.write("O documento lematizado e sem stopwords possui " + a.palavras_texto_lematizado_ssw + " tokens.\n\n")
    arq.write("CONCLUSãO:\n")
    comp = 100 - (float(a.palavras_texto_lematizado_ssw)/float(a.palavras_texto_original))*100
    arq.write("Compressão do texto após pré-processamento: " + str(comp) + " %.\n")
    pal_sen_org = round(float(int(a.palavras_texto_original)-int(a.quantidade_de_sentencas))/float(a.quantidade_de_sentencas))
    a.palavras_por_sentenca_org = int(pal_sen_org)
    a.save()
    arq.write("Em média, cada sentença do texto original possui " + str(int(pal_sen_org)) + " palavras.\n")
    pal_sen_lemssw = round(float(int(a.palavras_texto_lematizado_ssw) - int(a.quantidade_de_sentencas))/float(a.quantidade_de_sentencas))
    a.palavras_por_sentenca_lssw = int(pal_sen_lemssw)
    a.save()
    arq.write("Em média, cada sentença do texto lematizado sem stop-words possui " + str(int(pal_sen_lemssw)) + " palavras.\n")
    arq.close()
    messages.success(request, "Relatório gerado com sucesso.")
    rel = open("extrator/arquivos/relatorio_preproc.txt","r").read()
    return render(request, 'extrator/extrator_home_2.html', {'dados_de_entrada': None, 'relatorio_preproc':rel })

def preproc_completo(request):
    pre_processamento(request)
    lematizar(request)
    preparar_lista_stopwords(request)
    eliminar_stopwords(request)
    salvar_dados(request)
    gerar_relatorio(request)
    return redirect(request.META['HTTP_REFERER'])


## 3. REDE COMPLEXA ------------------------------------------------------------------------------------------------------------------------------------------

def lista_de_vertices(request):
    pontos_finais = [".\n","!\n","?\n",":\n",";\n"]
    objs = TextoPreproc.objects.exclude(vertice__in=pontos_finais).values_list('vertice', flat=True).distinct()
    index = 0
    ListaVertices.objects.all().delete()
    for item in objs:
        node = ListaVertices(index = index, node = item)
        node.save()
        index = index + 1
    messages.success(request, "lista criada com sucesso.")
    return render(request, 'extrator/extrator_home_3.html', {'dados_de_entrada': None, 'relatorio_preproc':None })

def mapear(request):

    v = TextoPreproc.objects.all()
    v_num = ListaVertices.objects.all()
    for item1 in v:
         for item2 in v_num:
             if item1.vertice == item2.node:
                item1.vertice_num = item2.index
                item1.save()

    messages.success(request, "Mapeamento completo.")
    return render(request, 'extrator/extrator_home_3.html', {'dados_de_entrada': None, 'relatorio_preproc':None })


def matriz(request):
    num = ListaVertices.objects.all().count()
    listav = ListaVertices.objects.all()
    elementos = TextoPreproc.objects.all()
    tamanho_do_texto = TextoPreproc.objects.all().count()
    matrix = numpy.zeros(shape=(num,num))

    paj = open("extrator/arquivos/pajek_net.net","w")
    paj.write("*Vertices ")
    paj.write(str(num))
    paj.write("\n")

    x = 1
    for item in listav:
        n = item.index + 1
        paj.write(str(n))
        paj.write(' ')
        #a = item.node.encode('ascii', errors='xmlcharrefreplace')
        paj.write(item.node.encode('iso 8859-15','ignore'))
        x = x + 1

    paj.write("*Arcs")
    paj.write("\n")
    for i, item in enumerate(elementos):
        vertice_atual = item.vertice_num
        proximo_vertice = elementos[(i+1) % len(elementos)].vertice_num

        if vertice_atual >= 0 and proximo_vertice >= 0 and i < tamanho_do_texto - 1:
            matrix[vertice_atual , proximo_vertice] = matrix[vertice_atual , proximo_vertice] + 1

    numpy.savetxt("extrator/arquivos/matriz_de_adjacencias.txt",matrix, fmt='%i')

    ListaDeAdjacencias.objects.all().delete()
    arq = open("extrator/arquivos/lista_de_adjacencias.txt","w")
    x = 0
    y = 0
    for i in range(0, len(matrix)):
        for j in range(0, len(matrix)):
            if matrix[i,j] > 0:
                a = ListaVertices.objects.get(index = x)
                arq.write(a.node.strip().encode('utf-8'))
                arq.write(" ")
                paj.write(str(a.index + 1))
                paj.write(" ")
                b = ListaVertices.objects.get(index = y)
                paj.write(str(b.index + 1))
                paj.write(" ")
                arq.write(b.node.strip().encode('utf-8'))
                arq.write(" ")
                arq.write(str(matrix[i,j]))
                arq.write("\n")
                paj.write(str(matrix[i,j]).split('.')[0])
                paj.write("\n")
                l = ListaDeAdjacencias(vertice_i=a.node,vertice_f=b.node,peso=matrix[i,j])
                l.save()
            y = y + 1
        y = 0
        x = x +1

    arq.close()
    lista = open("extrator/arquivos/lista_de_adjacencias.txt").readlines()
    paj.close()
    messages.success(request, "Matriz gerada com sucesso.")
    return render(request, 'extrator/extrator_home_3.html', {'dados_de_entrada': None, 'relatorio_preproc':None })



def rede_complexa(request):
    if os.path.exists("extrator/arquivos/pajek_net.net"):
        programName = "extrator/pajek64/Pajek.exe"
        fileName = "extrator/arquivos/pajek_net.net"
        subprocess.Popen([programName, fileName])
        messages.success(request, "Arquivo aberto com sucesso!")
        return render(request, 'extrator/extrator_home_3.html', {'dados_de_entrada': None, 'relatorio_preproc':None })
    else:
        messages.error(request, "Arquivo inexistente")
        return render(request, 'extrator/extrator_home_3.html', {'dados_de_entrada': None, 'relatorio_preproc':None })


def redecomplexa_completo(request):
    lista_de_vertices(request)
    mapear(request)
    matriz(request)
    return redirect(request.META['HTTP_REFERER'])


def cria_log_metricas(request):
    arq = open("extrator/arquivos/pajek_log_metricas.log","w")
    arq.write("NETBEGIN 1\nCLUBEGIN 1\nPERBEGIN 1\nCLSBEGIN 1\nHIEBEGIN 1\nVECBEGIN 1\n\n")
    arq.write("""N 1 RDN "c:/virtual-agora/extrator/arquivos/pajek_net.net" ()\n""")
    arq.write("V 1 LINESUM 1 [2] ()\n")
    arq.write("""V 1 WV "C:/virtual-agora/extrator/arquivos/graus.vec" 0 ()\n""")
    arq.write("V 2 CLOSE 1 [2] ()\n")
    arq.write("""V 2 WV "C:/virtual-agora/extrator/arquivos/closeness.vec" 0 ()\n""")
    arq.write("V 3 BETWEEN 1 ()\n")
    arq.write("""V 3 WV "C:/virtual-agora/extrator/arquivos/betweenness.vec" 0 ()\n""")
    arq.write("V 5 CLUSTCOEFF 1 ()\n")
    arq.write("""V 4 WV "C:/virtual-agora/extrator/arquivos/CC1.vec" 0 ()\n""")
    arq.write("V 6 DISTRDISTALL 1 ()\n")
    arq.write("""V 6 WV "C:/virtual-agora/extrator/arquivos/distance.vec" 0 ()\n""")
    arq.write("V 7 CENTERS 1 w w\n")
    arq.write("""V 7 WV "C:/virtual-agora/extrator/arquivos/centers.vec" 0 ()\n""")
    arq.write("E 1 CIRCULAR\nE 1 DRAW 0 0 0 0 0\nE 1 KAMADA\n")
    arq.write("""C 1 WTABCLUVEC "C:/virtual-agora/extrator/arquivos/metricas_completas.txt" -1 2 2 2 1\n""")
    arq.write("DRAWWINDOW OFF\n")
    arq.write("EXIT")
    arq.close()


    if os.path.exists("extrator/arquivos/pajek_log_metricas.log"):
        programName = "extrator/pajek64/Pajek.exe"
        fileName = "extrator/arquivos/pajek_log_metricas.log"
        subprocess.Popen([programName, fileName])
        messages.success(request, "Métricas calculadas com sucesso!")
        return render(request, 'extrator/extrator_home_4.html', {'dados_de_entrada': None, 'relatorio_preproc':None })
    else:
        messages.error(request, "Arquivo inexistente")
        return render(request, 'extrator/extrator_home_4.html', {'dados_de_entrada': None, 'relatorio_preproc':None })
    return render(request, 'extrator/extrator_home_4.html', {'dados_de_entrada': None, 'relatorio_preproc':None })

def gerar_tabelas_ranking(request):
    dados = open("extrator/arquivos/metricas_completas.txt").readlines()
    tabela_g = open("extrator/arquivos/tabela_graus.txt", 'w')
    tabela_b = open("extrator/arquivos/tabela_betweenness.txt", 'w')
    tabela_c = open("extrator/arquivos/tabela_closeness.txt", 'w')
    #D = {}
    #OD_graus = {}
    q = TabelaRanking.objects.all()
    q.delete()
    a = 0
    for item in dados:
        if a != 0:
            t = TabelaRanking(vertice_nome=item.split(';')[1],vertice_numero=item.split(';')[0],grau=item.split(';')[2],betweenness=float(item.split(';')[4].replace(',','.')),closeness=float(item.split(';')[3].replace(',','.')))
            t.save()
        a = 1

    tabela_graus = TabelaRanking.objects.all().order_by('-grau')
    tabela_betweenness = TabelaRanking.objects.all().order_by('-betweenness')
    tabela_closeness = TabelaRanking.objects.all().order_by('-closeness')

    for a in tabela_graus:
        tabela_g.write(a.vertice_nome.encode('utf-8'))
        tabela_g.write(' ')
        tabela_g.write(str(a.grau))
        tabela_g.write('\n')
    tabela_g.close()
    messages.success(request, "Tabela Graus gerada com sucesso.")

    for a in tabela_betweenness:
        tabela_b.write(a.vertice_nome.encode('utf-8'))
        tabela_b.write(' ')
        tabela_b.write(str(a.betweenness))
        tabela_b.write('\n')
    tabela_b.close()
    messages.success(request, "Tabela Betweenness gerada com sucesso.")

    for a in tabela_closeness:
        tabela_c.write(a.vertice_nome.encode('utf-8'))
        tabela_c.write(' ')
        tabela_c.write(str(a.closeness))
        tabela_c.write('\n')
    tabela_c.close()
    messages.success(request, "Tabela Closeness gerada com sucesso.")
    return render(request, 'extrator/extrator_home_4.html', {'dados_de_entrada': None, 'relatorio_preproc':None })



def metricas_e_ranking_comp(request):
    ProtoFrase.objects.all().delete()
    cria_log_metricas(request)
    gerar_tabelas_ranking(request)
    return redirect(request.META['HTTP_REFERER'])

def salvaVerticeInicial(request):
    v_inicial = request.POST['verticeinicial']
    n_pfs = request.POST['num_protofrases']
    try:
        a = int(n_pfs)
    except:
        messages.error(request, "Coloque a quantidade desejada de proto-frases.")
        return render(request, 'extrator/extrator_home_5.html', {'dados_de_entrada': None, 'relatorio_preproc':None })
    ProtoFrase.objects.all().delete()
    for i in range(int(n_pfs)):
        v = ProtoFrase(vertice_inicial=v_inicial)
        v.save()
    messages.success(request, "Dados enviados com sucesso.")
    return render(request, 'extrator/extrator_home_5.html', {'dados_de_entrada': None, 'relatorio_preproc':None })

def gerar_proto_frases(request):
    ps = DadosPreproc.objects.get(id=1)
    vertices = ProtoFrase.objects.all()
    for item in vertices:
        atual = item.vertice_inicial
        proto_frase = []
        count = 1
        while(count < ps.palavras_por_sentenca_lssw):
            proto_frase.append(atual)
            lista = ListaDeAdjacencias.objects.all()
            Sorteio.objects.all().delete()
            posicao = 1
            ok = 0
            for linha in lista:
                a = linha.vertice_i.strip()
                b = atual.strip()
                if a == b:
                    ok = 1
                    for i in range(linha.peso):
                        p = Sorteio(posicao=posicao,vertice=linha.vertice_f)
                        p.save()
                        posicao = posicao + 1
            if ok == 0:
                break
            sorteado = randint(1,posicao-1)
            a = Sorteio.objects.get(posicao=sorteado)
            atual = a.vertice
            count = count + 1
        pf = ProtoFrase()
        str1 = ''.join(proto_frase)
        item.protofrase = str1
        item.save()
    messages.success(request, "Proto-frases geradas com sucesso.")
    return render(request, 'extrator/extrator_home_5.html', {'dados_de_entrada': None, 'relatorio_preproc':None })

def removerProtoFrases(request):
    ProtoFrase.objects.all().delete()
    ver = ListaVertices.objects.all()
    messages.success(request, "Dados excluídos com sucesso.")
    return render(request, 'extrator/extrator_home_5.html', {'dados_de_entrada': None, 'relatorio_preproc':None , 'vertices' : ver })

def gerarRelatorioDadosPfs(request):
    DadosProtofrases.objects.all().delete()
    a = ProtoFrase.objects.values_list('vertice_inicial').distinct()
    for i in a:
        c = i[0].strip()
        c = unidecode(c)
    temp = time.strftime("%Y%m%d-%H%M%S")
    dadosp = DadosPreproc.objects.get(id=1)
    dadosp.nome_rel_protofrase = c + "_" + temp
    dadosp.save()
    arq = open("extrator/arquivos/protofrases/" + c + "_" + temp + ".txt","w")
    for item in a:
        numero = ProtoFrase.objects.filter(vertice_inicial__exact=item[0]).count()
        arq.write("Foram extraídas " + str(numero) + " proto-frases.\n")
        b = ProtoFrase.objects.filter(vertice_inicial__exact=item[0])
        z = b.values_list('protofrase').distinct()
        numero_d = z.count()
        arq.write(str(numero_d) + " proto-frases distintas, sendo:\n\n")
        for item in z:
            t = ProtoFrase.objects.filter(protofrase__exact=item[0]).count()
            d = DadosProtofrases(protofrase=item[0],repeticao=t)
            d.save()
        dados_p = DadosProtofrases.objects.all().order_by('-repeticao')
        for item in dados_p:
            t = item.repeticao
            pc = (float(t) / float(numero))*100
            pc = round(pc,1)
            a = item.protofrase.split('\n')
            new = []
            for i in a:
                new.append(i.strip())
            str1 = ' '.join(new)
            arq.write(str(t) + " vezes (" + str(pc) + " %): " + str1.encode('utf-8') + "\n")
    arq.close()
    messages.success(request, "Relatório gerado com sucesso.")
    rel = open("extrator/arquivos/protofrases/" + c + "_" + temp + ".txt","r").read()
    return render(request, 'extrator/extrator_home_5.html', {'dados_de_entrada': None, 'relatorio_preproc':None, 'relatorio_protofrases': rel })


### MAPEAMENTO ####################################################################################

def selecionarArquivoProtofrases(request):
    arq = request.POST['arquivo_selecionado']
    try:
       a = DadosMapeamentoEExtracao.objects.get(id=1)
       a.arquivo = arq
       a.save()
    except:
       DadosMapeamentoEExtracao.objects.create(id=1, arquivo=arq)
    messages.success(request, "Dados excluídos com sucesso.")
    dadoM = DadosMapeamentoEExtracao.objects.get(id=1)
    arquivo = dadoM.arquivo
    lista = open("extrator/arquivos/protofrases/" + arquivo).readlines()
    count = 0
    new2 = []
    for i in lista:
        if count > 2:
            new2.append(i.strip())
        count = count + 1
    str1 = ' '.join(new2)
    return render(request, 'extrator/extrator_home_6.html', {'dados_de_entrada': None, 'relatorio_preproc':None, 'proto_frases':new2 })

def selecionarProtoFrase(request):
    pf = request.POST['protofrase_selecionada']
    try:
       a = DadosMapeamentoEExtracao.objects.get(id=1)
       a.protofrase = pf.split(": ")[1]
       a.save()
    except:
       DadosMapeamentoEExtracao.objects.create(id=1, protofrase=pf.split(": ")[1])

    messages.success(request, "Protofrases carregadas.")
    return render(request, 'extrator/extrator_home_6.html', {'dados_de_entrada': None, 'relatorio_preproc':None })

def mapPrepararTextos(request):
    a = DadosMapeamentoEExtracao.objects.get(id=1)
    arq_dp = open("extrator/arquivos/doc_preproc.txt", "r")
    dp = arq_dp.read()
    dp = dp.split('.')
    a.num_sent_docPreproc = len(dp)
    a.save()
    arq_dlc = open("extrator/arquivos/doc_lematizado_csw.txt", "r")
    dlc = arq_dlc.read()
    dlc = dlc.split('.')
    a.num_sent_docPreprocLemCSW = len(dlc)
    a.save()
    arq_dls = open("extrator/arquivos/doc_preproc_ssw.txt", "r")
    dls = arq_dls.read()
    dls = dls.split('.')
    a.num_sent_docPreprocLemSSW = len(dls)
    a.save()
    if len(dp) != len(dlc) or len(dp) != len(dls) or len(dlc) != len(dls):
        messages.error(request, "Quantidade de sentenças não correspondem nos diferentes textos.")
        return render(request, 'extrator/extrator_home_6.html', {'dados_de_entrada': None, 'relatorio_preproc':None })

    MapeamentoEExtracaoTextos.objects.all().delete()
    count = 0
    while (count < len(dp)):
        MapeamentoEExtracaoTextos.objects.create(id = count, paragrafo = count + 1, doc_preproc=dp[count], doc_preprocLemCSSW=dlc[count], doc_preprocLemSSW=dls[count])
        count = count + 1
    messages.success(request, "Textos preparados.")
    return render(request, 'extrator/extrator_home_6.html', {'dados_de_entrada': None, 'relatorio_preproc':None })


def mapMapearProtofrase(request):
    ParagrafosExtraidos.objects.all().delete()
    a = DadosMapeamentoEExtracao.objects.get(id=1)
    bag_pf = a.protofrase.split(' ')
    paragrafos = []
    paragrafos2 = {}
    par_dict = {}
    protofrases_etapa2 ={}
    protofrase_original = a.protofrase
    dpls = MapeamentoEExtracaoTextos.objects.all()


    while (len(bag_pf) != 0):

        for prgf in dpls:
            bag_dpls = prgf.doc_preprocLemSSW.split(' ')
            bag_dpls = filter(None, bag_dpls)
            set_bag_dpls = set(bag_dpls)
            bag_pf = filter(None, bag_pf)
            set_bag_pf = set(bag_pf)
            inter = set_bag_pf.intersection(set_bag_dpls)
            inter = set_bag_pf.intersection(set_bag_dpls)
            print inter
            print set_bag_pf
            if len(inter) == len(set_bag_pf):

                paragrafos.append(prgf.paragrafo)


        if len(paragrafos) == 0:
            del bag_pf[-1]
            #print 1
            #inter2 = set_bag_pf.difference(inter)
            #for i in list(inter2):
            #    bag_pf.remove(i)

        if len(paragrafos) == 1:
            p = MapeamentoEExtracaoTextos.objects.get(paragrafo=paragrafos[0])
            str1 = ' '.join(bag_pf)
            ParagrafosExtraidos(arquivo=a.arquivo,paragrafo=p.doc_preproc, protofrase=str1, dataHora = time.strftime("%Y/%m/%d-%H:%M:%S"), etapa=1, protofrase_original=protofrase_original).save()

            break

        ### COMECA A ETAPA 2:

        if len(paragrafos) > 1:

            for i in paragrafos:
                sentenca = []
                p = MapeamentoEExtracaoTextos.objects.get(paragrafo=i)
                sentenca = p.doc_preprocLemSSW.split(' ')
                sentenca_final = sentenca
                sentenca_final = [word for word in sentenca if word in bag_pf]
                bag_pf_t = list(bag_pf)
                bag_pf_t2 = list(bag_pf)

                while (bag_pf_t != 0):
                    bag_pf_str = ' '.join(bag_pf_t)
                    sentenca_final_str = ' '.join(sentenca_final)
                    if bag_pf_str in sentenca_final_str:
                        qtd = bag_pf_str.split(' ')
                        break
                    else:
                        del bag_pf_t[-1]

                while (bag_pf_t2 != 0):
                    bag_pf_str2 = ' '.join(bag_pf_t2)
                    sentenca_final_str = ' '.join(sentenca_final)
                    if bag_pf_str2 in sentenca_final_str:
                        qtd2 = bag_pf_str2.split(' ')
                        if len(qtd2) > len(qtd):
                            paragrafos2[p.paragrafo] = len(qtd2)
                            protofrases_etapa2[p.paragrafo] = bag_pf_str2
                        else:
                            print 'socorro'
                            paragrafos2[p.paragrafo] = len(qtd)
                            protofrases_etapa2[p.paragrafo] = bag_pf_str
                        break
                    else:
                        del bag_pf_t2[0]

            abc = []
            abc = max(paragrafos2, key=lambda i: paragrafos2[i])
            maxval = max(paragrafos2.iteritems(), key=operator.itemgetter(1))[1]
            paragrafos_etapa2 = [k for k,v in paragrafos2.items() if v==maxval]

            if len(paragrafos_etapa2) == 0:
                messages.error(request, "Não foi possível extrair proto-frases.")
                break

            if len(paragrafos_etapa2) == 1:
                str1 = ' '.join(bag_pf)
                p = MapeamentoEExtracaoTextos.objects.get(paragrafo=paragrafos[0])
                ParagrafosExtraidos(arquivo=a.arquivo,paragrafo=p.doc_preproc, protofrase=protofrases_etapa2.values()[0], dataHora = time.strftime("%Y/%m/%d-%H:%M:%S"),etapa=2, protofrase_original=protofrase_original).save()
                break

            ### COMECA A ETAPA 3:
            if len(paragrafos_etapa2) > 1:
                #str1 = ' '.join(bag_pf)
                for i in paragrafos_etapa2:
                    p2 = MapeamentoEExtracaoTextos.objects.get(paragrafo=i)
                    p12 = p2.doc_preprocLemSSW.split(' ')
                    p12 =  filter(None, p12)
                    first = bag_pf[0]
                    dist = 0
                    for item in bag_pf:
                        count = 0
                        for palavra in p12:
                            if palavra == item:
                                dist = dist + count
                            count = count + 1
                    par_dict[i] = dist
                    ab = []
                    ab = max(par_dict, key=lambda i: par_dict[i])
                    maxval = max(par_dict.iteritems(), key=operator.itemgetter(1))[1]
                    keys = [k for k,v in par_dict.items() if v==maxval]

                for i in keys:
                    p = MapeamentoEExtracaoTextos.objects.get(paragrafo=i)
                    ParagrafosExtraidos(arquivo=a.arquivo,paragrafo=p.doc_preproc, protofrase=protofrases_etapa2[i], dataHora = time.strftime("%Y/%m/%d-%H:%M:%S"), etapa=3, protofrase_original=protofrase_original).save()
                break

    messages.success(request, "Parágrafo(s) extraído(s) com sucesso.")
    return render(request, 'extrator/extrator_home_6.html', {'dados_de_entrada': None, 'relatorio_preproc':None })

def gerarRelatorioFrasesExtraidas(request):
    nome =  ParagrafosExtraidos.objects.first()
    qtd = ParagrafosExtraidos.objects.all().count()
    dados = ParagrafosExtraidos.objects.all()
    arq = open("extrator/arquivos/paragrafos/extracao_" + nome.arquivo , "w")
    if qtd == 1:
        arq.write("Foi extraído 1 parágrafo.\n")
    else:
        arq.write("Foram extraídas " + str(qtd) + " parágrafos.\n")
    arq.write("Etapa de extração: " + str(nome.etapa) + "\n\n")
    arq.write("Proto-frase original: " + nome.protofrase_original.encode('utf-8') + "\n")
    arq.write("Proto-frase utilizada: " + nome.protofrase.encode('utf-8') + "\n\n")

    if qtd == 1:
        arq.write("Parágrafo:\n\n")
        arq.write(nome.paragrafo.encode('utf-8'))
    else:
        arq.write("Parágrafos:\n\n")
        for i in dados:
            arq.write(i.paragrafo + "\n")
    arq.close()

    rel = open("extrator/arquivos/paragrafos/extracao_" + nome.arquivo ,"r").read()
    return render(request, 'extrator/extrator_home_6.html', {'dados_de_entrada': None, 'relatorio_preproc':None, 'relatorio_ext': rel })


def mostra_tabela(request , tipo):
    if tipo == "graus":
        graus = open("extrator/arquivos/tabela_graus.txt","r").read()
        return render(request, 'extrator/extrator_home_4.html', {'tabela_graus': graus })
    if tipo == "bet":
        bet = open("extrator/arquivos/tabela_betweenness.txt","r").read()
        return render(request, 'extrator/extrator_home_4.html', {'tabela_bet': bet })
    if tipo == "closs":
        closs = open("extrator/arquivos/tabela_closeness.txt","r").read()
        return render(request, 'extrator/extrator_home_4.html', {'tabela_closs': closs })

def carrega_arq(request):
    new =[]
    for file in os.listdir("extrator/arquivos/protofrases/"):
        if file.endswith(".txt"):
            new.append(file)
    return render(request, 'extrator/extrator_home_6.html', {'arquivos': new })
