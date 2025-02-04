from ultralytics import YOLO
import cv2
from collections import defaultdict
import numpy as np

class VideoProcessor:
    def __init__(self, video_source, model_path):
        self.cap = cv2.VideoCapture(video_source)
        self.model = YOLO(model_path)
        self.track_history = defaultdict(lambda: [])
        self.class_points = defaultdict(list)
        self.class_points_mm = defaultdict(list)
        self.seguir = True
        self.deixar_rastro = True

        self.field_reference = None  # Armazena (x_ref, y_ref, w_ref, h_ref)

    def get_field_reference(self):
        """ Retorna os valores de referência do campo (Field) se disponíveis. """
        return self.field_reference if self.field_reference else (None, None, None, None)

    def process_frame(self, img):
        if self.seguir:
            results = self.model.track(img, persist=True, verbose=False)
        else:
            results = self.model(img)

        for result in results:
            img = result.plot()
            try:
                boxes = result.boxes.xywh.cuda()
                track_ids = result.boxes.id.int().cuda().tolist()
                class_idxs = result.boxes.cls.cuda().tolist()

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

                    if classe == "Field":
                        x_ref = x - (w / 2)
                        y_ref = y - (h / 2)
                        w_ref = w
                        h_ref = h
                        # corrigir para x e y
                        self.field_reference = (x, y, w_ref, h_ref)
                        # print(f"\nClasse: {classe}, w: {w:.3f}, h: {h:.3f}", end=' ')
                        # print(f"Classe: {classe}, x: {x:.3f}, y: {y:.3f}")

                    if classe in ["Yellow Robot", "Red Robot", "Ball"] and 'w_ref' in locals():
                        x_mm = (x - x_ref) * 1500 / w_ref
                        y_mm = (y - y_ref) * 1300 / h_ref
                        self.class_points_mm[classe].append((float(x_mm), float(y_mm)))

            except Exception as e:
                print(f"Error: {e}")
                pass

        return img

    def run(self):
        while True:
            success, img = self.cap.read()
            img = cv2.resize(img, (640, 362))

            if success:
                img = self.process_frame(img)
                cv2.imshow("Tela", img)

                # Obtendo valores do campo em tempo real
                x_ref, y_ref, w_ref, h_ref = self.get_field_reference()
                if x_ref is not None:
                    print(f"Referência do Campo: x_ref={x_ref:.3f}, y_ref={y_ref:.3f}, w_ref={w_ref:.3f}, h_ref={h_ref:.3f}")
                else:
                    print("Campo ainda não detectado")
                

            k = cv2.waitKey(1)
            if k == ord('q'):
                break

        self.cap.release()
        cv2.destroyAllWindows()
        print("desligando")

    def save_points(self, filename):
        with open(filename, "w") as arquivo:
            classes = list(self.class_points.keys())
            arquivo.write("\t".join(classes) + "\n")
            max_len = max(len(points) for points in self.class_points.values())

            for i in range(max_len):
                linha = []
                for classe in classes:
                    if i < len(self.class_points[classe]):
                        linha.append(f"{self.class_points[classe][i]}")
                    else:
                        linha.append("")
                arquivo.write("\t".join(linha) + "\n")


if __name__ == "__main__":
    video_processor = VideoProcessor("corte.mp4", "runs/detect/train12/weights/best.pt")
    video_processor.run()
    # video_processor.save_points("points.txt")
    
    x_ref, y_ref, w_ref, h_ref = video_processor.get_field_reference()
    print(f"Referência do Campo: x_ref={x_ref}, y_ref={y_ref}, w_ref={w_ref}, h_ref={h_ref}")