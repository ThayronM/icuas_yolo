from ultralytics import YOLO
import cv2
from collections import defaultdict
import numpy as np

# capturar video da webcam
# cap = cv2.VideoCapture(1)

# capturar video mp4
cap = cv2.VideoCapture("video.mp4")

# model = YOLO("yolov8n.pt")
model = YOLO("runs/detect/train7/weights/best.pt")


track_history = defaultdict(lambda: [])
seguir = True
deixar_rastro = True

class_points = defaultdict(list)

while True:
    success, img = cap.read()
    img = cv2.resize(img, (800, 600))

    if success:
        if seguir:
            results = model.track(img, persist=True)
        else:
            results = model(img)

        # Process results list
        for result in results:
            img = result.plot()
            
            # Get the boxes and track IDs
            boxes = result.boxes.xywh.cuda()
            track_ids = result.boxes.id.int().cuda().tolist()
            class_idx = result.boxes.cls.cuda().tolist()

            # Plot the tracks
            for box, track_id, class_idx in zip(boxes, track_ids, class_idx):
                x, y, w, h = box
                track = track_history[track_id]
                track.append((float(x), float(y)))  # x, y center point
                if len(track) > 30:  # retain 90 tracks for 90 frames
                    track.pop(0)
                    
                # pegando a classe do resultado
                classe = result.names[class_idx]
                # Adicionando os pontos no dicionário por classe
                class_points[classe].append((float(x), float(y)))
                # Draw the tracking lines
                points = np.hstack(track).astype(np.int32).reshape((-1, 1, 2))
                cv2.polylines(img, [points], isClosed=False, color=(230, 0, 0), thickness=5)
            

        cv2.imshow("Tela", img)

    k = cv2.waitKey(1)
    if k == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
print("desligando")



with open("points.txt", "w") as arquivo:
    classes = list(class_points.keys())
    arquivo.write("\t".join(classes) + "\n")
    # número máximo de linhas necessárias
    max_len = max(len(points) for points in class_points.values())

    for i in range(max_len):
        linha = []
        for classe in classes:
            if i < len(class_points[classe]):
                linha.append(f"{class_points[classe][i]}")
            else:
                linha.append("")  # vazio
        arquivo.write("\t".join(linha) + "\n")

