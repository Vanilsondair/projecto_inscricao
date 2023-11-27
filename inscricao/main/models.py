from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Curso(models.Model):
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome  # Retorna o nome do curso como representação de texto

class Cadeira(models.Model):
    nome = models.CharField(max_length=100)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    horas = models.IntegerField()
    semestre = models.IntegerField()
    ano = models.IntegerField()

    def __str__(self):
        return self.nome



class Estudante(models.Model):
    nome = models.CharField(max_length=100)
    apelido = models.CharField(max_length=50)
    sexo = models.CharField(max_length=1, choices=[('M', 'Masculino'), ('F', 'Feminino')])
    celular = models.PositiveIntegerField()
    nascimento = models.DateField()
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    bi = models.CharField(max_length=13)
    ano_ingresso = models.DateField()
    email = models.EmailField()
    codigo_estudante = models.CharField(max_length=20, unique=True)  # Campo para o código do estudante
    
    # Adicione o campo "periodo"
    PERIODO_CHOICES = [
        ('D', 'Diurno'),
        ('N', 'Noturno'),
    ]
    periodo = models.CharField(max_length=1, choices=PERIODO_CHOICES)
    
    def __str__(self):
        return self.nome



class Inscricao(models.Model):
    estudante = models.ForeignKey(Estudante, on_delete=models.CASCADE)
    cadeira = models.ForeignKey(Cadeira, on_delete=models.CASCADE)
    data_inscricao = models.DateTimeField(auto_now_add=True)
    feito = models.BooleanField(default=False)
    codigo_estudante = models.CharField(max_length=20, blank=True)  # Campo para o código do estudante

    def save(self, *args, **kwargs):
        # Preencher o código do estudante automaticamente antes de salvar
        if not self.codigo_estudante:
            self.codigo_estudante = self.estudante.codigo_estudante
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.estudante} - {self.cadeira}"

# Sinal para preencher o código do estudante automaticamente quando uma inscrição é criada
@receiver(post_save, sender=Inscricao)
def preencher_codigo_estudante(sender, instance, **kwargs):
    if not instance.codigo_estudante:
        instance.codigo_estudante = instance.estudante.codigo_estudante
        instance.save()



class Configuracoes(models.Model):
    semestre_ativo = models.IntegerField(choices=[(1, '1º Semestre'), (2, '2º Semestre')])
    periodo_inscricao_aberto = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        # Verifique se o semestre ativo foi alterado
        if self.pk is not None:
            original = Configuracoes.objects.get(pk=self.pk)
            if self.semestre_ativo != original.semestre_ativo:
                self.semestre_ativo_changed = True
            else:
                self.semestre_ativo_changed = False
        else:
            self.semestre_ativo_changed = False
        super().save(*args, **kwargs)

def create_initial_config():
    # Verifique se já existe uma configuração inicial
    if not Configuracoes.objects.exists():
        config = Configuracoes.objects.create(semestre_ativo=1, periodo_inscricao_aberto=True)
        config.semestre_ativo_changed = False  # Sem alteração inicial
        config.save()

# Em algum lugar onde você inicia a configuração inicial do sistema:
create_initial_config()

