import yfinance as yf
import matplotlib.pyplot as plt
import numpy as np
import tkinter as tk
from tkinter import ttk, messagebox

def search_stock():
    ticker = ticker_entry.get().strip()
    if not ticker:
        messagebox.showwarning("Input Error", "Por favor, insira um ticker válido.")
        return

    try:
        stock_data = yf.Ticker(ticker)
        history = stock_data.history(period="max")

        plt.figure()
        plt.plot(history.index, history["Close"])
        plt.title(f"Histórico de preços da ação {ticker}")
        plt.xlabel("Data")
        plt.ylabel("Preço (R$)")
        plt.ion()  # Modo interativo
        plt.show()
        plt.pause(0.001)  # Pequena pausa para garantir que o gráfico seja exibido

        last_dividends = stock_data.dividends.tail(12)
        last_dividend_dates = [date.date() for date in last_dividends.index]
        last_price = stock_data.history(period="1d")["Close"][0]
        last_dividend_yield = sum(last_dividends / 12) / last_price * 100

        last_dividends_str = "\n".join([f"Dividendo em {date}: R${dividend:.2f}" for date, dividend in zip(last_dividend_dates, last_dividends)])
        result_label.config(text=f"Últimos dividendos:\n{last_dividends_str}\nDividend yield: {last_dividend_yield:.2f}%")
    except Exception as e:
        messagebox.showerror("Error", f"Erro ao buscar ação: {str(e)}")

# Configuração da interface gráfica com Tkinter
root = tk.Tk()
root.title("Dados dividendos de ações v.4.0")

mainframe = ttk.Frame(root, padding="10 10 20 20")
mainframe.grid(column=0, row=0, sticky=(tk.W, tk.E, tk.N, tk.S))

ttk.Label(mainframe, text="Insira o ticker da ação como no exemplo PETR4.SA:").grid(column=1, row=1, sticky=tk.W)
ticker_entry = ttk.Entry(mainframe, width=20)
ticker_entry.grid(column=2, row=1, sticky=(tk.W, tk.E))

ttk.Button(mainframe, text="Buscar", command=search_stock).grid(column=1, row=2, sticky=tk.W)
ttk.Button(mainframe, text="Fechar", command=root.destroy).grid(column=2, row=2, sticky=tk.E)

result_label = ttk.Label(mainframe, text="", wraplength=300)
result_label.grid(column=1, row=3, columnspan=2, sticky=(tk.W, tk.E))

ttk.Label(mainframe, text="© IHSP Investimentos - 2024 - Todos os direitos reservados", font=("Arial", 8)).grid(column=1, row=4, columnspan=2, sticky=tk.S)

for child in mainframe.winfo_children():
    child.grid_configure(padx=5, pady=5)

root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

ticker_entry.focus()
root.bind("<Return>", lambda event: search_stock())

root.mainloop()