from django.db import models

class Time(models.Model):
    nome = models.CharField(max_length=100)
    #escudo = models.ImageField(upload_to='escudos/',blank=True, null=True)
    responsavel_nome = models.CharField(max_length=100)
    responsavel_contato = models.CharField(max_length=50)

    def __str__(self):
        return self.nome
    
class Partida(models.Model):
    fase = models.CharField(max_length=50, default="Fase de Grupos")
    time_casa = models.ForeignKey(Time, related_name='partidas_casa', on_delete=models.CASCADE)
    gols_time_casa = models.IntegerField(default=0)
    time_visitante = models.ForeignKey(Time, related_name='partidas_visitante',on_delete=models.CASCADE)
    gols_time_visitante = models.IntegerField(default=0)
    data_partida = models.DateTimeField()
    local = models.CharField(max_length=100)
    partida_realizada = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.time_casa} vs {self.time_visitante} - {self.data_partida.strftime('%d/%m/%Y')}"
