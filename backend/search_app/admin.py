
from django.contrib import admin
from .models import LegalDecision


@admin.register(LegalDecision)
#modeli yönetim paketine ekledik 
class LegalDecisionAdmin(admin.ModelAdmin):
    # Yönetim panelinde listelenecek sütunlar
    list_display = (
        "court",
        "case_number",
        "decision_number",
        "decision_date",
        "created_at",
    )

    # Mahkeme ve tarihe göre filtreleme
    list_filter = ("court", "decision_date")

    # Kararlar arasında arama yapma
    search_fields = (
        "court",
        "case_number",
        "decision_number",
        "title",
        "content",
    )
