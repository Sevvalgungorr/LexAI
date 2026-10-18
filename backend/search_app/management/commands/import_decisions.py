
import json
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError
#BaseCommand: Django'da özel terminal komutu oluşturmamızı sağlar.
#CommandError: Hata oluştuğunda anlamlı hata mesajı veri
from django.db import transaction
#transaction: Veritabanı işlemlerini güvenli bir bütün olarak yürütür

from backend.search_app.models import LegalDecision


class Command(BaseCommand):
    help = "Import legal decisions from a JSON file."
    # Django'nun hazır add_arguments metoduyla terminalden JSON dosyasının yolunu (file_path) alıyoruz.
    def add_arguments(self, parser):
        parser.add_argument(
            "file_path",
            type=str,
            help="Path to the JSON file containing legal decisions.",
        )

       # Django'nun hazır handle metodu, komut çalıştırıldığında asıl işlemleri başlatır.
    def handle(self, *args, **options):

        # Terminalden gelen dosya yolunu Python'un Path nesnesine dönüştürür.
        file_path = Path(options["file_path"])

        # Dosya mevcut değilse Django'nun CommandError sınıfıyla hata verir.
        if not file_path.is_file():
            raise CommandError(f"File not found: {file_path}")

        # JSON dosyasını açar ve içindeki verileri Python nesnelerine dönüştürür.
        try:
            with file_path.open("r", encoding="utf-8") as file:
                decisions = json.load(file)

        # Dosya okunamazsa veya JSON biçimi hatalıysa hata verir.
        except (OSError, json.JSONDecodeError) as error:
            raise CommandError(
                f"Could not read JSON file: {error}"
            ) from error

        # JSON verisinin liste (list) biçiminde olduğunu kontrol eder.
        if not isinstance(decisions, list):
            raise CommandError(
                "JSON file must contain a list of decisions."
            )

        # Her mahkeme kararında bulunması gereken zorunlu alanları tanımlar.
        required_fields = (
            "court",
            "case_number",
            "decision_number",
            "decision_date",
            "content",
        )

        # Eklenen ve tekrar ettiği için atlanan kararların sayaçlarını oluşturur.
        imported_count = 0
        skipped_count = 0

        try:
            # Django'nun atomic özelliği, hata oluşursa bu aktarımdaki kayıtları geri alır.
            with transaction.atomic():

                # JSON listesindeki kararları sıra numaralarıyla birlikte tek tek işler.
                for index, decision in enumerate(decisions, start=1):

                    # Her kararın sözlük (dict) biçiminde olduğunu kontrol eder.
                    if not isinstance(decision, dict):
                        raise CommandError(
                            f"Decision {index} must be a JSON object."
                        )

                    # Her kararın zorunlu alanlarını sırayla kontrol eder.
                    for field in required_fields:

                        # Alanın değeri string değilse hata verir.
                        if not isinstance(decision.get(field), str):
                            raise CommandError(
                                f"Decision {index}: '{field}' must be a string."
                            )

                        # Alan boşsa veya yalnızca boşluk içeriyorsa hata verir.
                        if not decision[field].strip():
                            raise CommandError(
                                f"Decision {index}: '{field}' cannot be empty."
                            )

                    # JSON verilerini Django'nun LegalDecision modeline aktarır.
                    # Böylece doğrulanabilir ve kaydedilebilir bir karar nesnesi oluşturur.
                    legal_decision = LegalDecision(
                        court=decision["court"].strip(),
                        case_number=decision["case_number"].strip(),
                        decision_number=decision["decision_number"].strip(),
                        decision_date=decision["decision_date"],
                        title=decision.get("title", ""),
                        content=decision["content"].strip(),
                        source_url=decision.get("source_url", ""),
                    )

                    # Django'nun hazır metoduyla verileri model kurallarına göre doğrular.
                    legal_decision.full_clean()

                    # Django ORM ile aynı mahkeme, esas ve karar numarasına
                    # sahip bir kaydın veritabanında bulunup bulunmadığını kontrol eder.
                    already_exists = LegalDecision.objects.filter(
                        court=legal_decision.court,
                        case_number=legal_decision.case_number,
                        decision_number=legal_decision.decision_number,
                    ).exists()

                    # Karar zaten kayıtlıysa sayacı artırır ve sonraki karara geçer.
                    if already_exists:
                        skipped_count += 1
                        continue

                    # Yeni kararı Django'nun save metoduyla veritabanına kaydeder.
                    legal_decision.save()

                    # Başarıyla eklenen karar sayısını bir artırır.
                    imported_count += 1

        # Bilerek oluşturduğumuz Django komut hatalarını değiştirmeden iletir.
        except CommandError:
            raise

        # Beklenmeyen hataları yakalar ve aktarımın başarısız olduğunu bildirir.
        except Exception as error:
            raise CommandError(
                f"Import failed. No decisions were saved: {error}"
            ) from error

        # Aktarım tamamlandığında eklenen ve atlanan karar sayılarını terminale yazdırır.
        self.stdout.write(
            self.style.SUCCESS(
                f"Imported: {imported_count}, skipped: {skipped_count}"
            )
        )
