from django.test import TestCase
from django.urls import reverse
from rest_framework import status


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
