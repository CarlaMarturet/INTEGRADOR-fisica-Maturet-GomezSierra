import tkinter as tk
from tkinter import messagebox

def calcular_potencia(energia_anterior, energia_actual):
    if energia_actual < energia_anterior:
        raise ValueError("La energía actual debe ser mayor o igual a la energía anterior.")
    consumo_energia = energia_actual - energia_anterior  # en kWh
    potencia_promedio_w = consumo_energia * 1000  # en W
    return consumo_energia, potencia_promedio_w

def calcular_corriente(potencia, tension=220, cos_fi=0.85):
    corriente = potencia / (tension * cos_fi)  # en A
    return corriente

def calcular_capacitancia(corriente, tension=220):
    frecuencia = 50  # Hz
    reactancia_capacitiva = tension / corriente  # en ohmios
    capacitancia = 1 / (2 * 3.1416 * frecuencia * reactancia_capacitiva)  # en Faradios
    return capacitancia

def calcular_total_pagar(consumo_energia):
    # Definir la tarifa básica
    
    tarifa_basica_600 = 123.9694
    tarifa_excedente_142 = 134.8487
    tarifa_excedente_43 = 162.1050
    tarifa_excedente_503 = 166.6580
    
    
    # Calcular el consumo bimensual básico multiplicando por la tarifa
    consumo_bimensual_basico = 600 * tarifa_basica_600
    consumo_excedente_basico142 = 142 * tarifa_excedente_142
    consumo_excedente_basico43 = 43 * tarifa_excedente_43
    consumo_excedente_basico503 = 503 * tarifa_excedente_503
    
    # Otros cargos (simulados aquí para simplificación)
    cargo_fijo_suministro = 11421.88
    alumbrado_publico = 4426.00
    beneficio_social = 800
    subtotal = (cargo_fijo_suministro + consumo_bimensual_basico + alumbrado_publico +  consumo_excedente_basico142+ consumo_excedente_basico43
                +consumo_excedente_basico503)

    # Calcular el total con un supuesto subsidio
    subsidio = (cargo_fijo_suministro+ consumo_bimensual_basico+ consumo_excedente_basico142+ consumo_excedente_basico43+ consumo_excedente_basico503- beneficio_social) * 0.20
    
    ConsumoBimestralBasico = subtotal -subsidio - beneficio_social

    # Calcular IVA
    iva =  (ConsumoBimestralBasico+ alumbrado_publico) * 0.21
    
    # Total a pagar
    total_pagar =  ConsumoBimestralBasico + iva + alumbrado_publico
    
    # Retornar el total a pagar y un desglose con los cargos
    return total_pagar, {
        "Cargo fijo por suministro": cargo_fijo_suministro,
        "Consumo primeros 600 KWh/Bim a $123.9694": consumo_bimensual_basico,
        "Consumo excendete 142 KWh/Bim a $134.8474": consumo_excedente_basico142,
        "Consumo excendete 43 KWh/Bim a $162.1050": consumo_excedente_basico43,
        "Consumo excendete 503 KWh/Bim a $166.6580": consumo_excedente_basico503,
        "Beneficio social provinvicial social -": beneficio_social ,
        "Subsidio  ": subsidio,
        "Consumo Bimestral - BASICO ": ConsumoBimestralBasico,
        "Alumbrado Publico": alumbrado_publico,
        "IVA consumidor final 21 %": iva,
        "Total a pagar": total_pagar
    }

def mostrar_desglose(cargos):
    desglose = "\n".join([f"{key}: ${value:.2f}" for key, value in cargos.items()])
    messagebox.showinfo("Desglose de Cargos", desglose)

def calcular():
    try:
        energia_anterior = float(entry_energia_anterior.get())
        energia_actual = float(entry_energia_actual.get())
        
        if energia_actual < 0 or energia_anterior < 0:
            raise ValueError("Los valores de energía no pueden ser negativos.")
        
        consumo_energia, potencia = calcular_potencia(energia_anterior, energia_actual)
        corriente = calcular_corriente(potencia)
        total_a_pagar, cargos = calcular_total_pagar(consumo_energia)
        
        label_resultado_potencia.config(text=f"Potencia en W: {potencia:.2f}")
        label_resultado_corriente.config(text=f"Corriente en A: {corriente:.2f}")
        label_resultado_total.config(text=f"Total a pagar: ${total_a_pagar:.2f}")
        
        button_desglose.config(command=lambda: mostrar_desglose(cargos))
    except ValueError as e:
        messagebox.showerror("Error", str(e))

# Crear la ventana principal
root = tk.Tk()
root.title("Calculadora de Energía")
root.geometry("900x500")  # Ajustar el tamaño de la ventana por defecto


# Hacer la ventana a media pantalla y centrarla
root.geometry("960x540")
root.eval('tk::PlaceWindow . center')

# Crear y colocar los widgets en un frame centrado
frame = tk.Frame(root)
frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

tk.Label(frame, text="Ingrese dato anterior (kWh)").grid(row=0)
tk.Label(frame, text="Ingrese dato actual (kWh)").grid(row=1)

entry_energia_anterior = tk.Entry(frame)
entry_energia_actual = tk.Entry(frame)

# Crear un Frame para centrar los elementos
frame = tk.Frame(root)
frame.pack(expand=True)

# Crear y colocar los widgets dentro del Frame
tk.Label(frame, text="Ingrese dato anterior (kWh)").grid(row=0, column=0, padx=10, pady=10)
entry_energia_anterior = tk.Entry(frame)
entry_energia_anterior.grid(row=0, column=1, padx=10, pady=10)


tk.Label(frame, text="Ingrese dato actual (kWh)").grid(row=1, column=0, padx=10, pady=10)
entry_energia_actual = tk.Entry(frame)
entry_energia_actual.grid(row=1, column=1, padx=10, pady=10)


tk.Button(frame, text="Calcular", command=calcular).grid(row=2, columnspan=2)

label_resultado_potencia = tk.Label(frame, text="Potencia en W: ")
label_resultado_potencia.grid(row=3, columnspan=2)
label_resultado_corriente = tk.Label(frame, text="Corriente en A: ")
label_resultado_corriente.grid(row=4, columnspan=2)
label_resultado_capacitancia = tk.Label(frame, text=" ")
label_resultado_capacitancia.grid(row=5, columnspan=2)
label_resultado_total = tk.Label(frame, text="Total a pagar: ")
label_resultado_total.grid(row=6, columnspan=2)

tk.Button(frame, text="Calcular", command=calcular).grid(row=2, column=0, columnspan=2, pady=20)

label_resultado_potencia = tk.Label(frame, text="Potencia en W: ")
label_resultado_potencia.grid(row=3, column=0, columnspan=2, pady=5)

label_resultado_corriente = tk.Label(frame, text="Corriente en A: ")
label_resultado_corriente.grid(row=4, column=0, columnspan=2, pady=5)

label_resultado_total = tk.Label(frame, text="Total a pagar: ")
label_resultado_total.grid(row=6, column=0, columnspan=2, pady=5)

button_desglose = tk.Button(frame, text="Ver desglose de cargos")
button_desglose.grid(row=7, column=0, columnspan=2, pady=5)


button_desglose = tk.Button(frame, text="Ver desglose de cargos")
button_desglose.grid(row=7, columnspan=2)
#sfdgfgdhdghdghd

# Iniciar el bucle principal de la interfaz gráfica
root.mainloop()