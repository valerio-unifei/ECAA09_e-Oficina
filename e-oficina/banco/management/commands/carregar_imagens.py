import os
from pathlib import Path
from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from django.conf import settings
from banco.models import Servico

class Command(BaseCommand):
    help = 'Popula Banco de dados com imagens de dados'

    def handle(self, *args, **options):
        image_folder = Path(settings.BASE_DIR) / 'static' / 'images' / 'danos'

        if not image_folder.exists():
            self.stdout.write(self.style.ERROR(f"Pasta de imagens não encontrada em: {image_folder}"))
            return

        self.stdout.write(f"Procurando imagens em {image_folder}...")

        lista_imagens = list(image_folder.glob('*.jpg'))
        self.stdout.write(f"Imagens encontradas: {len(lista_imagens)}")

        for i, caminho in enumerate(lista_imagens):
            nome_arquivo = f'/static/images/danos/{caminho.name}'
            if Servico.objects.filter(imagem=nome_arquivo).exists():
                self.stdout.write(self.style.WARNING(f"Servico '{nome_arquivo}' já existe. Pulando."))
                continue

            try:
                Servico.objects.create(carro=caminho.name, imagem=nome_arquivo, tipo='dano')
                self.stdout.write(self.style.SUCCESS(f"Produto '{nome_arquivo}' carregado com sucesso."))
            
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Erro ao carregar '{nome_arquivo}': {e}"))