# Teste Técnico – Visão Computacional + IA

## Objetivo
Este projeto implementa um **mini-aplicativo de linha de comando (CLI)** em **Python**, capaz de aplicar **dois algoritmos simples de visão computacional** para segmentação de imagens:

1. **Segmentação por cor (HSV)**  
2. **Segmentação por agrupamento (K-Means)**  

O usuário pode alternar entre os métodos via argumentos na linha de comando.  
O programa também salva automaticamente os resultados em uma pasta de saída.

---

## Pré-Requisitos

- Python **3.9 ou superior**
- Dependências listadas em `requirements.txt`

Instalação:
```bash
pip install -r requirements.txt

ou manualmente:

pip install opencv-python numpy

---

##Explicação dos métodos
#Método HSV

Converte a imagem do espaço BGR (padrão do OpenCV) para HSV.
Define intervalos de tonalidade, saturação e valor (H, S, V) para isolar a cor desejada.
Gera uma máscara binária, onde os pixels dentro do intervalo são marcados em branco.

Faixas padrão:

Cor	   Hmin	 Hmax  Smin	 Smax  Vmin  Vmax
Verde	35	 85	    50	 255	40	 255
Azul	90	 130	50	 255	40	 255

Esses valores podem ser ajustados via linha de comando para melhorar a precisão em imagens com iluminação diferente.

#Método K-Means

Converte a imagem para HSV.
Usa o algoritmo de K-Means para agrupar os pixels por cor.
Cada grupo tem uma cor média (centróide).
O algoritmo escolhe o grupo cuja cor média é mais próxima do verde ou azul.
Cria uma máscara binária com os pixels desse grupo.
O parâmetro --k define o número de clusters.

## Como rodar o programa

Certifique-se de que há imagens dentro da pasta samples/.

Execute o script com o comando apropriado:

# Exemplo de execução
# Segmentação verde (HSV)
python segment.py --input samples/verde3.jpg --method hsv --target green --hmin 40 --hmax 45 --smin 50 --smax 255 --vmin 40 --vmax 255

# Segmentação azul (HSV)
python segment.py --input samples/azul1.jpg --method hsv --target blue --hmin 105 --hmax 110 --smin 230 --smax 255 --vmin 40 --vmax 255

É possível ajustar manualmente os limites da cor:

# Segmentação por agrupamento (K-Means)
python segment.py --input samples/azul2.jpg --method kmeans --k 3 --target blue
python segment.py --input samples/verde4.jpg --method kmeans --k 3 --target green

Saída no terminal:

Máscara salva em: outputs/planta1_hsv_green_mask.png
Overlay salvo em: outputs/planta1_hsv_green_overlay.png
Tempo de execução: 0.64s
Pixels segmentados: 27.15%

Os resultados são salvos automaticamente na pasta outputs/ com nomes únicos (timestamp).

Arquivo	Descrição
*_mask.png	Máscara binária com as áreas detectadas 
*_overlay.png	Imagem original com as regiões detectadas destacadas




Autor:
Fabricio Fiss Bartz

Os testes comprovaram que o K-Means tem dificuldade em isolar alvos pequenos (placa azul1.jpg) e diferenciar tons de mesma cor em grandes áreas (floresta vs. campo), exigindo k alto. Em contraste, o HSV se saiu melhor em todos os cenários complexos devido à capacidade de ajuste fino dos limites de h/S/V.




python segment.py --input samples/azul1.jpg --method hsv --target blue --hmin 105 --hmax 110 --smin 230 --smax 255 --vmin 40 --vmax 255
python segment.py --input samples/azul1.jpg --method kmeans --k 4 --target blue

python segment.py --input samples/azul2.jpg --method kmeans --k 3 --target blue
python segment.py --input samples/azul2.jpg --method hsv --target blue --hmin 105 --hmax 107 --smin 50 --smax 255 --vmin 40 --vmax 255

python segment.py --input samples/verde3.jpg --method hsv --target green --hmin 40 --hmax 45 --smin 50 --smax 255 --vmin 40 --vmax 255
python segment.py --input samples/verde3.jpg --method kmeans --k 3 --target green

python segment.py --input samples/verde4.jpg --method hsv --target green --hmin 35 --hmax 85 --smin 50 --smax 255 --vmin 40 --vmax 255
python segment.py --input samples/verde4.jpg --method kmeans --k 3 --target green

python segment.py --input samples/verde5.jpg --method hsv --target green --hmin 40 --hmax 44 --smin 50 --smax 255 --vmin 40 --vmax 255
python segment.py --input samples/verde5.jpg --method kmeans --k 8 --target green