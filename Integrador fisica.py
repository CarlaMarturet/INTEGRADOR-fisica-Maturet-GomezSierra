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
    # Desgloses y tarifas
    cargo_fijo_suministro = 11421.88
    tarifa_basica_600 = 123.9694
    tarifa_excedente_142 = 134.8487
    tarifa_excedente_43 = 162.1050
    tarifa_excedente_503 = 166.6580
    beneficio_social = 800
    alumbrado_publico = 4426.00
    subsidio = 0.20

    # Calcular cargos por consumo
    consumo_bimensual_basico = min(consumo_energia, 600) * tarifa_basica_600
    consumo_excedente_142 = max(0, min(consumo_energia - 600, 142)) * tarifa_excedente_142
    consumo_excedente_43 = max(0, min(consumo_energia - 742, 43)) * tarifa_excedente_43
    consumo_excedente_503 = max(0, consumo_energia - 785) * tarifa_excedente_503

    # Calcular subtotal antes de beneficios y subsidios
    subtotal = (cargo_fijo_suministro + consumo_bimensual_basico +
                consumo_excedente_142 + consumo_excedente_43 +
                consumo_excedente_503 + alumbrado_publico - beneficio_social)

    # Aplicar subsidio
    subtotal_con_subsidio = subtotal * (1 - subsidio)
    
    # Calcular IVA
    iva = subtotal_con_subsidio * 0.21

    # Total a pagar
    total_pagar = subtotal_con_subsidio + iva
    
    return total_pagar, {
        "Cargo fijo por suministro": cargo_fijo_suministro,
        "Consumo primeros 600 KWh/Bim": consumo_bimensual_basico,
        "Consumo excedente 142 KWh/Bim": consumo_excedente_142,
        "Consumo excedente 43 KWh/Bim": consumo_excedente_43,
        "Consumo excedente 503 KWh/Bim": consumo_excedente_503,
        "Beneficio Social Provincial Eléctrico": -beneficio_social,
        "Alumbrado Publico": alumbrado_publico,
        "Subtotal con subsidio aplicado": subtotal_con_subsidio,
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
        capacitancia = calcular_capacitancia(corriente)
        total_a_pagar, cargos = calcular_total_pagar(consumo_energia)
        
        label_resultado_potencia.config(text=f"Potencia en W: {potencia:.2f}")
        label_resultado_corriente.config(text=f"Corriente en A: {corriente:.2f}")
        label_resultado_capacitancia.config(text=f"Capacitancia en Faradios: {capacitancia:.6f}")
        label_resultado_total.config(text=f"Total a pagar: ${total_a_pagar:.2f}")
        
        button_desglose.config(command=lambda: mostrar_desglose(cargos))
    except ValueError as e:
        messagebox.showerror("Error", str(e))

# Crear la ventana principal
root = tk.Tk()
root.title("Calculadora de Energía")

# Crear y colocar los widgets
tk.Label(root, text="Ingrese dato anterior (kWh)").grid(row=0)
tk.Label(root, text="Ingrese dato actual (kWh)").grid(row=1)

entry_energia_anterior = tk.Entry(root)
entry_energia_actual = tk.Entry(root)

entry_energia_anterior.grid(row=0, column=1)
entry_energia_actual.grid(row=1, column=1)

tk.Button(root, text="Calcular", command=calcular).grid(row=2, columnspan=2)

label_resultado_potencia = tk.Label(root, text="Potencia en W: ")
label_resultado_potencia.grid(row=3, columnspan=2)
label_resultado_corriente = tk.Label(root, text="Corriente en A: ")
label_resultado_corriente.grid(row=4, columnspan=2)
label_resultado_capacitancia = tk.Label(root, text="Capacitancia en Faradios: ")
label_resultado_capacitancia.grid(row=5, columnspan=2)
label_resultado_total = tk.Label(root, text="Total a pagar: ")
label_resultado_total.grid(row=6, columnspan=2)

button_desglose = tk.Button(root, text="Ver desglose de cargos")
button_desglose.grid(row=7, columnspan=2)

# Iniciar el bucle principal de la interfaz gráfica
root.mainloop()
