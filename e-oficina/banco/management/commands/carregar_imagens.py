import os
from pathlib import Path
from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from django.conf import settings
from banco.models import Servico

class Command(BaseCommand):
    help = 'Popula Banco de dados com imagens de dados'

    def handle(self, *args, **options):
        # 1. Defina o caminho para a pasta de imagens
        # (Usando BASE_DIR do settings.py para construir o caminho)
        image_folder = Path(settings.BASE_DIR) / 'static' / 'images' / 'danos'

        if not image_folder.exists():
            self.stdout.write(self.style.ERROR(f"Pasta de imagens não encontrada em: {image_folder}"))
            return

        self.stdout.write(f"Procurando imagens em {image_folder}...")

        lista_imagens = list(image_folder.glob('*.png'))
        self.stdout.write(f"Imagens encontradas: {len(lista_imagens)}")

        # 2. Itere sobre os arquivos .png na pasta
        for i, caminho in enumerate(lista_imagens):
            # 3. Verifique se o produto já existe (opcional)
            if Servico.objects.filter(imagem=caminho).exists():
                self.stdout.write(self.style.WARNING(f"Servico '{caminho}' já existe. Pulando."))
                continue

            # 4. Abra o arquivo em modo binário
            try:
                Servico.objects.create(
                    carro=caminho,
                    imagem=caminho,
                    tipo = 'dano'
                )
                
                self.stdout.write(self.style.SUCCESS(f"Produto '{caminho}' carregado com sucesso."))
            
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Erro ao carregar '{caminho}': {e}"))