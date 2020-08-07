import tkinter as tk
import tkinter.ttk as ttk

window = tk.Tk()
window.title('Eform')
window.geometry('400x300')

listbox = ttk.Combobox(window , value=['1','2','3']).pack()

listbox.grid(column=0, row=1)
listbox.current(0)
print(listbox.current(),listbox.get())

window.mainloop()