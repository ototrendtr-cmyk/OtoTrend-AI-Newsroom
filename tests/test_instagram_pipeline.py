import json
import unittest
from datetime import datetime
from unittest.mock import patch

from app.ai.instagram_pipeline import process_instagram


class InstagramPipelineTests(unittest.TestCase):
    def test_composes_required_caption_sections_from_model_fields(self):
        model_draft = {
            "instagram_title": "Yeni Elektrikli Model Tanıtıldı",
            "photo_direction": "Aracın ön üç çeyrek görünümünü öne çıkar.",
            "intro": "Marka yeni elektrikli modelini duyurdu.",
            "details": [
                "Yeni modelin tanıtımı yapıldı.",
                "Araç elektrikli altyapı kullanıyor.",
                "Marka teknik ayrıntıları paylaştı.",
                "Haber resmi açıklamaya dayanıyor.",
            ],
            "editor_note": "Açıklama, markanın paylaştığı bilgilerle sınırlı.",
            "question": "Yeni modeli nasıl buldunuz",
            "hashtags": "#ElektrikliArac #OtoTrendTR",
            "validation_notes": [],
        }

        with patch(
            "app.ai.instagram_pipeline.instagram_chat",
            return_value=json.dumps(model_draft, ensure_ascii=False),
        ):
            draft, _ = process_instagram(
                "Marka yeni elektrikli modelini duyurdu. Araç elektrikli "
                "altyapı kullanıyor. Marka teknik ayrıntıları paylaştı.",
                source_name="Resmi Marka",
                published_at=datetime(2026, 8, 15),
                headline="Yeni Elektrikli Model Tanıtıldı",
            )

        self.assertIn("📊 ÖNE ÇIKAN DİKKAT ÇEKİCİ DETAYLAR:", draft["instagram_caption"])
        self.assertEqual(draft["instagram_caption"].count("🔹 "), 4)
        self.assertIn("💡 EDİTÖR NOTU:", draft["instagram_caption"])
        self.assertIn("Yorumlarda buluşalım! 👇", draft["instagram_caption"])
        self.assertIn("⚠️ Bilgilendirme: Reklam değildir.", draft["instagram_caption"])
        self.assertIn("📍 KAYNAKLAR: Resmi Marka (Ağustos 2026)", draft["instagram_caption"])
        self.assertIn("#OtoTrendTR", draft["hashtags"])


if __name__ == "__main__":
    unittest.main()
