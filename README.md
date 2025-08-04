**OptiTrack ile Gerçek Zamanlı Konum Aktarımı**

Bu proje, OptiTrack hareket izleme sistemi üzerinden alınan konum verilerini Arduino’ya ve oradan da Bluetooth bağlantısı ile başka bir Arduino’ya gerçek zamanlı olarak aktarmak amacıyla geliştirilmiştir.

Sistemin temelinde, sahnede tanımlı bir nesnenin pozisyon bilgisi Python ile alınıp, seri port üzerinden Arduino’ya gönderilir. İlk Arduino bu veriyi Bluetooth üzerinden ikinci Arduino’ya iletir. Bu yapı sayesinde mobil veya kablosuz sistemlerde konum verisi paylaşımı mümkün hale gelir.

Sistemi kurmak için OptiTrack ile Gerçek Zamanlı Konum Paylaşımı Kılavuzu dosyasına göz atabilirsiniz.

Projede, OptiTrack’in resmi NatNet SDK’sını doğrudan kullanmak yerine, topluluk tarafından geliştirilmiş bir Python wrapper tercih edilmiştir.

🔗 Referans alınan GitHub reposu:
https://github.com/TimSchneider42/python-natnet-client
