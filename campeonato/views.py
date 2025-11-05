from django.shortcuts import render
from .models import Partida, Time
from django.db.models import Q

def lista_partidas(request):
    
    # [cite_start]--- Parte 1: Calcular a tabela de classificação (Não muda) [cite: 369-488] ---
    times = Time.objects.all()
    classificacao = []
    for time in times:
        stats = { 'time': time, 'P': 0, 'J': 0, 'V': 0, 'E': 0, 'D': 0, 'GP': 0, 'GC': 0, 'SG': 0 }
        partidas_time = Partida.objects.filter(partida_realizada=True).filter(
            Q(time_casa=time) | Q(time_visitante=time)
        )
        for partida in partidas_time:
            stats['J'] += 1
            if partida.time_casa == time:
                stats['GP'] += partida.gols_time_casa; stats['GC'] += partida.gols_time_visitante
                if partida.gols_time_casa > partida.gols_time_visitante:
                    stats['V'] += 1; stats['P'] += 3
                elif partida.gols_time_casa == partida.gols_time_visitante:
                    stats['E'] += 1; stats['P'] += 1
                else: stats['D'] += 1
            else:
                stats['GP'] += partida.gols_time_visitante; stats['GC'] += partida.gols_time_casa
                if partida.gols_time_visitante > partida.gols_time_casa:
                    stats['V'] += 1; stats['P'] += 3
                elif partida.gols_time_visitante == partida.gols_time_casa:
                    stats['E'] += 1; stats['P'] += 1
                else: stats['D'] += 1
        stats['SG'] = stats['GP'] - stats['GC']
        classificacao.append(stats)
    classificacao.sort(key=lambda item: (item['P'], item['V'], item['SG']), reverse=True)

    # --- Parte 2: Lógica do Filtro de Fase (Não muda) ---
    fase_selecionada = request.GET.get('fase', None)
    nomes_fases_dropdown = Partida.objects.order_by('fase').values_list('fase', flat=True).distinct()
    partidas_todas = Partida.objects.all().order_by('data_partida')

    if fase_selecionada and fase_selecionada in nomes_fases_dropdown:
        nomes_fases_para_agrupar = [fase_selecionada]
    else:
        nomes_fases_para_agrupar = nomes_fases_dropdown

    grupos_de_partidas = []
    for nome_fase in nomes_fases_para_agrupar:
        partidas_desta_fase = partidas_todas.filter(fase=nome_fase)
        if partidas_desta_fase.exists():
            grupos_de_partidas.append({ 'nome_fase': nome_fase, 'partidas': partidas_desta_fase })

    # --- PARTE 3: NOVA LÓGICA - "Últimos Resultados" e "Próximos Jogos" ---
    
    # 1. Busca os jogos da última rodada REALIZADA
    ultimos_resultados = []
    ultimo_jogo_realizado = Partida.objects.filter(partida_realizada=True).order_by('-data_partida').first()
    if ultimo_jogo_realizado:
        nome_fase_recente = ultimo_jogo_realizado.fase
        ultimos_resultados = Partida.objects.filter(
            fase=nome_fase_recente, partida_realizada=True
        ).order_by('data_partida')

    # 2. Busca os jogos da próxima rodada AGENDADA
    proximos_jogos = []
    proximo_jogo_agendado = Partida.objects.filter(partida_realizada=False).order_by('data_partida').first()
    if proximo_jogo_agendado:
        nome_proxima_fase = proximo_jogo_agendado.fase
        proximos_jogos = Partida.objects.filter(
            fase=nome_proxima_fase, partida_realizada=False
        ).order_by('data_partida')

    # --- Parte 4: Enviar TUDO para o template ---
    contexto = {
        'classificacao': classificacao,
        'grupos_de_partidas': grupos_de_partidas,
        'nomes_fases_dropdown': nomes_fases_dropdown, 
        'fase_selecionada': fase_selecionada,      
        'ultimos_resultados': ultimos_resultados, # NOVO: Apenas jogos realizados
        'proximos_jogos': proximos_jogos,         # NOVO: Apenas jogos agendados
    }
    
    return render(request, 'campeonato/lista_partidas.html', contexto)