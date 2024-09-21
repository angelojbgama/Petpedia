from django.db import models
from django.contrib.auth.models import AbstractUser
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from django.core.files.storage import default_storage
import os
from io import BytesIO
from django.core.files.base import ContentFile

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
    ESTADO_CHOICES = (
        ('pendente', 'Pendente'),
        ('aprovado', 'Aprovado'),
        ('rejeitado', 'Rejeitado'),
    )

    usuario_adotante = models.ForeignKey(USUARIO, on_delete=models.CASCADE, related_name='adocoes')
    pet = models.ForeignKey(PET, on_delete=models.CASCADE, related_name='solicitacoes_adocao')
    ong_adocao = models.ForeignKey(USUARIO, on_delete=models.CASCADE, related_name='solicitacoes_ong')
    data_solicitacao = models.DateTimeField(auto_now_add=True)
    estado_da_adocao = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='pendente')

    def __str__(self):
        return f'Solicitação de {self.usuario_adotante} para {self.pet}'
    
    def save(self, *args, **kwargs):
        
        super().save(*args, **kwargs)
        
        # Se a adoção for aprovada, marcar o pet como indisponível
        if self.estado_da_adocao == 'aprovado':
            self.pet.disponivel_adocao = False
            self.pet.save()

    def gerar_pdf_adocao(self):
        # Gerar o PDF na memória em vez de salvar no disco
        buffer = BytesIO()
        c = canvas.Canvas(buffer, pagesize=A4)

        # Conteúdo do PDF
        c.drawString(100, 800, "Detalhes da Adoção:")
        c.drawString(100, 780, f"Usuário Adotante: {self.usuario_adotante.username}")
        # Outros dados...

        c.showPage()
        c.save()

        # Salvar o PDF no sistema de arquivos do Django
        pdf_file = ContentFile(buffer.getvalue())
        filename = f'adocao_{self.id}.pdf'
        file_path = default_storage.save(f'adocoes_pdfs/{filename}', pdf_file)

        buffer.close()
