from django.db import models

class Paciente(models.Model):
    nome = models.CharField(max_length=200)
    cpf = models.CharField(max_length=14, unique=True)
    whatsapp = models.CharField(max_length=20)
    data_cadastro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome

class Agendamento(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    data = models.DateField()
    exame = models.CharField(max_length=100) # Ex: Sangue Oculto
    status = models.CharField(max_length=20, default='Pendente')
    resultado_alerta = models.BooleanField(default=False) # Se a IA detectar perigo

    def __str__(self):
        return f"{self.paciente.nome} - {self.exame}"
