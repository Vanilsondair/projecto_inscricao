from django.shortcuts import render
from .models import *
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect

@login_required(login_url='login')
def lista_cadeiras(request):
    # Obtém o semestre ativo a partir das configurações
    configuracoes = Configuracoes.objects.first()
    semestre_ativo = configuracoes.semestre_ativo
    periodo_inscricao_aberto = configuracoes.periodo_inscricao_aberto
    
    # Filtra as cadeiras do semestre ativo
    codigo_estudante = request.user.username
    estudante = Estudante.objects.get(codigo_estudante=codigo_estudante)

    # Verifique se algum dos formulários de inscrição foi enviado
    if request.method == 'POST':
        submeter_formulario(request, estudante)

    # Filtra as cadeiras do semestre ativo e ano
    primeiro_ano_cadeiras = get_cadeiras_por_ano(estudante, 1, semestre_ativo)
    segundo_ano_cadeiras = get_cadeiras_por_ano(estudante, 2, semestre_ativo)
    terceiro_ano_cadeiras = get_cadeiras_por_ano(estudante, 3, semestre_ativo)
    quarto_ano_cadeiras = get_cadeiras_por_ano(estudante, 4, semestre_ativo)

    # Obtém as inscrições do estudante
    inscricoes_estudante = Inscricao.objects.filter(estudante=estudante)

    # Crie um conjunto de IDs das cadeiras em que o estudante já está inscrito
    cadeiras_inscritas = set(inscricao.cadeira_id for inscricao in inscricoes_estudante)

    # Filtra apenas as cadeiras que o estudante ainda não está inscrito
    primeiro_ano_cadeiras = filter_cadeiras_nao_inscritas(primeiro_ano_cadeiras, cadeiras_inscritas)
    segundo_ano_cadeiras = filter_cadeiras_nao_inscritas(segundo_ano_cadeiras, cadeiras_inscritas)
    terceiro_ano_cadeiras = filter_cadeiras_nao_inscritas(terceiro_ano_cadeiras, cadeiras_inscritas)
    quarto_ano_cadeiras = filter_cadeiras_nao_inscritas(quarto_ano_cadeiras, cadeiras_inscritas)
    

      # Obter o estudante com base no usuário autenticado
    estudante = Estudante.objects.get(codigo_estudante=request.user.username)

    # Consultar as inscrições com base no estudante
    inscricoes = Inscricao.objects.filter(estudante=estudante)

    # Calcular a soma das horas
    total_horas = sum(inscricao.cadeira.horas for inscricao in inscricoes)
    print("total de horas",total_horas)  # Adicione esta linha para debug

    context = {
        'primeiro_ano_cadeiras': primeiro_ano_cadeiras,
        'segundo_ano_cadeiras': segundo_ano_cadeiras,
        'terceiro_ano_cadeiras': terceiro_ano_cadeiras,
        'quarto_ano_cadeiras': quarto_ano_cadeiras,
        'periodo_inscricao_aberto': periodo_inscricao_aberto,
        'total_horas': total_horas,  # Adicione o total de horas ao contexto
    }

    return render(request, 'main/index.html', context)

def submeter_formulario(request, estudante):
    form_name_mapping = {
        'submeter_primeiro_ano': 1,
        'submeter_segundo_ano': 2,
        'submeter_terceiro_ano': 3,
        'submeter_quarto_ano': 4,
    }
    
    form_name = next((name for name in form_name_mapping if name in request.POST), None)

    if form_name:
        ano = form_name_mapping[form_name]
        cadeiras_selecionadas = request.POST.getlist('cadeira_selecionada')
        
        for cadeira_id in cadeiras_selecionadas:
            inscricao = Inscricao(estudante=estudante, cadeira_id=cadeira_id)
            inscricao.save()

def get_cadeiras_por_ano(estudante, ano, semestre):
    return Cadeira.objects.filter(curso=estudante.curso, ano=ano, semestre=semestre)

def filter_cadeiras_nao_inscritas(cadeiras, cadeiras_inscritas):
    return cadeiras.exclude(id__in=cadeiras_inscritas)



@login_required(login_url='login')
def cadeiras_feitas(request):
    # Obter o estudante com base no usuário autenticado
    estudante = Estudante.objects.get(codigo_estudante=request.user.username)

    # Consultar as inscrições com base no estudante
    inscricoes = Inscricao.objects.filter(estudante=estudante)

    # Calcular a soma das horas
    total_horas = sum(inscricao.cadeira.horas for inscricao in inscricoes)
    print("total de horas",total_horas)  # Adicione esta linha para debug
    context = {
        'cadeiras_feitas': inscricoes,
        'total_horas': total_horas,
    }

    return render(request, 'main/cadeiras.html', context)



@login_required(login_url='login')
def excluir_cadeira(request, inscricao_id):
    inscricao = get_object_or_404(Inscricao, id=inscricao_id)
    
    # Verificar se o código do estudante associado à inscrição é igual ao código do usuário logado
    if request.user.username == inscricao.codigo_estudante:
        inscricao.delete()

    return redirect('cadeiras')
