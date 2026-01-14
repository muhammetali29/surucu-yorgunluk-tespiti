# 🚗 Sürücü Yorgunluk Tespit Sistemi

Bu proje, sürücülerin yorgunluk ve uykululuk durumlarını **gerçek zamanlı** olarak tespit etmek amacıyla geliştirilmiştir.  
Görüntü işleme teknikleri kullanılarak sürücünün göz durumu analiz edilir ve tehlikeli durumlarda uyarı mekanizması devreye girer.

## 🎯 Projenin Amacı
Uzun süreli araç kullanımında oluşabilecek dikkat kaybı ve yorgunluğun erken tespit edilerek trafik kazalarının önlenmesine katkı sağlamaktır.

## 🧠 Kullanılan Yöntem
- Kamera üzerinden yüz ve göz tespiti
- Göz açıklık oranı (EAR – Eye Aspect Ratio) hesaplama
- Belirli bir eşik değerin altında gözlerin kapalı kalma süresinin ölçülmesi
- Yorgunluk durumunda sesli ve/veya görsel uyarı verilmesi

## 🛠️ Kullanılan Teknolojiler
- Python
- OpenCV
- Dlib
- NumPy

## ⚙️ Kurulum ve Çalıştırma
1. Projeyi bilgisayarınıza klonlayın:
   ```bash
   git clone https://github.com/muhammetali29/surucu-yorgunluk-tespiti.git
