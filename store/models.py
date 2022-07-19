from django.db import models


class StateChoices(models.TextChoices):
    AC = ("AC", "Acre")
    AL = ("AL", "Alagoas")
    AP = ("AP", "Amapá")
    AM = ("AM", "Amazonas")
    BA = ("BA", "Bahia")
    CE = ("CE", "Ceará")
    DF = ("DF", "Distrito Federal")
    ES = ("ES", "Espírito Santo")
    GO = ("GO", "Goiás")
    MA = ("MA", "Maranhão")
    MT = ("MT", "Mato Grosso")
    MS = ("MS", "Mato Grosso do Sul")
    MG = ("MG", "Minas Gerais")
    PA = ("PA", "Pará")
    PB = ("PB", "Paraíba")
    PE = ("PE", "Pernambuco")
    PI = ("PI", "Piauí")
    RJ = ("RJ", "Rio de Janeiro")
    RN = ("RN", "Rio Grande do Norte")
    RS = ("RS", "Rio Grande do Sul")
    RO = ("RO", "Rondônia")
    RR = ("RR", "Roraima")
    SC = ("SC", "Santa Catarina")
    SP = ("SP", "São Paulo")
    SE = ("SE", "Sergipe")
    TO = ("TO", "Tocantins")
    NONE = ("NONE", "undefined")


class Store(models.Model):

    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=50)
    state = models.CharField(
        max_length=20, choices=StateChoices.choices, default=StateChoices.NONE
    )
    is_active = models.BooleanField(default=True)
