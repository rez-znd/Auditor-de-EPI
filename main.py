import cv2
from ultralytics import YOLO
import os
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

# --- Configurações de Caminho e Modelo ---
pasta_do_projeto = os.path.dirname(os.path.abspath(__file__))
caminho_modelo = os.path.join(pasta_do_projeto, "modelo_epi.pt")
model = YOLO(caminho_modelo)


class AplicativoEPI:
    def __init__(self, janela):
        self.janela = janela
        self.janela.title("Sistema Inteligente de Auditoria de EPI")
        self.janela.geometry("1100x650")
        self.janela.configure(bg="#1a1a1a")

        self.cap = cv2.VideoCapture(0)

        self.janela.columnconfigure(0, weight=3)
        self.janela.columnconfigure(1, weight=1)
        self.janela.rowconfigure(0, weight=1)

        self.lbl_video = tk.Label(janela, bg="#000000")
        self.lbl_video.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        self.painel_lateral = tk.Frame(janela, bg="#262626", bd=2, relief="groove")
        self.painel_lateral.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")

        lbl_titulo = tk.Label(self.painel_lateral, text="PAINEL DE AUDITORIA", font=("Arial", 14, "bold"), fg="#deff9a",
                              bg="#262626")
        lbl_titulo.pack(pady=20)

        # Status Geral
        self.lbl_status_geral = tk.Label(self.painel_lateral, text="Aguardando inspeção...", font=("Arial", 12, "bold"),
                                         fg="#ffffff", bg="#333333", width=25, height=2)
        self.lbl_status_geral.pack(pady=15)

        self.frame_capacete = tk.Frame(self.painel_lateral, bg="#262626")
        self.frame_capacete.pack(pady=10, fill="x", padx=20)
        tk.Label(self.frame_capacete, text="Capacete:", font=("Arial", 11), fg="#ffffff", bg="#262626").pack(
            side="left")
        self.lbl_status_cap = tk.Label(self.frame_capacete, text="-", font=("Arial", 11, "bold"), fg="#ffffff",
                                       bg="#262626")
        self.lbl_status_cap.pack(side="right")

        self.frame_colete = tk.Frame(self.painel_lateral, bg="#262626")
        self.frame_colete.pack(pady=10, fill="x", padx=20)
        tk.Label(self.frame_colete, text="Colete:", font=("Arial", 11), fg="#ffffff", bg="#262626").pack(side="left")
        self.lbl_status_col = tk.Label(self.frame_colete, text="-", font=("Arial", 11, "bold"), fg="#ffffff",
                                       bg="#262626")
        self.lbl_status_col.pack(side="right")

        self.btn_sair = ttk.Button(self.painel_lateral, text="Sair do Sistema", command=self.fechar_aplicativo)
        self.btn_sair.pack(side="bottom", pady=20)

        self.janela.protocol("WM_DELETE_WINDOW", self.fechar_aplicativo)

        self.atualizar_frame()

    def atualizar_frame(self):
        ret, frame = self.cap.read()
        if ret:
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
                cv2.putText(img_saida, "Pessoa Principal", (xp1, yp1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                            (255, 0, 255), 2)

                for box in results[0].boxes:
                    classe_id = int(box.cls[0])
                    nome_classe = model.names[classe_id].lower()
                    xo1, yo1, xo2, yo2 = int(box.xyxy[0][0]), int(box.xyxy[0][1]), int(box.xyxy[0][2]), int(
                        box.xyxy[0][3])

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
                    cor_cv = (0, 255, 0)
                    cor_tk = "#00FF00"
                elif tem_capacete or tem_colete:
                    status = "EPI parcial - Atencao!"
                    cor_cv = (0, 165, 255)
                    cor_tk = "#FFA500"
                else:
                    status = "ALERTA: TOTALMENTE SEM EPI"
                    cor_cv = (0, 0, 255)
                    cor_tk = "#FF0000"

                cv2.putText(img_saida, status, (10, 40), fonte, 0.8, cor_cv, 2)

                self.lbl_status_geral.config(text=status, bg=cor_tk,
                                             fg="#000000" if tem_capacete or tem_colete else "#ffffff")
                self.lbl_status_cap.config(text="OK" if tem_capacete else "Faltando",
                                           fg="#00FF00" if tem_capacete else "#FF0000")
                self.lbl_status_col.config(text="OK" if tem_colete else "Faltando",
                                           fg="#00FF00" if tem_colete else "#FF0000")
            else:
                cv2.putText(img_saida, "Aguardando inspecao (Nenhuma pessoa)...", (10, 40), fonte, 0.7, (255, 255, 255),
                            2)
                self.lbl_status_geral.config(text="Nenhuma pessoa detectada", bg="#333333", fg="#ffffff")
                self.lbl_status_cap.config(text="-", fg="#ffffff")
                self.lbl_status_col.config(text="-", fg="#ffffff")

            img_rgb = cv2.cvtColor(img_saida, cv2.COLOR_BGR2RGB)
            img_pil = Image.fromarray(img_rgb)
            img_tk = ImageTk.PhotoImage(image=img_pil)

            self.lbl_video.img_tk = img_tk
            self.lbl_video.config(image=img_tk)

        self.janela.after(15, self.atualizar_frame)

    def fechar_aplicativo(self):
        if self.cap.isOpened():
            self.cap.release()
        self.janela.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = AplicativoEPI(root)
    root.mainloop()