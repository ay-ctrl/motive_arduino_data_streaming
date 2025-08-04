import time
import serial

# NatNetClient kütüphanesinden gerekli sınıflar içe aktarılıyor
from natnet_client import DataDescriptions, DataFrame, NatNetClient

# Veri gönderimi için başlangıç zaman damgası
prev = time.time()

# Arduino ile seri bağlantı kuruluyor (COM7 portu, 9600 baud hızında)
# COM port numarası Arduino'yu yeniden taktığında değişebilir, güncel portu kontrol et
ser = serial.Serial('COM7', 9600)
time.sleep(2)  # Arduino'nun bağlantı sonrası hazır olması için kısa gecikme

# Her yeni veri çerçevesi geldiğinde çağrılacak olan fonksiyon
def send_rigidbody_pos(data_frame: DataFrame):
    global prev
    current = time.time()  # Şu anki zaman kaydediliyor

    rb = data_frame.rigid_bodies[0]  # İlk rigid body (sert cisim) alınıyor

    # Eğer son gönderimden bu yana 0.05 saniyeden fazla geçmişse:
    if (current - prev) > 0.05:
        # Pozisyon bilgisi ve zaman damgası formatlanıyor
        position = f"[({rb.pos[0]:.6f},{rb.pos[1]:.6f},{rb.pos[2]:.6f}),{current}]"

        print(str(position))  # Terminale pozisyon yazdırılıyor
        ser.write(position.encode())  # Pozisyon bilgisi Arduino'ya seri port üzerinden gönderiliyor

        prev = current  # Son gönderim zamanı güncelleniyor

# Ana program buradan başlıyor
num_frames = 0
if __name__ == "__main__":
    # NatNetClient başlatılıyor: IP adresleri ve multicast ayarı yapılmış
    streaming_client = NatNetClient(
        server_ip_address="169.254.109.96",
        local_ip_address="169.254.109.96",
        use_multicast=False
    )

    # Gelen her veri çerçevesinde çalışacak olan fonksiyon belirtiliyor
    streaming_client.on_data_frame_received_event.handlers.append(send_rigidbody_pos)

    # NatNet istemcisi aktif hale getiriliyor
    with streaming_client:
        while True:
            streaming_client.update_sync()       # Veri senkronizasyonu
            streaming_client.request_modeldef()  # Model tanımı isteniyor (isteğe bağlı)

# Program sonunda seri port kapatılıyor
ser.close()
