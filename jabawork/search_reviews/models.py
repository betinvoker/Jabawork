from django.db import models

class Universities(models.Model):
    abbreviated = models.CharField(max_length=100, null=False)
    name = models.CharField(max_length=300, null=False)
    link = models.CharField(max_length=300, null=False)
    logo = models.CharField(max_length=50, null=False)
    link_universitiy = models.CharField(max_length=46, null=True)

    def __str__(self):
        return f"{self.id}, {self.abbreviated}, {self.name}, {self.link} , {self.logo}, {self.link_universitiy}"

class Opinions(models.Model):
    text = models.CharField(max_length=200000)
    date_opinion = models.CharField(max_length=40)
    opinion = models.CharField(max_length=5)
    university = models.ForeignKey(Universities, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.id}, {self.text}, {self.date_opinion}, {self.opinion}, {self.university}"