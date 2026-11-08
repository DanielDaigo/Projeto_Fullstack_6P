from django.db import migrations

def org_padrao(apps, schema_editor):
    Org = apps.get_model('core', 'Organizacao')
    Livro = apps.get_model('acervo', 'Livro')
    User = apps.get_model('auth', 'User')
    Perfil = apps.get_model('core', 'Perfil')

    org, _ = Org.objects.get_or_create(nome='Organização padrão')
    Livro.objects.filter(organizacao__isnull=True).update(organizacao=org)

    # Garante que todo usuário existente tenha perfil associado à organização padrão
    for user in User.objects.all():
        Perfil.objects.get_or_create(usuario=user, defaults={'organizacao': org})

class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
        ('acervo', '0002_livro_org_null'),
    ]

    operations = [
        migrations.RunPython(org_padrao, migrations.RunPython.noop),
    ]
