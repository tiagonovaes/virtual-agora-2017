# -*- coding: utf-8 -*-
from django.contrib import messages
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.views import generic
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import HttpResponseRedirect
from django.forms import modelformset_factory
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.models import User as AuthUser
from agoraunicamp.models import User as QuestionUser
from agoraunicamp.models import Tutorial
from .models import Topic, TopicAnswer, User, TopicAnswerForm
from agoraunicamp.decorators import term_required
from projetos.models import Projeto

@method_decorator(login_required(login_url='agora:login'), name='dispatch')
@method_decorator(term_required, name='dispatch')
class ForumHomeView(generic.ListView):
  template_name = 'forum/home.html'
  model = Topic

  def get_queryset(self):
    u = User.objects.get(user=self.request.user)
    return Topic.objects.filter(published='Sim',projeto__sigla=u.user.user.projeto).distinct()

  def get_context_data(self, **kwargs):
    context = super(ForumHomeView, self).get_context_data(**kwargs)
    u = User.objects.get(user=self.request.user)
    context['topic'] = Topic.objects.filter(published='Sim',projeto__sigla=u.user.user.projeto)
    context['answers'] = TopicAnswer.objects.filter(topic=context['topic']).order_by('-answer_date').reverse()
    context['answer_form'] = TopicAnswerForm()
    auth_user = self.request.user
    user = auth_user.user
    projeto_nome = Projeto.objects.filter(sigla=user.user.user.projeto).first()
    t = Tutorial.objects.get(user=user)
    context['tutorial'] = t.status
    context['req_user'] = self.request.user
    context['username'] = auth_user
    context['user'] = user
    context['topic_user'] = User.objects.get(user=auth_user)
    context['topic_users'] = TopicAnswer.objects.all()
    context['nickname'] = user.nickname
    context['projeto'] = projeto_nome.projeto
    context['sigla'] = user.projeto
    return context


@method_decorator(login_required(login_url='agora:login'), name='dispatch')
@method_decorator(term_required, name='dispatch')
class TopicView(generic.ListView):
  template_name = 'forum/home-topico.html'
  model = Topic

  def get_context_data(self, **kwargs):
    context = super(TopicView, self).get_context_data(**kwargs)
    context['topic'] = Topic.objects.get(id=self.kwargs['pk'])
    context['answers'] = TopicAnswer.objects.filter(topic=context['topic']).order_by('-answer_date').reverse()
    context['answer_form'] = TopicAnswerForm()
    auth_user = self.request.user
    user = auth_user.user
    projeto_nome = Projeto.objects.filter(sigla=user.user.user.projeto).first()
    context['req_user'] = self.request.user
    context['username'] = auth_user
    context['user'] = user
    context['topic_user'] = User.objects.get(user=auth_user)
    context['category'] = Category.objects.all()
    context['topic_users'] = TopicAnswer.objects.all()
    context['nickname'] = user.nickname
    context['projeto'] = projeto_nome.projeto
    context['sigla'] = user.projeto

    if TopicAnswer.objects.filter(user=context['topic_user'], topic=context['topic']).count():
      context['user_answered'] = True
    else:
      context['user_answered'] = False
    return context

def save_topic_answer(request, topic_id):
  topic = get_object_or_404(Topic, pk=topic_id)
  auth_user = AuthUser.objects.get(username=request.user)
  topic_user = User.objects.get(user=auth_user)
  answered_topic = TopicAnswer.objects.filter(user=topic_user, topic=topic).count()
  if answered_topic:
    error_message = 'Você já respondeu este tópico.'
    messages.error(request, error_message)
  else:
    answer = request.POST['text']
    if answer:
      answer_model = TopicAnswer(user=topic_user, topic=topic, text=answer)
      answer_model.save()
    else:
      messages.error(request, "Parece que você deixou o campo em branco. Por favor, tente novamente.")
  return HttpResponseRedirect(reverse('forum:topic', kwargs={'pk': topic_id}))

def save_topic_answer_home(request, topic_id):
  topic = get_object_or_404(Topic, pk=topic_id)
  auth_user = AuthUser.objects.get(username=request.user)
  topic_user = User.objects.get(user=auth_user)
  answered_topic = TopicAnswer.objects.filter(user=topic_user, topic=topic).count()
  if answered_topic:
    error_message = 'Você já respondeu este tópico.'
    messages.error(request, error_message)
  else:
    answer = request.POST['text']
    if answer:
      answer_model = TopicAnswer(user=topic_user, topic=topic, text=answer)
      answer_model.save()
    else:
      messages.error(request, "Parece que você deixou o campo em branco. Por favor, tente novamente.")
    return redirect(request.META['HTTP_REFERER']+"#area%s"%(topic_id))

def save_topic_answer_home_edit(request, topic_id):
  topic = get_object_or_404(Topic, pk=topic_id)
  auth_user = AuthUser.objects.get(username=request.user)
  topic_user = User.objects.get(user=auth_user)
  answered_topic = TopicAnswer.objects.filter(user=topic_user, topic=topic).delete()
  answer = request.POST['text']
  if answer:
      answer_model = TopicAnswer(user=topic_user, topic=topic, text=answer)
      answer_model.save()
  else:
      messages.error(request, "Parece que você deixou o campo em branco. Por favor, tente novamente.")

  return redirect(request.META['HTTP_REFERER']+"#area%s"%(topic_id))
