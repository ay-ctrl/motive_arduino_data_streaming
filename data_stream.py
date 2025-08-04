import time
import serial

from natnet_client import DataDescriptions, DataFrame, NatNetClient

# Veri gönderimi aralığını kontrol etmek için başlangıç zamanı
prev = time.time()

# Arduino ile seri bağlantı kuruluyor (COM7 portu, 9600 baud hızı)
ser = serial.Serial('COM7', 9600)
time.sleep(2)  # Arduino'nun açıldıktan sonra hazır olması için beklenir

# Unlabeled marker'ların konumlarını sürekli yazdırır
def recieve_unlabeled_marker_frame(data_frame: DataFrame):
    markers = data_frame.unlabeled_markers_pos
    for marker in markers:
        print(f"Marker: X={marker[0]:.2f}, Y={marker[1]:.2f}, Z={marker[2]:.2f}")

# İki veri çerçevesi arasındaki süreyi ölçmek için kullanılabilir
def measure_time():
    global prev
    current = time.time()
    if prev is not None:
        delta = current - prev
        print("Frame arası süre: ", delta)
    prev = current

# Labeled marker'ları yazdırır ve 1 saniyede bir seri porta gönderir
def receive_labeled_marker_frame(data_frame: DataFrame):
    print("Labeled Rigid Bodies: ")
    for rb in data_frame.rigid_bodies:
        global prev
        current = time.time()
        if current - prev >= 1.0:
            print(f"Rigid body id: {rb.id_num}")
            print(f"Position: X={rb.pos[0]:.2f}, Y={rb.pos[1]:.2f}, Z={rb.pos[2]:.2f}")
            print(f"Rotation: {rb.rot}")
            print("Markers (Rigid Body): \n")

            # ID bilgisi seri porta gönderiliyor
            bdata = f"Rigid body id: {rb.id_num}\n"
            ser.write(bdata.encode())

            # Marker pozisyonları gönderiliyor
            for i, marker in enumerate(rb.markers):
                data = f"Marker {i}: X={marker.pos[0]:.2f}, Y={marker.pos[1]:.2f}, Z={marker.pos[2]:.2f}\n"
                print(data)
                ser.write(data.encode())

            print("-")
            prev = current

# Verileri direkt seri porta gönderir (string olarak yapılandırılmış)
def receive_and_send_data(data_frame: DataFrame):
    global prev
    current = time.time()
    if current - prev >= 1.0:
        data = "("
        for rb in data_frame.rigid_bodies:
            idn = rb.id_num
            rot = f"({rb.rot[0]:.2f},{rb.rot[1]:.2f},{rb.rot[2]:.2f})"
            pos = f"({rb.pos[0]:.2f},{rb.pos[1]:.2f},{rb.pos[2]:.2f})"
            marks = "["
            for i, marker in enumerate(rb.markers):
                mar = f"({i},{marker.pos[0]:.2f},{marker.pos[1]:.2f},{marker.pos[2]:.2f})"
                marks += mar
            marks += "]"
            data += f"[{idn},{rot},{pos},{marks}],"
        data += ")\n"

        ser.write(data.encode())  # Veriler Arduino'ya gönderilir
        prev = current

# Gerçek zamanlı veri akışı için kullanılabilir, sürekli gönderir
def send_real_time_data(data_frame: DataFrame):
    data = "("
    for rb in data_frame.rigid_bodies:
        idn = rb.id_num
        rot = f"({rb.rot[0]:.2f},{rb.rot[1]:.2f},{rb.rot[2]:.2f})"
        pos = f"({rb.pos[0]:.2f},{rb.pos[1]:.2f},{rb.pos[2]:.2f})"
        marks = "["
        for i, marker in enumerate(rb.markers):
            mar = f"({i},{marker.pos[0]:.2f},{marker.pos[1]:.2f},{marker.pos[2]:.2f})"
            marks += mar
        marks += "]"
        data += f"[{idn},{rot},{pos},{marks}],"
    data += ")\n"

    ser.write(data.encode())

# Yeni tanımlanan veri açıklamaları geldiğinde çalışır
def receive_new_desc(desc: DataDescriptions):
    print("Received data descriptions.")
    # print(desc)  # Dilersen açabilirsin

# Ana uygulama başlangıcı
num_frames = 0
if __name__ == "__main__":
    streaming_client = NatNetClient(
        server_ip_address="169.254.109.96",
        local_ip_address="169.254.109.96",
        use_multicast=False
    )

    # Yeni tanım geldiğinde çalışacak fonksiyon
    streaming_client.on_data_description_received_event.handlers.append(receive_new_desc)

    # Veri çerçevesi geldiğinde çalışacak fonksiyonlardan biri (aktif olan)
    streaming_client.on_data_frame_received_event.handlers.append(receive_and_send_data)

    # Alternatif olarak aşağıdakileri kullanabilirsin:
    # streaming_client.on_data_frame_received_event.handlers.append(receive_labeled_marker_frame)
    # streaming_client.on_data_frame_received_event.handlers.append(send_real_time_data)

    with streaming_client:
        while True:
            streaming_client.update_sync()
            streaming_client.request_modeldef()

# Uygulama kapatıldığında seri port kapatılır
ser.close()
