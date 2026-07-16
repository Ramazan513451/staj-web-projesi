# PROJE KURALLARI — Hazır Kurumsal Web Sitesi ve Yönetim Paneli (MTÜ)

Bu proje, Malatya Turgut Özal Üniversitesi "Hazır Kurumsal Web Sitesi ve Yönetim
Paneli" raporuna göre geliştiriliyor. Aşağıdaki kurallar HER adımda geçerlidir.
Açıkça belirtilmedikçe hiçbirinden sapma.

## Teknoloji ve Mimari (sabit — değiştirme)
- Backend: Python + Django (pip ile kurulacak en güncel kararlı sürüm; belirli
  bir versiyon pinlemene gerek yok).
- Frontend: HTML5, CSS3, vanilla JavaScript + Bootstrap 5 (CDN üzerinden dahil
  edilecek). npm/webpack gibi ayrı bir JS build sistemi KURULMAYACAK.
- Veritabanı: Geliştirmede SADECE SQLite. PostgreSQL'e geçiş yalnızca bunun
  için ayrılan adımda ele alınacak; aksi belirtilmedikçe PostgreSQL'e
  bağlanmaya veya ilgili paketleri fiilen kullanmaya çalışma.
- Mimari kesinlikle Django MVT: iş mantığı views.py'da, veri şeması ve temel
  model kuralları models.py'da, sunum templates/ klasöründe, yönlendirme
  urls.py'da.
- URL yapısı: herkese açık site kökte (`/`), yönetim paneli `/panel/` altında
  (örn. `/panel/login/`, `/panel/dashboard/`).
- Şablon motoru sadece Django Templates (DTL). React/Vue/Next.js gibi ayrı bir
  frontend framework KULLANMA.

## Kapsam Disiplini
- Sadece o anki adımda açıkça istenen dosyaları oluştur veya değiştir. Rapor
  ya da sohbette geçmeyen bir özelliği kendiliğinden ekleme; gerekli görürsen
  eklemeden önce bana sor.
- Blog Modülü ve Çoklu Dil (multi-language) desteği bu projenin kapsamı
  DIŞINDADIR (rapor bunları "ileride eklenecek" olarak işaretliyor) — bu
  özellikleri istenmeden ASLA ekleme.
- Önceki adımlarda tamamlanmış, çalışır durumdaki bir özelliği açıkça
  istenmeden değiştirme veya silme.

## Veritabanı Şeması (sabit alan adları — değiştirme, yeniden adlandırma)
- `Profile` (accounts app): user (User'a OneToOneField), role
  ('admin' | 'editor')
- `SiteSettings` (sitesettings app): site_title, logo, primary_color, address,
  phone, email, facebook_url, instagram_url, linkedin_url, map_iframe — tek
  kayıtlık (singleton) bir tablo olacak.
- `Page` (pages app): title, slug, content, is_published, created_at,
  updated_at
- `Service` (services app): title, image, description, is_featured, order
- `Slider` (sliders app): image, title, subtitle, is_active, order
- `ContactMessage` (contactmessages app): name, email, phone, message, status
  ('new' | 'read' | 'archived'), created_at
- Model değiştiren her adımdan sonra `makemigrations` + `migrate` çalıştır;
  migration dosyalarını elle düzenleme.

## Güvenlik (asla atlanmaz)
- `/panel/` altındaki HER view login_required (veya eşdeğer bir mixin) ile
  korunacak.
- HER formda Django'nun CSRF koruması (`{% csrf_token %}`) kullanılacak; CSRF
  middleware'ini kapatma.
- Şifreler SADECE Django'nun kendi auth/hashing sistemiyle saklanacak; asla
  düz metin, asla özel/manuel bir hash fonksiyonu yazma.
- role='editor' olan kullanıcılar Genel Ayarlar (SiteSettings) görünümüne ve
  URL'sine giremez. Bu kısıtlama view/decorator seviyesinde uygulanacak —
  linki sadece menüden gizlemek YETERLİ DEĞİL; URL adres çubuğuna doğrudan
  yazılsa bile 403 dönmeli.

## İş Kuralları (rapordan birebir — asla ihlal edilmez)
- ContactMessage kayıtları hiçbir zaman veritabanından silinemez; sadece
  status='read' veya status='archived' olarak güncellenebilir. Panelde bu
  model için delete butonu, view'ı veya URL'i BULUNMAYACAK.
- SiteSettings.logo, address, phone, email alanları boş kaydedilemez (model
  VE form seviyesinde zorunlu alan doğrulaması).
- Aynı anda en fazla 5 adet is_active=True Slider olabilir. 6. slider'ı
  aktive etmeye çalışan kullanıcıya açık ve anlaşılır bir hata mesajı
  gösterilecek (sessizce reddetme, sunucu hatası (500) verme).

## Süreç ve Doğrulama
- Her adımın sonunda `python manage.py check` hatasız çalışmalı ve
  `python manage.py runserver` sorunsuz ayağa kalkmalı; hata varsa
  "tamamlandı" deme, önce düzelt.
- Her adım, tarayıcıdan bağımsız olarak test edilebilir bir durumda bitmeli.
- Adım sonunda ne değiştiğini ve nasıl manuel test edeceğimi kısaca özetle.
- Rapor veya bu kurallarda net olmayan bir detayla karşılaşırsan (örn. eksik
  bir alan ya da belirsiz bir davranış), varsayım yapıp sessizce ilerlemek
  yerine bana sor.

## Kesinlikle Yapılmayacaklar
- Bu adımda istenmeyen bir paket/kütüphane kurmak.
- Migration dosyalarını elle düzenlemek.
- Veritabanını sıfırlamak veya `flush` etmek (açık onay almadan asla).
- `DEBUG`, `SECRET_KEY`, `ALLOWED_HOSTS` gibi production ayarlarını talimat
  gelmeden değiştirmek.
- Git geçmişine `force push` yapmak.
