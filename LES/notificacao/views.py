from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.utils.datetime_safe import datetime
from django.views.generic import View

from utilizadores.models import AuthUser, Utilizadortipo
from .forms import NotificacaoForm
from .models import Notificacao, Utilizador


class notificacao(View):
    template_name = 'notificacao.html'

    def get(self, request):
        form = NotificacaoForm()
        all_users = Utilizador.objects.all
        # ---------------get autenticated user
        user_id = request.user
        # utilizador_env = Utilizador.objects.get(pk=auth_user.id)
        utilizador_env = AuthUser.objects.get(pk=user_id.pk).utilizador
        print(utilizador_env)
        utilizadortipo = Utilizadortipo.objects.all
        # ----------------------
        return render(request, self.template_name, {'form': form,
                                                    'utilizador_env': utilizador_env,
                                                    'utilizadortipo': utilizadortipo,
                                                    'all_users': all_users,
                                                    })

    def post(self, request):
        form_notificacao = NotificacaoForm(request.POST)
        print(form_notificacao.errors)
        if form_notificacao.is_valid():
            print('asd')
            assunto = form_notificacao['assunto'].value()
            conteudo = form_notificacao['conteudo'].value()
            hora = datetime.now()
            prioridade = form_notificacao['prioridade'].value()
            # utilizador_env = form_notificacao['utilizador_env'].value()
            auth_user = request.user
            utilizador_env = AuthUser.objects.get(pk=auth_user.pk).utilizador
            # utilizador_env = Utilizador.objects.get(pk=1)
            # utilizador_env_value = form_notificacao.cleaned_data.get("utilizador_env")
            # print(utilizador_env_value)
            # utilizador_env = Utilizador.objects.get(nome=utilizador_env_value)
            utilizadortipo_value = request.POST['utilizadortipo']
            print(utilizadortipo_value)

            teste = form_notificacao['teste'].value()
            if Notificacao.objects.all().exists():
                notificacao_grupo = Notificacao.objects.last().notificacao_grupo + 1
            else:
                notificacao_grupo = 0
            if utilizadortipo_value != "escolher":
                print("1,2")
                print(teste)
                id_u = Utilizadortipo.objects.get(tipo=utilizadortipo_value)
                print(id_u)
                teste1 = Utilizador.objects.all().filter(utilizadortipo=id_u)
                print(teste1)
                for x in teste1:
                    print(x)
                    Notificacao.objects.create(assunto=assunto, conteudo=conteudo, hora=hora,
                                               prioridade=prioridade, utilizador_env=utilizador_env,
                                               utilizador_rec=x, notificacao_grupo=notificacao_grupo)
            else:
                utilizador_v = Utilizador.objects.all()
                # utilizador_email = utilizador_v.email
                print(utilizador_v)
                utilizador_rec = request.POST['utilizador_rec']
                utilizador_rec1 = Utilizador.objects.get(email=utilizador_rec)
                Notificacao.objects.create(assunto=assunto, conteudo=conteudo, hora=hora,
                                           prioridade=prioridade, utilizador_env=utilizador_env,
                                           utilizador_rec=utilizador_rec1, notificacao_grupo=notificacao_grupo)
        return redirect('/notificacao/consultar_notificacao/')


class Consultar_notificacao(View):
    template_name = 'consultar_notificacao.html'

    def get(self, request):
        lista_colab3 = []
        auth_user = request.user
        lista_notificacao_final = Notificacao.objects.filter(utilizador_env_id=AuthUser.objects.get(pk=auth_user.pk).utilizador)
        return render(request, self.template_name, {
            # 'form': form,
            # 'lista_colab': lista_colab,
            # 'hora_str': hora_str,
            # 'lista_colab3': lista_colab3,
            'lista_notificacao_final': lista_notificacao_final,
        })

    def post(self, request):
        post = request.POST
        id = post['del']
        print(id)
        Notificacao.objects.filter(pk=id).delete()
        return redirect('/notificacao/consultar_notificacao/')


class Editar_notificacao(View):
    template_name = 'editar_notificacao.html'

    def get(self, request, pk):
        form = NotificacaoForm()
        obj = Notificacao.objects.get(pk=pk)
        auth_user = request.user
        utilizador_env = AuthUser.objects.get(pk=auth_user.pk).utilizador
        if utilizador_env == obj.utilizador_env:
            if len(Notificacao.objects.filter(notificacao_grupo=obj.notificacao_grupo)) == 1:
                tiponotificacao = "notificação indvidual"
            elif len(Notificacao.objects.filter(notificacao_grupo=obj.notificacao_grupo)) > 1:
                tiponotificacao = "notificação grupo"
            return render(request, self.template_name, {
                'form': form,
                'obj': obj,
                'user_id': auth_user,
                'tiponotificacao': tiponotificacao,
            })
        else:
            return HttpResponse('<h1>Não lhe é permitido aceder a esta página</h1>')

    def post(self, request, pk):
        form_notificacao = NotificacaoForm(request.POST)
        print(form_notificacao.errors)
        if form_notificacao.is_valid():
            print('asd')
            assunto = form_notificacao['assunto'].value()
            conteudo = form_notificacao['conteudo'].value()
            hora = datetime.now()
            prioridade = form_notificacao['prioridade'].value()
            # utilizador_env = form_notificacao['utilizador_env'].value()
            auth_user = request.user
            utilizador_env = AuthUser.objects.get(pk=auth_user.pk).utilizador
            # utilizador_env = Utilizador.objects.get(pk=1)
            # utilizador_env_value = form_notificacao.cleaned_data.get("utilizador_env")
            # print(utilizador_env_value)
            # utilizador_env = Utilizador.objects.get(nome=utilizador_env_value)
            utilizadortipo_value = request.POST.get('utilizadortipo')
            print(utilizadortipo_value)
            teste = form_notificacao['teste'].value()
            notificacao = Notificacao.objects.get(pk=pk)
            notificacao2 = Notificacao.objects.filter(notificacao_grupo=notificacao.notificacao_grupo)
            if utilizadortipo_value != "escolher":
                for x in notificacao2:
                    x.conteudo = conteudo
                    x.hora = hora
                    x.prioridade = prioridade
                    x.assunto = assunto
                    x.save()
            else:
                notificacao.conteudo = conteudo
                notificacao.hora = hora
                notificacao.prioridade = prioridade
                notificacao.assunto = assunto
                notificacao.save()
        return redirect('/notificacao/consultar_notificacao/')
