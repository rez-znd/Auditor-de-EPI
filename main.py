import cv2
from ultralytics import YOLO
import os

pasta_do_projeto = os.path.dirname(os.path.abspath(__file__))
caminho_modelo = os.path.join(pasta_do_projeto, "modelo_epi.pt")

model = YOLO(caminho_modelo)
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)

    results = model(frame, verbose=False, conf=0.4)

    img_saida = frame.copy()

    pessoa_detectada = False
    tem_capacete = False
    tem_colete = False

    box_pessoa = None
    maior_area = 0

    for box in results[0].boxes:
        classe_id = int(box.cls[0])
        nome_classe = model.names[classe_id].lower()

        if "person" in nome_classe or "pessoa" in nome_classe:
            xo1, yo1, xo2, yo2 = box.xyxy[0]
            area = (xo2 - xo1) * (yo2 - yo1)

            if area > maior_area:
                maior_area = area
                box_pessoa = (int(xo1), int(yo1), int(xo2), int(yo2))
                pessoa_detectada = True

    if pessoa_detectada:
        xp1, yp1, xp2, yp2 = box_pessoa

        cv2.rectangle(img_saida, (xp1, yp1), (xp2, yp2), (255, 0, 255), 2)
        cv2.putText(img_saida, "Pessoa Principal", (xp1, yp1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 255), 2)

        for box in results[0].boxes:
            classe_id = int(box.cls[0])
            nome_classe = model.names[classe_id].lower()

            xo1, yo1, xo2, yo2 = int(box.xyxy[0][0]), int(box.xyxy[0][1]), int(box.xyxy[0][2]), int(box.xyxy[0][3])

            if xo1 >= (xp1 - 50) and xo2 <= (xp2 + 50):
                if "helmet" in nome_classe or "capacete" in nome_classe or "hard hat" in nome_classe:
                    tem_capacete = True
                    cv2.rectangle(img_saida, (xo1, yo1), (xo2, yo2), (255, 0, 0), 2)
                elif "vest" in nome_classe or "colete" in nome_classe:
                    tem_colete = True
                    cv2.rectangle(img_saida, (xo1, yo1), (xo2, yo2), (0, 255, 255), 2)

    fonte = cv2.FONT_HERSHEY_SIMPLEX

    if pessoa_detectada:
        if tem_capacete and tem_colete:
            status = "EPI totalmente regular"
            cor = (0, 255, 0)
        elif tem_capacete or tem_colete:
            status = "EPI parcial - Atenção!"
            cor = (0, 165, 255)
        else:
            status = "ALERTA: TOTALMENTE SEM EPI"
            cor = (0, 0, 255)

        cv2.putText(img_saida, status, (10, 40), fonte, 0.8, cor, 2)

        status_cap = "OK" if tem_capacete else "Faltando"
        status_col = "OK" if tem_colete else "Faltando"
        cv2.putText(img_saida, f"Capacete: {status_cap}", (10, 80), fonte, 0.6, (255, 255, 255), 2)
        cv2.putText(img_saida, f"Colete: {status_col}", (10, 110), fonte, 0.6, (255, 255, 255), 2)
    else:
        cv2.putText(img_saida, "Aguardando inspecao (Nenhuma pessoa)...", (10, 40), fonte, 0.7, (255, 255, 255), 2)

    cv2.imshow("Inspecao de EPI Unica - Pressione 'q' para sair", img_saida)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()