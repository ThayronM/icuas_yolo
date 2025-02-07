import os
import cv2
import numpy as np
from ultralytics import YOLO
from collections import defaultdict

class VideoProcessor:
    def __init__(self, video_source, model_path, output_video="output/processed.mp4"):
        self.cap = cv2.VideoCapture(video_source)
        self.model = YOLO(model_path)
        self.track_history = defaultdict(lambda: [])
        self.class_points = defaultdict(list)
        self.class_points_mm = defaultdict(list)
        self.seguir = True
        self.field_reference = None

        # Criar pasta de saída
        os.makedirs("output", exist_ok=True)

        # Verificar se o vídeo foi aberto corretamente
        if not self.cap.isOpened():
            print(f"Erro: Não foi possível abrir o vídeo '{video_source}'")
            exit()

        # Configurar saída de vídeo
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")  # Codec MP4
        fps = int(self.cap.get(cv2.CAP_PROP_FPS)) or 30  # FPS padrão se não for detectado
        width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.out = cv2.VideoWriter(output_video, fourcc, fps, (width, height))

    def process_frame(self, img):
        if img is None:
            return None
        
        # Inicializa todas as classes com (0,0) no início do frame
        for classe in ["Yellow Robot", "Blue Robot", "Ball"]:
            self.class_points_mm[classe].append((0, 0))

        if self.seguir:
            results = self.model.track(img, persist=True, verbose=False)
        else:
            results = self.model(img)

        for result in results:
            img = result.plot()
            try:
                boxes = result.boxes.xywh.cpu().numpy()
                track_ids = result.boxes.id.int().cpu().tolist()
                class_idxs = result.boxes.cls.cpu().tolist()

                for box, track_id, class_idx in zip(boxes, track_ids, class_idxs):
                    x, y, w, h = box
                    track = self.track_history[track_id]
                    track.append((float(x), float(y)))
                    if len(track) > 30:
                        track.pop(0)

                    classe = result.names[class_idx]
                    self.class_points[classe].append((float(x), float(y)))
                    points = np.hstack(track).astype(np.int32).reshape((-1, 1, 2))
                    cv2.polylines(img, [points], isClosed=False, color=(230, 0, 0), thickness=5)


                    if classe in ["Yellow Robot", "Blue Robot", "Ball"]:
                        # Remove o (0,0) adicionado antes e adiciona a posição real
                        self.class_points_mm[classe].pop()
                        if self.field_reference:
                            x_ref, y_ref, w_ref, h_ref = self.field_reference
                            x_mm = (x - x_ref) * 1500 / w_ref
                            y_mm = (y - y_ref) * 1300 / h_ref
                            self.class_points_mm[classe].append((float(x_mm), float(y_mm)))
                        else:
                            self.class_points_mm[classe].append((float(x), float(y)))

                    if classe == "Field":
                        x_ref = x - (w / 2)
                        y_ref = y - (h / 2)
                        w_ref = w
                        h_ref = h
                        self.field_reference = (x_ref, y_ref, w_ref, h_ref)

            except:
                pass

        return img

    def run(self):
        frame_count = 0  # Contador de frames

        while True:
            success, img = self.cap.read()
            if not success:
                print("Frame não capturado")
                break

            frame_count += 1  # Incrementa o contador de frames
            processed_img = self.process_frame(img)
            if processed_img is not None:
                self.out.write(processed_img)
                cv2.imshow("Tela", processed_img)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        self.cap.release()
        self.out.release()
        cv2.destroyAllWindows()
        print("Vídeo processado salvo em 'output/processed.mp4'")

    def save_points(self, filename):
        with open(filename, "w") as arquivo:
            classes = list(self.class_points_mm.keys())
            arquivo.write("\t".join(classes) + "\n")

            max_len = max(len(self.class_points_mm[classe]) for classe in classes)

            for i in range(max_len):
                linha = []
                for classe in classes:
                    if i < len(self.class_points_mm[classe]):
                        linha.append(f"{self.class_points_mm[classe][i]}")
                    else:
                        linha.append("(0, 0)")  # Se faltar um dado, preenche com (0,0)
                arquivo.write("\t".join(linha) + "\n")

        print(f"Pontos convertidos para mm salvos em {filename}")

if __name__ == "__main__":
    video_processor = VideoProcessor("Yolo_rotated.mp4", "runs/detect/train13/weights/best.pt")
    video_processor.run()
    video_processor.save_points("output/points.txt")
