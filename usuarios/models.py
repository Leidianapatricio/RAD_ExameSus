from django.db import models


class Usuario(models.Model):

    TIPO_CHOICES = [
        ('CIDADAO', 'Cidadão'),
        ('SERVIDOR', 'Servidor'),
        ('ADMIN', 'Administrador'),
    ]

    nome = models.CharField(max_length=100)
    cpf = models.CharField(max_length=14, unique=True)
    tipo = models.CharField(
        max_length=20,
        choices=TIPO_CHOICES,
        default='CIDADAO'
    )

    def __str__(self):
        return self.nome