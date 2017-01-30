# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import User, Answer, Termo, MeuEspaco, Message, Tutorial
from django.http import HttpResponse
from django.core import serializers
from django.shortcuts import render
from django.utils import timezone
# Register your models here.




class AnswerAdmin(admin.ModelAdmin):
  actions = ['show_results']
  list_display = ['userd','user_stf','user_inst','question', '__str__']
  list_filter = ['question','user__institute','user__staff' ]

  def show_results(self, request, queryset):
    response = HttpResponse(content_type="application/json")
    serializers.serialize("json", queryset, stream=response)
    return render(request, 'admin/resultados_admin.html', {'objects': queryset} )
  show_results.short_description = "Mostrar resultados"


class TermoAdmin(admin.ModelAdmin):
  list_display = ['userd', 'condition']

class TutorialAdmin(admin.ModelAdmin):
  list_display = ['userd', 'status']

class MeuEspacoAdmin(admin.ModelAdmin):
  list_filter = ['projeto']
  list_display = ['projeto','user', 'secao', 'categoria', 'publ_date','comentario','link','arquivo']

class MessageAdmin(admin.ModelAdmin):
    actions=['publicar_no_mural','desfazer_publicacao_no_mural','remover_mensagem']
    fields = ['projeto','kind','message','address','publ_date']
    list_display = ['projeto','kind','message','published','publ_date','address']
    list_filter = ['projeto']
    def publicar_no_mural(modeladmin, request, queryset):
            queryset.update(published = 'Sim')
            queryset.update(publ_date = timezone.now())
            return

    def desfazer_publicacao_no_mural(modeladmin, request, queryset):
            queryset.update(published = 'Nao')
            return

    def remover_mensagem(modeladmin, request, queryset):
        if queryset.count() != 1:
            modeladmin.message_user(request, "Não é possível remover mais de uma mensagem por vez.")
            return
        else:
            queryset.delete()
        return



admin.site.register(Answer, AnswerAdmin)
admin.site.register(Termo, TermoAdmin)
admin.site.register(Tutorial, TutorialAdmin)
admin.site.register(MeuEspaco, MeuEspacoAdmin)
admin.site.register(Message, MessageAdmin)
