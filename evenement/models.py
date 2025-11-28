from django.db import models
from django.utils import timezone

class Evenement(models.Model):
    STATUT_CHOICES = [
        ('en_attente', 'En attente'),
        ('valide', 'Validé'),
        ('refuse', 'Refusé'),
    ]
    
    nom = models.CharField(max_length=200, verbose_name="Nom de l'événement")
    date = models.DateTimeField(verbose_name="Date et heure")
    description = models.TextField(verbose_name="Description")
    capacite = models.IntegerField(verbose_name="Capacité")
    statut = models.CharField(
        max_length=20, 
        choices=STATUT_CHOICES, 
        default='en_attente',
        verbose_name="Statut"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Dernière modification")
    
    class Meta:
        verbose_name = "Événement"
        verbose_name_plural = "Événements"
        ordering = ['-date']
    
    def __str__(self):
        return self.nom
    
    @property
    def est_valide(self):
        return self.statut == 'valide'
    
    @property
    def est_en_attente(self):
        return self.statut == 'en_attente'

class ImageEvenement(models.Model):
    evenement = models.ForeignKey(
        Evenement, 
        on_delete=models.CASCADE, 
        related_name='images',
        verbose_name="Événement"
    )
    image = models.ImageField(upload_to='evenements/%Y/%m/', verbose_name="Image")
    legende = models.CharField(max_length=200, blank=True, verbose_name="Légende")
    est_principale = models.BooleanField(default=False, verbose_name="Image principale")
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name="Date d'ajout")
    
    class Meta:
        verbose_name = "Image d'événement"
        verbose_name_plural = "Images d'événements"
        ordering = ['-est_principale', '-uploaded_at']
    
    def __str__(self):
        return f"Image de {self.evenement.nom}"
    
    def save(self, *args, **kwargs):
        # Si c'est l'image principale, retirer le flag des autres images
        if self.est_principale:
            ImageEvenement.objects.filter(
                evenement=self.evenement, 
                est_principale=True
            ).update(est_principale=False)
        super().save(*args, **kwargs)