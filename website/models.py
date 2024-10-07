from django.db import models

class Contato(models.Model):
    nome = models.CharField(max_length=100, null=True)
    sobrenome = models.CharField(max_length=100, null=True)
    endereco = models.TextField(blank=True, null=True)
    email = models.EmailField(null=True)
    mensagem = models.TextField(blank=True, null=True)
    receber_noticias = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.nome} {self.sobrenome}'
