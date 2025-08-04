import time
import serial

# NatNetClient'ten veri tanımları ve veri çerçevesi sınıfları içe aktarılıyor
from natnet_client import DataDescriptions, DataFrame, NatNetClient

# Önceki zaman damgası, veri gönderme aralığını kontrol etmek için kullanılır
prev = time.time()

# Arduino ile seri iletişim başlatılıyor (COM7 portu, 9600 baud)
# Not: Arduino'yu her bağladığında port değişebilir
ser = serial.Serial('COM7', 9600)
time.sleep(2)  # Arduino'nun hazır olması için kısa bir gecikme

# Bu fonksiyon, her yeni gelen veri çerçevesinde çağrılır
def send_rigidbody_pos(data_frame: DataFrame):
    global prev
    current = time.time()  # Şu anki zaman alınır

    rb = data_frame.rigid_bodies[0]  # İlk rigid body'si alınır

    # Eğer önceki gönderimden bu yana 0.05 saniyeden fazla geçmişse
    if (current - prev) > 0.05:
        # Pozisyon ve rotasyon bilgileri alınır ve biçimlendirilir
        position = f"({rb.pos[0]:.6f},{rb.pos[1]:.6f},{rb.pos[2]:.6f})"
        rotation = f"({rb.rot[0]:.6f},{rb.rot[1]:.6f},{rb.rot[2]:.6f},{rb.rot[3]:.6f})"
        data = f"[{position},{rotation},{current}]\n"

        print(str(position))  # Pozisyon terminale yazdırılır
        ser.write(data.encode())  # Arduino’ya veri gönderilir

        prev = current  # Son gönderim zamanı güncellenir

# Ana program başlangıcı
num_frames = 0
if __name__ == "__main__":
    # NatNetClient başlatılır; server ve local IP adresi ayarlanır
    streaming_client = NatNetClient(
        server_ip_address="169.254.109.96",
        local_ip_address="169.254.109.96",
        use_multicast=False
    )

    # Her veri çerçevesi geldiğinde çalışacak fonksiyon belirtilir
    streaming_client.on_data_frame_received_event.handlers.append(send_rigidbody_pos)

    # Veri akışı başlatılır ve sürekli olarak çerçeve alınır
    with streaming_client:
        while True:
            streaming_client.update_sync()       # Zaman senkronizasyonu yapılır
            streaming_client.request_modeldef()  # Model tanımı istenir (isteğe bağlı)

# Program sona erdiğinde seri port kapatılır
ser.close()
