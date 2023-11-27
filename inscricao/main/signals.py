from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Configuracoes, Inscricao

@receiver(post_save, sender=Configuracoes)
def reset_inscricoes(sender, instance, **kwargs):
    if instance.semestre_ativo_changed:
        # Verifique se o semestre ativo foi alterado
        print("Semestre ativo alterado. Resetando inscrições.")
        Inscricao.objects.filter(feito=False).delete()

