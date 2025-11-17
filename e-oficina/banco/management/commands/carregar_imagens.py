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

        # implemente aqui a forma de carregar as imagens na tabela servico do app banco