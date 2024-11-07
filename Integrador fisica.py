import tkinter as tk
from tkinter import messagebox

def calcular_potencia(energia_anterior, energia_actual):
    # Asegurarse de que la energía actual sea mayor que la anterior
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

def calcular_total_pagar(consumo_energia, tarifa_basica=135.11756, cargo_fijo=74.28188, iva=0.21):
    subtotal = cargo_fijo + consumo_energia * tarifa_basica
    total_iva = subtotal * iva
    total_pagar = subtotal + total_iva
    return total_pagar

def calcular():
    try:
        energia_anterior = float(entry_energia_anterior.get())
        energia_actual = float(entry_energia_actual.get())
        
        if energia_actual < 0 or energia_anterior < 0:
            raise ValueError("Los valores de energía no pueden ser negativos.")
        
        consumo_energia, potencia = calcular_potencia(energia_anterior, energia_actual)
        corriente = calcular_corriente(potencia)
        capacitancia = calcular_capacitancia(corriente)
        total_a_pagar = calcular_total_pagar(consumo_energia)
        
        label_resultado_potencia.config(text=f"Potencia en W: {potencia:.2f}")
        label_resultado_corriente.config(text=f"Corriente en A: {corriente:.2f}")
        label_resultado_capacitancia.config(text=f"Capacitancia en Faradios: {capacitancia:.6f}")
        label_resultado_total.config(text=f"Total a pagar: ${total_a_pagar:.2f}")
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

# Iniciar el bucle principal de la interfaz gráfica
root.mainloop()
