# 👷‍♂️ Sistema de Inspeção de EPI em Tempo Real

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![OpenCV](https://img.shields.io/badge/OpenCV-4.x-green)
![YOLOv8](https://img.shields.io/badge/YOLOv8-Ultralytics-orange)

Este projeto utiliza **Visão Computacional** e **Inteligência Artificial** (via YOLO) para realizar a detecção em tempo real do uso de Equipamentos de Proteção Individual (EPIs). O sistema foca em identificar a pessoa principal na câmera e verificar se ela está utilizando **capacete** e **colete de segurança**.

## ✨ Funcionalidades

* **Detecção Dinâmica:** Identifica a pessoa com maior área de foco na tela.
* **Associação Inteligente:** Verifica se os EPIs detectados (capacete e colete) pertencem especificamente à pessoa principal, utilizando o cálculo do centro geométrico para evitar falsos positivos.
* **Interface Minimalista:** Painel lateral limpo (fundo cinza com bordas) que exibe o status dos equipamentos sem poluir a imagem da câmera.
* **Alertas Visuais:** * 🟢 **Verde:** EPI totalmente regular (capacete + colete).
  * 🟠 **Laranja:** EPI parcial (apenas um dos itens detectado).
  * 🔴 **Vermelho:** Totalmente sem EPI.

## 📂 Estrutura do Projeto

Para que o código funcione corretamente, a estrutura do seu diretório deve estar assim:

```text
📁 seu_projeto/
│
├── 📄 inspecao_epi.py       # Código principal do script
├── 📄 modelo_epi.pt         # Arquivo de pesos do modelo YOLO treinado para EPIs
└── 📄 README.md             # Este arquivo
