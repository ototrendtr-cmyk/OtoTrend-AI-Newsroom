# OtoTrend AI Newsroom

OtoTrendTR'nin haber toplama, AI editör, Instagram taslağı ve Telegram
bildirim sistemidir. Bu depo program kodunu ve marka görsellerini içerir;
parolalar, Telegram bilgileri, yerel haber veritabanı ve üretilmiş haber
görselleri özellikle depoya eklenmez.

## Yeni bilgisayarda hızlı kurulum (Windows)

Gerekenler:

- Git
- Python 3.11 veya daha yeni
- [Ollama](https://ollama.com/) (ücretsiz yerel AI için)

Komut İstemi veya PowerShell'de aşağıdaki adımları uygulayın:

```powershell
git clone https://github.com/ototrendtr-cmyk/OtoTrend-AI-Newsroom.git
cd OtoTrend-AI-Newsroom
py -3.11 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
Copy-Item .env.example .env
ollama pull gemma3:4b
```

Ardından `.env` dosyasını açın ve aşağıdaki değerleri kendi bilgilerinizle
doldurun:

- `SECRET_KEY`: uzun ve rastgele bir metin
- `ADMIN_USERNAME` ve `ADMIN_PASSWORD`: yeni bilgisayardaki yönetici girişi
- `TELEGRAM_BOT_TOKEN` ve `TELEGRAM_CHAT_ID`: mevcut Telegram bot bilgileriniz
- Yerel kurulum için `DATABASE_URL=sqlite:///news.db`
- `AI_PROVIDER=ollama` ve `OLLAMA_HOST=http://127.0.0.1:11434`

Programı başlatmak için:

```powershell
.\.venv\Scripts\python.exe -m uvicorn main:app --host 127.0.0.1 --port 8765
```

Tarayıcıdan `http://127.0.0.1:8765` adresini açın. İlk açılışta veritabanı
ve kaynak listesi otomatik oluşur. Yerel haber geçmişini de taşımak
isterseniz eski bilgisayardaki `news.db` dosyasını, uygulama kapalıyken, yeni
bilgisayardaki proje klasörüne kopyalayın. Bu dosya GitHub'a yüklenmez.

AI kuyruğu varsayılan olarak yalnızca son 24 saatte gelen haberleri işler.
Puanı 8 ve üzeri olanlar editör incelemesine düşer; bu eşikleri `.env`
dosyasındaki `AI_QUEUE_MAX_AGE_HOURS` ve `AI_REVIEW_MIN_IMPORTANCE`
değerleriyle değiştirebilirsiniz.

Bir kaynak art arda üç kez hata verirse otomatik olarak pasife alınır. Kaynak
Yönetimi ekranındaki “yeniden etkinleştir” düğmesiyle tekrar açılabilir.

## Otomatik çalışma ve saklama

Windows'ta oturum açınca arka planda çalıştırmak için
`scripts/start_ototrend.ps1` kullanılabilir. Haber saklama politikası varsayılan
olarak 90 gün sonra arşivler; bir yılı geçen arşivleri, önce yedek alarak,
temizler.

## Sunucu kurulumu

Docker ve sunucu kurulumu için [DEPLOYMENT.md](DEPLOYMENT.md) dosyasındaki
adımları izleyin. Sunucuda `.env` içindeki `DATABASE_URL` değeri
`sqlite:////data/news.db` olarak kalmalıdır.
