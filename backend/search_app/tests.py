import json
from pathlib import Path
from tempfile import TemporaryDirectory

from django.core.management import call_command
from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from backend.search_app.models import LegalDecision


# Arama API'sinin doğru çalışıp çalışmadığını kontrol eden test sınıfı
class SearchAPITests(TestCase):

    # Her testten önce çalışır ve API adresini hazırlar
    def setUp(self):
        # URL adından /api/search/ adresini bulur
        self.url = reverse("search-decisions")

    # TEST 1: Geçerli bir arama isteğinin kabul edilmesini kontrol eder
    def test_valid_search_request(self):

        # Django test istemcisiyle API'ye POST isteği gönderilir
        # Parantez içindeki veriler API'ye gönderilen örnek kullanıcı bilgileridir
        # API'nin döndürdüğü cevap response değişkenine kaydedilir
        response = self.client.post(
            self.url,
            {
                "query": "Haksız işten çıkarılma ile ilgili kararlar",
                "top_k": 5,
            },
            content_type="application/json",
        )

        # API'nin başarılı yanıt (200 OK) döndürdüğünü kontrol eder
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # API cevabındaki top_k değerinin 5 olduğunu kontrol eder
        self.assertEqual(response.json()["top_k"], 5)

    # TEST 2: Çok kısa arama metninin reddedilmesini kontrol eder
    def test_short_query_is_rejected(self):

        # En az 10 karakter şartını sağlamayan bir arama metni gönderilir
        response = self.client.post(
            self.url,
            {"query": "iş", "top_k": 5},
            content_type="application/json",
        )

        # Geçersiz isteğin 400 Bad Request ile reddedildiğini kontrol eder
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # TEST 3: İzin verilen karar sayısının aşılmasını kontrol eder
    def test_invalid_top_k_is_rejected(self):

        # top_k en fazla 20 olabilir; bilerek 30 gönderiyoruz
        response = self.client.post(
            self.url,
            {
                "query": "İş sözleşmesinin feshi hakkında kararlar",
                "top_k": 30,
            },
            content_type="application/json",
        )

        # API'nin geçersiz top_k değerini reddettiğini kontrol eder
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


# JSON dosyasından mahkeme kararı aktarma işlemini test eden sınıf
class ImportDecisionsTests(TestCase):

    # TEST 4: Geçerli JSON verisinin veritabanına kaydedildiğini kontrol eder
    def test_import_valid_decision(self):

        # Test için kurgusal bir mahkeme kararı oluşturur
        decisions = [
            {
                "court": "Ornek Hukuk Dairesi",
                "case_number": "TEST-2026/002",
                "decision_number": "TEST-2026/102",
                "decision_date": "2026-01-15",
                "title": "Ornek karar",
                "content": "Bu, otomatik test icin olusturulmus bir karardir.",
                "source_url": "",
            }
        ]

        # Python'un hazır TemporaryDirectory yapısıyla geçici klasör oluşturur
        # Test tamamlandığında bu klasör otomatik olarak silinir
        with TemporaryDirectory() as temporary_dir:

            # Geçici klasörde decisions.json dosyasının yolunu oluşturur
            file_path = Path(temporary_dir) / "decisions.json"

            # Örnek mahkeme kararını JSON dosyasına yazar
            with file_path.open("w", encoding="utf-8") as file:
                json.dump(decisions, file)

            # Django'nun hazır call_command fonksiyonuyla
            # import_decisions komutunu Python içerisinden çalıştırır
            call_command("import_decisions", str(file_path))

        # Django ORM ile veritabanındaki karar sayısını kontrol eder
        # Tam olarak 1 karar kaydedilmiş olmalıdır
        self.assertEqual(LegalDecision.objects.count(), 1)

        # Veritabanına kaydedilen ilk mahkeme kararını getirir
        legal_decision = LegalDecision.objects.first()

        # Kaydedilen mahkeme adının beklediğimiz değer olduğunu doğrular
        self.assertEqual(
            legal_decision.court,
            "Ornek Hukuk Dairesi"
        )
