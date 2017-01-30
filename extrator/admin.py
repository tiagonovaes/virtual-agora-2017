from django.contrib import admin
from .models import TextoPreproc, DadosPreproc, ListaVertices, TabelaRanking, ProtoFrase, Sorteio, ListaDeAdjacencias, DadosProtofrases, DadosMapeamentoEExtracao, MapeamentoEExtracaoTextos, ParagrafosExtraidos

# Register your models here.


class TextoPreprocAdmin(admin.ModelAdmin):
  list_display = ['id', 'vertice_num','vertice']

class ListaVerticesAdmin(admin.ModelAdmin):
  list_display = ['id','index', 'node']


class DadosPreprocAdmin(admin.ModelAdmin):
  list_display = ['id','palavras_por_sentenca_lssw', 'palavras_por_sentenca_org','quantidade_de_sentencas','palavras_texto_original', 'palavras_texto_lematizado','palavras_texto_lematizado_ssw','nome_rel_protofrase']

class TabelaRankingAdmin(admin.ModelAdmin):
  list_display = ['vertice_nome','vertice_numero','grau','betweenness','closeness']

class ProtoFraseAdmin(admin.ModelAdmin):
  list_display = ['vertice_inicial','protofrase']

class SorteioAdmin(admin.ModelAdmin):
  list_display = ['posicao','vertice']

class ListaDeAdjacenciasAdmin(admin.ModelAdmin):
  list_display = ['vertice_i','vertice_f','peso']


class DadosProtofrasesAdmin(admin.ModelAdmin):
  list_display = ['protofrase','repeticao']
  ordering = ('-repeticao',)

class DadosMapeamentoEExtracaoAdmin(admin.ModelAdmin):
  list_display = ['arquivo','protofrase','num_sent_docPreproc','num_sent_docPreprocLemCSW','num_sent_docPreprocLemSSW','extracaoParagrafosEtapa1']

class MapeamentoEExtracaoTextosAdmin(admin.ModelAdmin):
  list_display = ['paragrafo','doc_preproc','doc_preprocLemCSSW','doc_preprocLemSSW']
  ordering = ('paragrafo',)

class ParagrafosExtraidosAdmin(admin.ModelAdmin):
  list_display = ['paragrafo', 'protofrase','protofrase_original','etapa','arquivo','dataHora']
  ordering = ('-dataHora',)




admin.site.register(ParagrafosExtraidos, ParagrafosExtraidosAdmin)
admin.site.register(MapeamentoEExtracaoTextos, MapeamentoEExtracaoTextosAdmin)
admin.site.register(DadosMapeamentoEExtracao, DadosMapeamentoEExtracaoAdmin)
admin.site.register(DadosProtofrases, DadosProtofrasesAdmin)
admin.site.register(ListaDeAdjacencias, ListaDeAdjacenciasAdmin)
admin.site.register(Sorteio, SorteioAdmin)
admin.site.register(TextoPreproc, TextoPreprocAdmin)
admin.site.register(ProtoFrase, ProtoFraseAdmin)
admin.site.register(DadosPreproc, DadosPreprocAdmin)
admin.site.register(ListaVertices, ListaVerticesAdmin)
admin.site.register(TabelaRanking, TabelaRankingAdmin)
