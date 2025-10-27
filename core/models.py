from django.db import models

class Continentes(models.Model):
    nome = models.CharField(max_length=45)
    versao = models.IntegerField(blank=True, null=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return self.nome
    
    class Meta:
        managed = True
        db_table = 'continentes'

class Patrias(models.Model):
    nome = models.CharField(max_length=255, unique=True)
    capital = models.CharField(max_length=100)
    populacao = models.BigIntegerField()
    versao = models.IntegerField(blank=True, null=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    continentes = models.ForeignKey(Continentes, models.DO_NOTHING)
    #continentes = models.ForeignKey(Continente, on_delete=models.CASCADE, default=1)  # Use um ID válido do continente
    flag = models.ImageField(upload_to='flags/', null=True)

    def __str__(self):
        return self.nome
    
    class Meta:
        managed = True
        db_table = 'patrias'
        unique_together = (('id', 'continentes'),)

class Estados(models.Model):
    nome = models.CharField(max_length=100)
    uf = models.CharField(max_length=4)
    patrias = models.ForeignKey('Patrias', models.DO_NOTHING)
    versao = models.IntegerField(blank=True, null=True)
    created_at = models.DateField(blank=True, null=True)
    updated_at = models.DateField()
    flag = models.ImageField(upload_to='flags/', null=True)    

    def __str__(self):
        return self.nome
    
    class Meta:
        managed = True
        db_table = 'estados'

class Cidades(models.Model):
    nome = models.CharField(max_length=100)
    estados = models.ForeignKey('Estados', models.DO_NOTHING)
    versao = models.IntegerField(blank=True, null=True)
    created_at = models.DateField()
    updated_at = models.DateField(auto_now=True)
    

    def __str__(self):
        return self.nome

    class Meta:
        managed = True
        db_table = 'cidades'
