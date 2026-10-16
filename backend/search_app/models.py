
from django.db import models


class LegalDecision(models.Model):
    # Kararı veren mahkeme (ör. Yargıtay 9. Hukuk Dairesi)
    court = models.CharField(max_length=255)

    # Kararın esas ve karar numaraları
    case_number = models.CharField(max_length=100)
    decision_number = models.CharField(max_length=100)

    # Kararın verildiği tarih
    decision_date = models.DateField()

    # Kararın başlığı (bazı kararlarda bulunmayabilir)
    title = models.CharField(max_length=500, blank=True)

    # Kararın tam metni
    content = models.TextField()

    # Kararın alındığı kaynak bağlantısı (isteğe bağlı)
    source_url = models.URLField(max_length=1000, blank=True)

    # Kaydın sistemimize eklendiği zaman
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.court} - {self.case_number} / {self.decision_number}"


