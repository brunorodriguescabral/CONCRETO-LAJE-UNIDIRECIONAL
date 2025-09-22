import time
import math

def timer(delay):
    print("\n")
    for i in range(delay):
        i = i - delay
        print(f"\rEncerrando/Reiniciado em: {abs(i)} segundos ", end='')
        time.sleep(1)
    print("\n")

try:
    import numpy as np
    import pandas as pd
    import openpyxl
except Exception as es:
    print(f"\n❌ Não foi possivel localizar uma das seguintes bibliotecas: \n▪ Numpy \n▪ Pandas \n▪ Openpyxl \n\nDownload de todos os arquivos ou duvidasa em: \n➡️ https://github.com/brunorodriguescabral/CONCRETO-LAJE-UNIDIRECIONAL")
    timer(120)


# Definição de Parâmetros
VALUE_PESO_PROPRIO = 25 #Valor do peso proprio em KN (Padrão = 25)
VALUE_CONTRAPISO = 21 #Peso do contrapiso em KN (Padrão = 21)
HEIGHT_CONTRAPISO = 0.07 #Altura do contrapiso em M (Padrão = 0.07)
VALUE_REVESTIMENTO = 20 #Peso do revestimento em KN (Padrão = 20)
HEIGHT_REVESTIMENTO = 0.02 #Altura do revestimento em M (Padrão = 0.02)
VALUE_CARGA_VARIAVEL = 1.5 #Valor da carga variavel em KN (Padrão = 1.5)
HEIGHT_MIN_LAJE = 12 #Valor minimo da laje
VALUE_FCK = 30 #Valor do FCK utilizado no projeto em MPA [Disponivel apenas (30, 35, 40, 45 e 50)](Padrão = 30 para litoral)
VALUE_COBRIMENTO = 3.5 #Valor do cobrimento do concreto em CM (Padrão = 3.5)
VALUE_ACO = "CA-50" #Definir o tipo do Aço [Disponivel apenas (CA-25, CA-50 e CA-60)] (Padrão = CA-50)
TIME_DELAY = 0.5 #Valor do delay entre os cálculo em Segundos (Padrão = 1)
DOBRA_ACO = True #Definir se vai ter dobra na barra ou não [Escolher entre True e False] (Padrão = True)

try:
    XLSX_KS = pd.read_excel("kc-ks.xlsx", index_col=0)
    XLSX_ACO = pd.read_excel("tabela_de_aco.xlsx", index_col=0)
except Exception as es:
    try:
        url1 = "https://raw.githubusercontent.com/brunorodriguescabral/CONCRETO-LAJE-UNIDIRECIONAL/main/kc-ks.xlsx"
        XLSX_KS = pd.read_excel(url1, index_col=0)
        url2 = "https://raw.githubusercontent.com/brunorodriguescabral/CONCRETO-LAJE-UNIDIRECIONAL/main/tabela_de_aco.xlsx"
        XLSX_ACO = pd.read_excel(url2, index_col=0)
    except Exception as es:
        print(f"\n❌ Não foi possível localizar o arquivo e nem baixar automaticamente \"kc-ks.xlsx\" \n\nO arquivo excel deverá estar na mesma pasta que o arquivo python \nDownload de todos os arquivos em: \n➡️ https://github.com/brunorodriguescabral/CONCRETO-LAJE-UNIDIRECIONAL")
        timer(120)

def delay(i):
    time.sleep(i)

def get_aco(target):
    limit = target + 0.9
    results = []
    for line in XLSX_ACO.index:
        for column in XLSX_ACO.columns:
            value = XLSX_ACO.at[line, column]
            if target <= value <= limit:
                results.append((line, column, value))
    results.sort(key= lambda x: x[2])
    for line, column, value in results:
        print(f"Diâmetro Barra Ø: {column} mm | Espaçamento: {line} cm | As: {value} cm²/m")
    

print(f"\n-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-")
print(" Calculadora de Laje armada em 1 Direção \n Feito por: Bruno Rodrigues Cabral \n https://github.com/brunorodriguescabral/CONCRETO-LAJE-UNIDIRECIONAL")
print("-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-")
time.sleep(1)

print(f"""\nInstruções:
▪ Não utilize virgulas para casas decimais, sempre utilize ponto
▪ Todos os parâmetros são configuraveis diretamente no arquivo Python
▪ Verifique sempre a unidade métrica utilizada na variável ou solicitada
▪ Não é possivel utiliza-la para calcular Lajes armadas em mais de uma direção\n""")

time.sleep(2)

while True:
    print("-=- Insira os valores e L e l em METROS e com ponto para separação (Ex: 8.5) -=-\n")
    l_maior = float(input("-> Digite o valor de L (maior lado): "))
    l_menor = float(input("-> Digite o valor de l (menor lado): "))
    
    if l_maior < l_menor:
        print("\n【❌ 】\nO valor de (L) está menor do que o valor de (l)\n")
        timer(9)
        continue

    print(f"\nLado maior (L): {l_maior} x Lado menor (l): {l_menor}\n")
    for _ in range(int(l_maior)): 
        print('🧱'*int(l_menor)) 
    
    delay(TIME_DELAY)
    
    print("\n💠 Verificação do Lambda ( λ ) \nSe λ >= 2: Armadura 1D (1 direção)")
    value_lambda = l_maior/l_menor
    
    if l_maior/l_menor >= 2:
        print(f"λ = L/l \nλ = {l_maior}/{l_menor} \nλ = {value_lambda}\n✅ OK!\n")
    else:
        print(f"\nλ = L/l \nλ = {l_maior}/{l_menor} \nλ = {value_lambda}\n❌ NÃO PASSOU!\n-> A laje escolhida deverá ser armada em 2 direções, devendo utilizar outro app para o calculo\n")
        continue
    delay(TIME_DELAY)
    
    height_laje = 0.025 * ((l_maior+l_menor)/2)
    height_laje_r = round(height_laje, 2)
    print(f"💠 Cálculo da altura da laje (2,5% x Média dos lados)\n1D: 2,5% x (L + l)/2\n1D: 2,5% x ({l_maior}+{l_menor})/2\n1D: 2,5% x ({(l_maior+l_menor)/2})\n1D: 0.025 x {height_laje/0.025}\n1D: {height_laje}\n1D: {height_laje_r} m\n1D: {int(height_laje_r*100)} cm")
    if height_laje_r*100 < HEIGHT_MIN_LAJE:
        print(f"\nComo a altura da laje ({height_laje_r}) é menor do que a altura mínima ({HEIGHT_MIN_LAJE})\n-> Adotaremos o valor mínimo de: {HEIGHT_MIN_LAJE} cm\n✅ OK!")
        height_laje_r = HEIGHT_MIN_LAJE/100
    else: print("✅ OK!")
    delay(TIME_DELAY)

    print("\n💠 Cargas Atuantes")
    print(f"""▪ Peso Próprio: γ = {VALUE_PESO_PROPRIO} kN/m³ e h = {height_laje_r} m
▪ Contrapiso: γ = {VALUE_CONTRAPISO} kN/m³ e h = {HEIGHT_CONTRAPISO} m
▪ Revestimento: γ = {VALUE_REVESTIMENTO} kN/m³ e h = {HEIGHT_REVESTIMENTO} m
▪ Carga Váriavel: γ = {VALUE_CARGA_VARIAVEL} kN/m²""")
    
    carga_peso_proprio = round(l_maior * l_menor * height_laje_r * VALUE_PESO_PROPRIO, 2)
    carga_contrapiso = round(l_maior * l_menor * HEIGHT_CONTRAPISO * VALUE_CONTRAPISO, 2)
    carga_revestimento = round(l_maior * l_menor * HEIGHT_REVESTIMENTO * VALUE_REVESTIMENTO, 2)
    carga_variavel = round(l_maior * l_menor * VALUE_CARGA_VARIAVEL, 2)

    print("\nCálculo de Cargas")
    print(f"""▪ Peso Próprio: {l_maior}m x {l_menor} m x {height_laje_r} m x {VALUE_PESO_PROPRIO} kN/m³ = {carga_peso_proprio} kN
▪ Contrapiso: {l_maior}m x {l_menor} m x {height_laje_r} m x {VALUE_CONTRAPISO} kN/m³ = {carga_contrapiso} kN
▪ Revestimento: {l_maior}m x {l_menor} m x {height_laje_r} m x {VALUE_REVESTIMENTO} kN/m³ = {carga_revestimento} kN
▪ Carga Váriavel: {l_maior}m x {l_menor} m x {VALUE_CARGA_VARIAVEL} kN/m² = {carga_variavel} kN""")
    delay(TIME_DELAY)

    carga_total = round(carga_peso_proprio + carga_contrapiso + carga_revestimento + carga_variavel, 2)
    carga_distribuida = round(carga_total / (l_maior*l_menor), 2)
    print(f"\nQ = Carga Total (Soma das cargas atuantes)\nQ = {carga_peso_proprio} + {carga_contrapiso} + {carga_revestimento} + {carga_variavel}\nQ = {carga_total} kN")
    print(f"\nq = Carga Distribuida (Total / Área da laje)\nq = {carga_distribuida} kN/m²")
    delay(TIME_DELAY)

    value_momento = round((carga_distribuida*(l_menor**2))/8, 2)
    print(f"\nM = (q * l²) / 8\nM = ({carga_distribuida} * {l_menor}²) / 8 \nM = {value_momento} kN.m")
    value_md = round(value_momento * 1.4, 2)
    print(f"\nMd = M x 1,4\nMd = {value_momento} x 1,4\nMd = {value_md}")
    delay(TIME_DELAY)

    print("\n💠 Coeficiente de Compressão")
    c_limite = 0.14 * VALUE_FCK*10
    value_b = 100
    print(f"C limite = 0,14 x Fck (em Kgf/cm²)\nC limite = 0,14 x {VALUE_FCK*10}\nC limite = {c_limite} Kgf/cm²")
    value_md_kgf = int(value_md * 10000)
    print(f"\nConverter Md de Kn.m para Kgf.cm\nMd = {value_md} x 10000\nMd = {value_md_kgf} Kgf.cm")
    area_util = round((height_laje_r*100) - VALUE_COBRIMENTO - VALUE_COBRIMENTO, 2)
    print(f"Calcular Área Util da Laje (d) \nd = h - c - c (Altura da laje - cobrimento superior - cobrimento inferior) \nd = {height_laje_r*100} - {VALUE_COBRIMENTO} - {VALUE_COBRIMENTO} \nd = {area_util}")
    value_c = round(value_md_kgf / (100*(area_util**2)) ,2)

    print(f"\nC = M / (b x d²)\nC = {value_md_kgf} / {value_b} x {area_util**2}\nC = {value_c}")

    if value_c > c_limite:
        print(f"\nO valor do FCK ultrapassa o limite do concreto\n-> deverá ser escolhido outro FCK\n❌ NÃO PASSOU!")
        timer(60)
        continue
    else: 
        print(f"\nO valor C deve ser menor que C Limite\n{value_c} < {c_limite} Kgf/cm²\n✅ OK!")
        delay(TIME_DELAY)
    
    value_md_kncm = value_md * 100
    print("\n💠 Cálculo de Kc e Ks")
    value_kc = round((value_b * (area_util**2)/value_md_kncm), 2)
    print(f"Converter Md de kN.m para kN.cm \nMd = {value_md} x 100 \nMd = {value_md_kncm} kN.cm\n")
    print(f"Kc = (b x d²) / Md (Kn.cm) \nKc = ({value_b} x {area_util}²) / {value_md_kncm} \nKc = {value_kc} cm²/kN \n✅ OK!")
    delay(TIME_DELAY)

    print("\n💠 Taxa de Armadura (As)")
    column_fck = f"C{VALUE_FCK}"
    column = XLSX_KS[column_fck]
    lower_kc = column[column <= value_kc]
    line_kc = lower_kc.idxmax()
    value_kc = lower_kc.loc[line_kc]
    value_ks = XLSX_KS.at[line_kc, VALUE_ACO]

    print(f"Valor aproximado de Kc: {value_kc}\nValor tabelado de Ks: {value_ks}\n")

    value_as = round((value_ks * value_md_kncm) / area_util, 2)
    print(f"As = (Ks x Md) / d \nAs = ({value_ks} x {value_md_kncm})/ {area_util} \nAs = {value_as} cm²/m \n✅ OK! \n")

    print(f"Lista de Barras que podem ser utilizadas no projeto: ")
    get_aco(value_as)

    dim_barra = float(input("\n-> Diâmetro da barra escolhida: "))
    esp_barra = float(input("-> Espaçamento da barra escolhida: "))
    comprimento_barra = (l_menor*100)-(VALUE_COBRIMENTO*2)
    
    print(f"\n💠 Informações da Ferragem \nBarra escolhida: {dim_barra} m c/ {esp_barra} cm \nDescontar cobrimento: \n{l_menor*100} - {VALUE_COBRIMENTO} - {VALUE_COBRIMENTO}\n")
    if DOBRA_ACO != False:
        comprimento_dobra = comprimento_barra+(area_util*2)
        quantidade = math.floor((l_maior*100/esp_barra))-1
        print(f"Tamanho ta barra considerando a dobra: \n{comprimento_dobra} cm \nQuantidade de Barras: \nQnt: (Lado maior / Espaçamento) - 1 \nQnt: ({l_maior*100} / {esp_barra}) - 1 \nQnt: {quantidade} barras \n\nDesenho da Barra: \n")
        print(f"   {area_util}            {comprimento_barra}             {area_util}")
        print(f"    |_________________________________|")
        print(f"     {quantidade} Ø {dim_barra} mm c/ {esp_barra} - c = {comprimento_dobra}")
    else:
        quantidade = math.floor((l_maior*100/esp_barra))-1
        print(f"Tamanho da barra considerando a dobra: \n{comprimento_barra} cm \nQuantidade de Barras: \nQnt: (Lado maior / Espaçamento) - 1 \nQnt: ({l_maior*100} / {esp_barra}) - 1 \nQnt: {quantidade} barras \n\nDesenho da Barra: \n")
        print(f"                  {comprimento_barra} ")
        print(f"    _________________________________")
        print(f"     {quantidade} Ø {dim_barra} mm c/ {esp_barra} - c = {comprimento_barra}")
        

    timer(120)

    


