from django.contrib import admin
from django.utils.html import format_html
from django.db.models import Count
from .models import Evenement, ImageEvenement

class ImageEvenementInline(admin.TabularInline):
    model = ImageEvenement
    extra = 1
    readonly_fields = ['apercu_image']
    
    def apercu_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="100" />', obj.image.url)
        return "Pas d'image"
    apercu_image.short_description = "Aperçu"

@admin.register(Evenement)
class EvenementAdmin(admin.ModelAdmin):
    list_display = ['nom', 'date', 'capacite', 'statut_badge', 'nombre_images', 'created_at']
    list_filter = ['statut', 'date', 'created_at']
    search_fields = ['nom', 'description']
    date_hierarchy = 'date'
    inlines = [ImageEvenementInline]
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Informations principales', {
            'fields': ('nom', 'date', 'description', 'capacite')
        }),
        ('Validation', {
            'fields': ('statut',),
            'classes': ('wide',)
        }),
        ('Métadonnées', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['valider_evenements', 'refuser_evenements', 'mettre_en_attente']
    
    def statut_badge(self, obj):
        colors = {
            'en_attente': '#fbbf24',  # jaune
            'valide': '#22c55e',      # vert
            'refuse': '#ef4444',       # rouge
        }
        color = colors.get(obj.statut, '#6b7280')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; '
            'border-radius: 3px; font-weight: bold;">{}</span>',
            color,
            obj.get_statut_display()
        )
    statut_badge.short_description = 'Statut'
    
    def nombre_images(self, obj):
        count = obj.images.count()
        if count == 0:
            return format_html('<span style="color: red;">Aucune image</span>')
        return format_html('<span style="color: green;">{} image(s)</span>', count)
    nombre_images.short_description = 'Images'
    
    def valider_evenements(self, request, queryset):
        updated = queryset.update(statut='valide')
        self.message_user(request, f'{updated} événement(s) validé(s).')
    valider_evenements.short_description = "✓ Valider les événements sélectionnés"
    
    def refuser_evenements(self, request, queryset):
        updated = queryset.update(statut='refuse')
        self.message_user(request, f'{updated} événement(s) refusé(s).')
    refuser_evenements.short_description = "✗ Refuser les événements sélectionnés"
    
    def mettre_en_attente(self, request, queryset):
        updated = queryset.update(statut='en_attente')
        self.message_user(request, f'{updated} événement(s) mis en attente.')
    mettre_en_attente.short_description = "⏸ Mettre en attente"
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.annotate(images_count=Count('images'))
        return qs

@admin.register(ImageEvenement)
class ImageEvenementAdmin(admin.ModelAdmin):
    list_display = ['evenement', 'apercu', 'legende', 'est_principale', 'uploaded_at']
    list_filter = ['est_principale', 'uploaded_at']
    search_fields = ['evenement__nom', 'legende']
    readonly_fields = ['apercu_grande']
    
    def apercu(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" style="object-fit: cover;" />', obj.image.url)
        return "Pas d'image"
    apercu.short_description = "Aperçu"
    
    def apercu_grande(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="400" />', obj.image.url)
        return "Pas d'image"
    apercu_grande.short_description = "Image"