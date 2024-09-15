from django.db import models
from django.contrib.auth.models import AbstractUser
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from django.core.files.storage import default_storage
import os

class USUARIO(AbstractUser):
    email = models.EmailField(unique=True)
    localidade = models.CharField(max_length=255, null=True, blank=True)
    telefone = models.CharField(max_length=15, blank=True, null=True)
    is_ong = models.BooleanField(default=False)
    nome_ong = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.username

class PET(models.Model):
    ESPECIES_CHOICES = (
        ('C', 'Cachorro'),
        ('G', 'Gato'),
    )

    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=100)
    especie = models.CharField(max_length=1, choices=ESPECIES_CHOICES)
    idade = models.PositiveIntegerField()
    vacinado = models.BooleanField(default=False)
    vacinas = models.TextField(blank=True)
    caracteristicas = models.TextField()
    foto = models.ImageField(upload_to='fotos_pets/', blank=True, null=True)
    dono = models.ForeignKey(USUARIO, on_delete=models.CASCADE, related_name='pets', null=True, blank=True)
    localidade = models.CharField(max_length=255, null=True, blank=True)
    disponivel_adocao = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.nome} - {self.get_especie_display()}'

    def save(self, *args, **kwargs):
        # Apenas ONGs podem cadastrar pets para adoção
        if self.dono and not self.dono.is_ong:
            raise ValueError("Apenas ONGs podem cadastrar pets para adoção.")
        super().save(*args, **kwargs)

class ADOCAO(models.Model):
    usuario_adotante = models.ForeignKey(USUARIO, on_delete=models.CASCADE, related_name='adocoes')
    pet = models.ForeignKey(PET, on_delete=models.CASCADE, related_name='solicitacoes_adocao')
    ong_adocao = models.ForeignKey(USUARIO, on_delete=models.CASCADE, related_name='solicitacoes_ong')
    data_solicitacao = models.DateTimeField(auto_now_add=True)
    estado_da_adocao = models.BooleanField(default=False)

    def __str__(self):
        return f'Solicitação de {self.usuario_adotante} para {self.pet}'

    def save(self, *args, **kwargs):
        # Verificar se o usuário não é uma ONG
        if self.usuario_adotante.is_ong:
            raise ValueError("ONGs não podem adotar pets.")
        
        super().save(*args, **kwargs)

        # Gerar PDF após salvar o objeto
        self.gerar_pdf_adocao()

    def gerar_pdf_adocao(self):
        # Caminho para salvar o PDF
        filename = f'adocao_{self.id}.pdf'
        directory = 'adocoes_pdfs'
        filepath = os.path.join(directory, filename)

        # Certificar-se de que o diretório existe
        if not os.path.exists(directory):
            os.makedirs(directory)

        # Criar canvas para o PDF
        c = canvas.Canvas(filepath, pagesize=A4)

        # Escrever no PDF
        c.drawString(100, 800, "Detalhes da Adoção:")
        c.drawString(100, 780, f"Usuário Adotante: {self.usuario_adotante.username}")
        c.drawString(100, 760, f"Email do Adotante: {self.usuario_adotante.email}")
        c.drawString(100, 740, f"Telefone do Adotante: {self.usuario_adotante.telefone}")
        c.drawString(100, 720, f"Pet Adotado: {self.pet.nome}")
        c.drawString(100, 700, f"Espécie do Pet: {self.pet.get_especie_display()}")
        c.drawString(100, 680, f"Ong Responsável: {self.ong_adocao.username}")  # Nome da ONG
        c.drawString(100, 660, f"Data da Solicitação: {self.data_solicitacao.strftime('%d/%m/%Y %H:%M')}")

        # Finalizar o PDF
        c.showPage()
        c.save()

        # Salvar o PDF usando o sistema de arquivos do Django
        with open(filepath, 'rb') as pdf_file:
            file_path = default_storage.save(f'{directory}/{filename}', pdf_file)

        # Remover o arquivo temporário
        os.remove(filepath)
