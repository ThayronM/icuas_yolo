from ultralytics import YOLO
import cv2
from collections import defaultdict
import numpy as np

# capturar video da webcam
# cap = cv2.VideoCapture(1)

# capturar video mp4
cap = cv2.VideoCapture("RealSense_trimmed.mp4")

# model = YOLO("yolov8n.pt")
model = YOLO("runs/detect/train12/weights/best.pt")


track_history = defaultdict(lambda: [])
seguir = True
deixar_rastro = True

# Dicionário para armazenar os pontos por classe
class_points = defaultdict(list)
class_points_mm = defaultdict(list) 


while True:
    success, img = cap.read()
    img = cv2.resize(img, (640, 362))

    if success:
        if seguir:
            results = model.track(img, persist=True, verbose=False)
        else:
            results = model(img)

        # Process results list
        for result in results:
            img = result.plot()
            
            try:
                # Get the boxes and track IDs
                boxes = result.boxes.xywh.cuda()
                track_ids = result.boxes.id.int().cuda().tolist()
                class_idxs = result.boxes.cls.cuda().tolist()

                # Plot the tracks
                for box, track_id, class_idx in zip(boxes, track_ids, class_idxs):
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
                    
                    # points em mm apenas para classe Field
                    
                    if classe == "Field":
                        # reference points
                        x_ref = x - (w / 2)
                        y_ref = y - (h / 2)
                        w_ref = w
                        h_ref = h
                        print(f"\nClasse: {classe}, w: {w:.3f}, h: {h:.3f}", end=' ')
                        print(f"Classe: {classe}, x: {x:.3f}, y: {y:.3f}")
                        
                        
                    if classe == "Yellow Robot":
                        print(f'{points[classe.index("Yellow Robot")]}')
                        x_mm = (x - x_ref) * 1500 / w_ref
                        y_mm = (y - y_ref) * 1300 / h_ref 
                        print(f"Classe: {classe}, x: {x_mm:.3f}, y: {y_mm:.3f}")   
                        
                    
                    if classe == "Red Robot":
                        print(f'{points[classe.index("Red Robot")]}')
                        x_mm = (x - x_ref) * 1500 / w_ref
                        y_mm = (y - y_ref) * 1300 / h_ref 
                        print(f"Classe: {classe}, x: {x_mm:.3f}, y: {y_mm:.3f}")
                    
                    
                    if classe == "Ball":
                        print(f'{points[classe.index("Ball")]}')
                        x_mm = (x - x_ref) * 1500 / w_ref
                        y_mm = (y - y_ref) * 1300 / h_ref 
                        print(f"Classe: {classe}, x: {x_mm:.3f}, y: {y_mm:.3f}")
                    
                    
                    
                    # Adicionando os pontos no dicionário por classe
                    if classe in ["Yellow Robot", "Red Robot", "Ball"] and 'w_ref' in locals():
                        x_mm = (x - x_ref) * 1500 / w_ref
                        y_mm = (y - y_ref) * 1300 / h_ref
                        class_points_mm[classe].append((float(x_mm), float(y_mm)))  # Salva em mm
            
            except:
                pass
            

        cv2.imshow("Tela", img)

    k = cv2.waitKey(1)
    if k == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
print("desligando")


# Salvar os pontos em mm no arquivo
with open("points.txt", "w") as arquivo:
    classes = list(class_points_mm.keys())
    arquivo.write("\t".join(classes) + "\n")
    max_len = max(len(points) for points in class_points_mm.values())
    for i in range(max_len):
        linha = []
        for classe in classes:
            if i < len(class_points_mm[classe]):
                linha.append(f"{class_points_mm[classe][i]}")
            else:
                linha.append("")  # vazio para classes que não têm pontos nesse frame
        arquivo.write("\t".join(linha) + "\n")
        