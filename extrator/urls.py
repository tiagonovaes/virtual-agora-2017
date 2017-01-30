from django.conf.urls import url

from . import views

app_name = 'extrator'
urlpatterns = [
  url(r'^extrator/$', views.ExtratorHomeView.as_view(), name='extratorHome'),

  url(r'^extrator/lematizar$', views.lematizar, name='lematizador'),
  url(r'^extrator/verarquivo/(?P<arquivo>[-\w]+)/$', views.ver_arquivo, name='ver_arquivo'),
  url(r'^extrator/dados$', views.inserir_dados_de_entrada, name='dados'),
  url(r'^extrator/stopwords$', views.eliminar_stopwords, name='stopwords'),
  url(r'^extrator/preproc$', views.pre_processamento, name='preproc'),
  url(r'^extrator/preprocsw$', views.preparar_lista_stopwords, name='preprocsw'),
  url(r'^extrator/salvar$', views.salvar_dados, name='salvar'),
  url(r'^extrator/relatorio$', views.gerar_relatorio, name='relatorio'),
  url(r'^extrator/preproccomp$', views.preproc_completo, name='preproc_comp'),
  url(r'^extrator/listavertices$', views.lista_de_vertices, name='lista_vertices'),
  url(r'^extrator/mapear$', views.mapear, name='mapear'),
  url(r'^extrator/matriz$', views.matriz, name='matriz'),
  url(r'^extrator/rede$', views.rede_complexa, name='rede_complexa'),
  url(r'^extrator/redecpmplexacomp$', views.redecomplexa_completo, name='redecomplexa_comp'),
  url(r'^extrator/logmetricas$', views.cria_log_metricas, name='logmetricas'),
  url(r'^extrator/gerartabelas$', views.gerar_tabelas_ranking, name='gerartabelas'),
  url(r'^extrator/metricaserankingcomp$', views.metricas_e_ranking_comp, name='metricas_e_ranking_comp'),
  url(r'^extrator/salvaverticeinicial$', views.salvaVerticeInicial, name='salva_vertice_inicial'),
  url(r'^extrator/gerarprotofrases$', views.gerar_proto_frases, name='gerarpfs'),
  url(r'^extrator/removerprotofrases$', views.removerProtoFrases, name='removerpfs'),
  url(r'^extrator/gerarrelatoriopfs$', views.gerarRelatorioDadosPfs, name='dados_protofrases'),
  url(r'^extrator/protofrases/salvaarquivo$', views.selecionarArquivoProtofrases, name='salva_arquivo'),
  url(r'^extrator/protofrases/salvaprotofrase$', views.selecionarProtoFrase, name='salva_protofrase'),
  url(r'^extrator/protofrases/mapeamento/preparartextos$', views.mapPrepararTextos, name='map_prepararTextos'),
  url(r'^extrator/protofrases/mapeamento/mapearprotofrase$', views.mapMapearProtofrase, name='map_mapearprotofrase'),
  url(r'^extrator/protofrases/mapeamento/gerarrelatorio$', views.gerarRelatorioFrasesExtraidas, name='rel_paragrafos'),
  url(r'^extrator/mostratabela/(?P<tipo>[-\w]+)/$', views.mostra_tabela, name='mostra_tabela'),
  url(r'^extrator/carregaarquivos/$', views.carrega_arq, name='carrega_arq'),
    #url(r'^atprojeto/(?P<projeto_nome>[-\w]+)/$', views.atualizaProjeto, name='atualiza-projeto'),
]
