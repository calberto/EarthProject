from core.models import Patrias
from django.db.models import Count

# Identificar nomes duplicados
duplicados = (
    Patrias.objects.values('nome')
    .annotate(total=Count('id'))
    .filter(total__gt=1)
)

print("Nomes duplicados:")
for d in duplicados:
    print(d['nome'])

# Remover duplicatas, mantendo apenas um registro por nome
for d in duplicados:
    duplicados_por_nome = Patrias.objects.filter(nome=d['nome'])
    duplicados_por_nome.exclude(id=duplicados_por_nome.first().id).delete()
