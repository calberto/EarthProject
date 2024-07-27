from django.db import models

class Continente(models.Model):
    nome = models.CharField(max_length=45)
    versao = models.IntegerField(blank=True, null=True)
    created_at = models.DateField()
    updated_at = models.DateField()

    def __str__(self):
        return self.nome
    
    class Meta:
        managed = False
        db_table = 'continentes'

class Patrias(models.Model):
    nome = models.CharField(max_length=45)
    capital = models.CharField(max_length=100)
    populacao = models.IntegerField()
    versao = models.IntegerField(blank=True, null=True)
    created_at = models.DateField()
    updated_at = models.DateField()
    flag = models.ImageField(upload_to='flags/')
    continentes = models.ForeignKey(Continente, models.DO_NOTHING)

    def __str__(self):
        return self.nome
    
    class Meta:
        managed = False
        db_table = 'patrias'
        unique_together = (('id', 'continentes'),)


class Estados(models.Model):
    nome = models.CharField(max_length=100)
    uf = models.CharField(max_length=4)
    versao = models.IntegerField(blank=True, null=True)
    flag = models.ImageField(upload_to='flags/')
    created_at = models.DateField(blank=True, null=True)
    updated_at = models.DateField()
    patrias = models.ForeignKey('Patrias', models.DO_NOTHING)

    def __str__(self):
        return self.nome
    
    class Meta:
        managed = False
        db_table = 'estados'

class Cidades(models.Model):
    nome = models.CharField(max_length=100)
    versao = models.IntegerField(blank=True, null=True)
    created_at = models.DateField()
    updated_at = models.DateField()
    estados = models.ForeignKey('Estados', models.DO_NOTHING)

    def __str__(self):
        return self.nome

    class Meta:
        managed = False
        db_table = 'cidades'

