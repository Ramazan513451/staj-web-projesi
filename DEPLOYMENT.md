# Proje Yayına Alma (Deployment) ve PostgreSQL'e Geçiş Rehberi

Bu belge, mevcut SQLite geliştirme veritabanından üretim (production) veya test (staging) ortamlarında PostgreSQL'e geçiş adımlarını açıklamaktadır.

## 1. Ortam Değişkenleri (.env)

Projede veritabanı bağlantısı `django-environ` paketi kullanılarak esnek hale getirilmiştir. PostgreSQL'e bağlanmak için projenin kök dizininde bulunan `.env` dosyasına (veya sunucunun ortam değişkenlerine) `DATABASE_URL` eklemeniz gerekmektedir.

Örnek `.env` yapılandırması:
```ini
# PostgreSQL kullanmak için aşağıdaki formatta kendi bilgilerinizi girin:
# postgres://KULLANICI_ADI:SIFRE@HOST:PORT/VERITABANI_ADI
DATABASE_URL=postgres://myuser:mypassword@localhost:5432/kurumsal_db
```

*Not:* `DATABASE_URL` tanımlı değilse, sistem otomatik olarak varsayılan geliştirme veritabanı olan SQLite'ı (`db.sqlite3`) kullanmaya devam eder. Ortamı bozmadan geliştirme yapabilirsiniz.

## 2. PostgreSQL Kurulumu ve Veritabanı Oluşturma

PostgreSQL sunucusunda projeniz için boş bir veritabanı oluşturun. Örnek SQL komutları:
```sql
CREATE DATABASE kurumsal_db;
CREATE USER myuser WITH PASSWORD 'mypassword';
ALTER ROLE myuser SET client_encoding TO 'utf8';
ALTER ROLE myuser SET default_transaction_isolation TO 'read committed';
ALTER ROLE myuser SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE kurumsal_db TO myuser;
```

## 3. Bağımlılıkların Kurulumu

Projedeki PostgreSQL adaptörü (`psycopg2-binary`) `requirements.txt` dosyasında yer almaktadır. Sunucuda tüm gereksinimlerin kurulduğundan emin olun:
```bash
pip install -r requirements.txt
```

## 4. Migration İşlemleri

PostgreSQL'e bağlandıktan sonra (yani `.env` güncellendikten sonra) veritabanı tablolarını oluşturmak için:
```bash
python manage.py migrate
```

Yeni bir Süper Admin (Yönetici) hesabı oluşturun:
```bash
python manage.py createsuperuser
```

*(Profil modülündeki varsayılan role 'editor' olarak atanabilir, ancak superuser komutuyla oluşturulan kullanıcılar admin paneline erişim sağladıktan sonra Django admin üzerinden rolünü 'admin' yapabilirsiniz veya projeye entegre özel bir script ile admin atayabilirsiniz.)*

## Dikkat Edilmesi Gereken Noktalar
- **Veri Taşıma:** SQLite'daki eski veriler PostgreSQL'e kendiliğinden aktarılmaz. Gerekirse eski veritabanından `python manage.py dumpdata` ile yedek alıp PostgreSQL'de `python manage.py loaddata` komutunu kullanarak verileri aktarabilirsiniz.
- **Güvenlik Ayarları:** Canlı ortamda `DEBUG = False` yapılmalı ve `.env` dosyasındaki `SECRET_KEY` güçlü bir değere ayarlanmalıdır. Ayrıca `ALLOWED_HOSTS` ayarının doğru domain/IP adreslerini içerdiğine dikkat edilmelidir.
