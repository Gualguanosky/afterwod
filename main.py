import tkinter as tk
from tkinter import messagebox, ttk
import customtkinter as ctk
from PIL import Image, ImageTk
import os
from database import (init_db, add_product, get_products, update_product, delete_product, 
                      record_sale, get_sales_history, add_user, get_users, update_user_balance, delete_user,
                      record_payment, get_combined_history, record_purchase, get_financial_summary,
                      add_recipe_item, get_recipe, delete_recipe, update_ingredient_unit_cost, get_user_purchases)
from styles import Styles, apply_theme

class AfterwordApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Database and Theme
        init_db()
        apply_theme()

        self.title("MILITAR BOX AFTERWORD")
        self.geometry("1300x850") 
        self.configure(fg_color=Styles.BG_COLOR)
        
        # Set window icon
        icon_path = os.path.join("assets", "logo.png")
        if os.path.exists(icon_path):
            try:
                self.iconbitmap(icon_path) if icon_path.endswith('.ico') else self.tk.call('wm', 'iconphoto', self._w, tk.PhotoImage(file=icon_path))
            except: pass

        # Layout
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Sidebar
        self.sidebar = ctk.CTkFrame(self, width=240, corner_radius=0, fg_color=Styles.SIDEBAR_COLOR, border_width=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        
        # Logo Integration
        self.load_logo()

        # Navigation
        self.create_nav_button("📦  INVENTARIO", self.show_inventory)
        self.create_nav_button("👤  USUARIOS / CARTERA", self.show_users)
        self.create_nav_button("💰  NUEVA VENTA", self.show_sales)
        self.create_nav_button("📊  RESUMEN / CAJA", self.show_financial_summary)
        self.create_nav_button("📜  HISTORIAL", self.show_history)

        # Main Content Area
        self.main_container = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.main_container.grid(row=0, column=1, sticky="nsew", padx=40, pady=30)
        
        self.show_inventory()

    def load_logo(self):
        logo_path = os.path.join("assets", "logo.png")
        if os.path.exists(logo_path):
            try:
                img = Image.open(logo_path)
                # Resize to fit sidebar width nicely
                self.logo_img = ctk.CTkImage(light_image=img, dark_image=img, size=(180, 180))
                self.logo_label = ctk.CTkLabel(self.sidebar, text="", image=self.logo_img)
            except Exception as e:
                self.logo_label = ctk.CTkLabel(self.sidebar, text="MILITAR BOX\nAFTERWORD", font=Styles.FONT_HEADER, text_color=Styles.ACCENT_COLOR)
        else:
            self.logo_label = ctk.CTkLabel(self.sidebar, text="MILITAR BOX\nAFTERWORD", font=Styles.FONT_HEADER, text_color=Styles.ACCENT_COLOR)
        
        self.logo_label.pack(pady=(50, 40), padx=20)

    def create_nav_button(self, text, command):
        btn = ctk.CTkButton(
            self.sidebar, text=text, command=command,
            fg_color="transparent", text_color=Styles.TEXT_COLOR, 
            hover_color=Styles.CARD_BG, anchor="w", height=50,
            font=Styles.FONT_LABEL, # Using labels font for nav
            corner_radius=0, # Flat sidebar look
            border_spacing=10
        )
        btn.pack(fill="x", padx=0, pady=2)

    def clear_container(self):
        for widget in self.main_container.winfo_children():
            widget.destroy()

    def create_card(self, parent, title=None):
        card = ctk.CTkFrame(
            parent, fg_color=Styles.CARD_BG, 
            corner_radius=Styles.CORNER_RADIUS,
            border_width=Styles.BORDER_WIDTH,
            border_color=Styles.BORDER_COLOR
        )
        if title:
            title_lbl = ctk.CTkLabel(card, text=title, font=Styles.FONT_CARD_TITLE, text_color=Styles.ACCENT_COLOR)
            title_lbl.pack(pady=(15, 10), padx=20, anchor="w")
        return card

    def show_inventory(self):
        self.clear_container()
        header_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        header_frame.pack(fill="x", pady=(0, 10))
        ctk.CTkLabel(header_frame, text="INVENTARIO DE PRODUCTOS", font=Styles.FONT_SUBHEADER).pack(side="left")
        
        ctk.CTkButton(header_frame, text="+ NUEVO PRODUCTO", command=self.open_product_window,
                     fg_color=Styles.ACCENT_COLOR, text_color="black", font=Styles.FONT_LABEL).pack(side="right")

        # Search Bar
        search_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        search_frame.pack(fill="x", pady=(0, 10))
        ctk.CTkLabel(search_frame, text="🔍", font=Styles.FONT_BODY).pack(side="left", padx=(5, 5))
        self.inv_search_var = tk.StringVar()
        self.inv_search_var.trace("w", lambda *args: self.load_products(self.inv_search_var.get()))
        search_entry = ctk.CTkEntry(search_frame, textvariable=self.inv_search_var, placeholder_text="Buscar por nombre o categoría...", width=400)
        search_entry.pack(side="left")

        table_card = self.create_card(self.main_container)
        table_card.pack(fill="both", expand=True)

        columns = ("ID", "Nombre", "Precio", "Stock", "Categoría", "Tipo")
        self.tree = self.create_styled_tree(table_card, columns)
        self.load_products()

        action_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        action_frame.pack(fill="x", pady=20)
        ctk.CTkButton(action_frame, text="✏️ Editar", command=self.edit_selected_product, width=100).pack(side="left", padx=5)
        ctk.CTkButton(action_frame, text="🗑️ Eliminar", command=self.delete_selected_product, fg_color="transparent", text_color=Styles.DANGER, width=100).pack(side="left", padx=5)

    def show_users(self):
        self.clear_container()
        header_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        header_frame.pack(fill="x", pady=(0, 20))
        ctk.CTkLabel(header_frame, text="USUARIOS Y CARTERA", font=Styles.FONT_SUBHEADER).pack(side="left")
        
        ctk.CTkButton(header_frame, text="+ NUEVO USUARIO", command=self.open_user_window,
                     fg_color=Styles.ACCENT_COLOR, text_color="black", font=Styles.FONT_LABEL).pack(side="right")

        # Search Bar for Users
        search_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        search_frame.pack(fill="x", pady=10)
        ctk.CTkLabel(search_frame, text="🔍 Buscar Usuario:", font=Styles.FONT_LABEL).pack(side="left", padx=10)
        self.user_search_var = tk.StringVar()
        self.user_search_var.trace("w", lambda *args: self.load_users(self.user_search_var.get()))
        search_entry = ctk.CTkEntry(search_frame, textvariable=self.user_search_var, placeholder_text="Nombre o teléfono...", width=350)
        search_entry.pack(side="left", padx=10)

        table_card = self.create_card(self.main_container)
        table_card.pack(fill="both", expand=True)

        ctk.CTkLabel(table_card, text="(Doble clic para ver historial detallado)", font=("Arial", 10), text_color="gray").pack(pady=2)

        columns = ("ID", "Nombre", "Teléfono", "Saldo (Cartera)")
        self.user_tree = self.create_styled_tree(table_card, columns)
        self.user_tree.bind("<Double-1>", lambda e: self.open_user_details_window())
        self.load_users()

        action_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        action_frame.pack(fill="x", pady=20)
        
        ctk.CTkButton(action_frame, text="💵 Registrar Abono", command=self.open_payment_window, 
                      fg_color=Styles.SUCCESS).pack(side="left", padx=5)
        
        ctk.CTkButton(action_frame, text="✅ Liquidar Deuda", command=self.settle_debt, 
                      fg_color=Styles.ACCENT_COLOR, text_color="black").pack(side="left", padx=5)

        ctk.CTkButton(action_frame, text="🗑️ Eliminar Usuario", command=self.delete_selected_user, 
                      fg_color="transparent", text_color=Styles.DANGER).pack(side="left", padx=5)

    def settle_debt(self):
        selected = self.user_tree.selection()
        if not selected:
            messagebox.showwarning("Selección", "Elige un usuario para liquidar su deuda")
            return
        user_data = self.user_tree.item(selected[0])['values']
        # balance is shown as $XX.XX, we need to extract the number
        try:
            balance_str = str(user_data[3]).replace("$", "").replace(",", "")
            balance = float(balance_str)
            
            if balance >= 0:
                messagebox.showinfo("Info", "Este usuario no tiene deuda que liquidar.")
                return
            
            if messagebox.askyesno("Confirmar", f"¿Liquidar deuda de ${abs(balance):.2f} para {user_data[1]}?"):
                # Ask for method when liquidating
                method_win = ctk.CTkToplevel(self)
                method_win.title("Método de Pago")
                method_win.geometry("350x300")
                method_win.attributes("-topmost", True)
                method_win.grab_set()

                scroll = ctk.CTkScrollableFrame(method_win, fg_color="transparent")
                scroll.pack(fill="both", expand=True, padx=5, pady=5)
                
                card = self.create_card(scroll, "Confirmar Liquidación")
                card.pack(fill="both", padx=10, pady=10)

                ctk.CTkLabel(card, text="Selecciona método:", font=Styles.FONT_LABEL).pack(pady=10)
                m_combo = ctk.CTkComboBox(card, values=["Efectivo", "Nequi"], width=200)
                m_combo.pack(pady=10)
                m_combo.set("Efectivo")

                def confirm():
                    record_payment(user_data[0], abs(balance), m_combo.get())
                    self.load_users()
                    method_win.destroy()
                    messagebox.showinfo("Éxito", "Deuda liquidada y registrada en el historial.")

                ctk.CTkButton(scroll, text="Confirmar Liquidación", command=confirm, fg_color=Styles.SUCCESS).pack(pady=10)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo procesar: {str(e)}")

    def create_styled_tree(self, parent, columns):
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", background=Styles.CARD_BG, foreground="white", fieldbackground=Styles.CARD_BG, rowheight=40, borderwidth=0, font=("Segoe UI", 11))
        style.configure("Treeview.Heading", background=Styles.SIDEBAR_COLOR, foreground=Styles.ACCENT_COLOR, relief="flat", padding=10, font=("Segoe UI", 12, "bold"))
        style.map("Treeview", background=[('selected', Styles.ACCENT_COLOR)], foreground=[('selected', 'black')])

        container = ctk.CTkFrame(parent, fg_color="transparent")
        container.pack(fill="both", expand=True)

        tree = ttk.Treeview(container, columns=columns, show="headings")
        
        # Scrollbars
        vsb = ttk.Scrollbar(container, orient="vertical", command=tree.yview)
        hsb = ttk.Scrollbar(container, orient="horizontal", command=tree.xview)
        tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        
        vsb.pack(side="right", fill="y")
        hsb.pack(side="bottom", fill="x")
        tree.pack(side="left", fill="both", expand=True)

        for col in columns:
            tree.heading(col, text=col)
            # Adjust width for Tipo and Category
            w = 150 if col == "Nombre" else 80 if col in ["ID", "Stock", "Tipo"] else 120
            tree.column(col, width=w, anchor="center")
        
        return tree

    def load_users(self, query=""):
        for item in self.user_tree.get_children():
            self.user_tree.delete(item)
        query = query.lower()
        for user in get_users():
            if query in str(user[1]).lower() or query in str(user[2]).lower():
                u_list = list(user)
                u_list[3] = f"${u_list[3]:.2f}"
                self.user_tree.insert("", "end", values=u_list)

    def open_user_details_window(self, user_id=None, user_name=None, balance=None, tree_to_use=None):
        if user_id is None:
            # Fallback to current tree selection (Users Tab)
            tree = tree_to_use if tree_to_use else self.user_tree
            selected = tree.selection()
            if not selected: return
            user_data = tree.item(selected[0])['values']
            user_id = user_data[0]
            user_name = user_data[1]
            balance = user_data[3]

        win = ctk.CTkToplevel(self)
        win.title(f"Historial Financiero: {user_name}")
        win.geometry("850x650")
        win.attributes("-topmost", True)
        win.grab_set()

        scroll = ctk.CTkScrollableFrame(win, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=5, pady=5)

        # Summary Header Card
        total_bought, total_paid = get_user_financial_totals(user_id)
        
        header_card = self.create_card(scroll, f"Estado de Cuenta: {user_name}")
        header_card.pack(fill="x", padx=10, pady=10)
        
        stats_frame = ctk.CTkFrame(header_card, fg_color="transparent")
        stats_frame.pack(fill="x", pady=10)
        
        def add_stat(p, lbl, val, color):
            f = ctk.CTkFrame(p, fg_color="transparent")
            f.pack(side="left", fill="both", expand=True)
            ctk.CTkLabel(f, text=lbl, font=("Arial", 11, "bold")).pack()
            ctk.CTkLabel(f, text=f"${val:.2f}" if isinstance(val, (int, float)) else val, 
                         font=Styles.FONT_SUBHEADER, text_color=color).pack()

        add_stat(stats_frame, "Total Consumido", total_bought, Styles.TEXT_COLOR)
        add_stat(stats_frame, "Total Abonado", total_paid, Styles.SUCCESS)
        add_stat(stats_frame, "Saldo Pendiente", balance, Styles.ACCENT_COLOR)

        # History Table Card
        history_card = self.create_card(scroll, "Movimientos (Ventas y Abonos)")
        history_card.pack(fill="both", expand=True, padx=10, pady=10)

        # Columns: ID, Tipo (Compra/Abono), Detalle (Prod/Método), Info (Cant/-), Monto, Fecha.
        columns = ("ID", "Tipo", "Detalle", "Info", "Monto", "Fecha")
        tree = self.create_styled_tree(history_card, columns)
        
        history = get_user_financial_history(user_id)
        for row in history:
            r_list = list(row)
            r_list[4] = f"${r_list[4]:.2f}"
            tree.insert("", "end", values=r_list)

        ctk.CTkButton(win, text="Cerrar", command=win.destroy, fg_color=Styles.CARD_BG).pack(pady=10)

    def open_user_window(self):
        win = ctk.CTkToplevel(self)
        win.title("Gestión de Usuario")
        win.geometry("450x500")
        win.configure(fg_color=Styles.BG_COLOR)
        win.attributes("-topmost", True)
        win.grab_set()

        scroll = ctk.CTkScrollableFrame(win, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=5, pady=5)

        form = self.create_card(scroll, "Datos del Usuario")
        form.pack(padx=10, pady=10, fill="both")

        ctk.CTkLabel(form, text="Nombre Completo:").pack(pady=(10, 0), padx=20, anchor="w")
        name_entry = ctk.CTkEntry(form, width=300)
        name_entry.pack(pady=5, padx=20)

        ctk.CTkLabel(form, text="Teléfono:").pack(pady=(10, 0), padx=20, anchor="w")
        phone_entry = ctk.CTkEntry(form, width=300)
        phone_entry.pack(pady=5, padx=20)

        def save():
            name = name_entry.get()
            if not name: return
            add_user(name, phone_entry.get())
            self.load_users()
            win.destroy()

        ctk.CTkButton(scroll, text="Guardar Usuario", command=save, fg_color=Styles.ACCENT_COLOR, text_color="black").pack(pady=20)

    def open_payment_window(self):
        selected = self.user_tree.selection()
        if not selected: return
        user_data = self.user_tree.item(selected[0])['values']
        
        win = ctk.CTkToplevel(self)
        win.title("Registrar Abono")
        win.geometry("400x450")
        win.attributes("-topmost", True)
        win.grab_set()

        scroll = ctk.CTkScrollableFrame(win, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=5, pady=5)

        card = self.create_card(scroll, f"Abono: {user_data[1]}")
        card.pack(fill="both", padx=10, pady=10)
        amt_entry = ctk.CTkEntry(card, placeholder_text="Monto a abonar", width=250)
        amt_entry.pack(pady=10)
        
        ctk.CTkLabel(card, text="Método de Pago:").pack(pady=5)
        method_combo = ctk.CTkComboBox(card, values=["Efectivo", "Nequi"], width=250)
        method_combo.pack(pady=10)
        method_combo.set("Efectivo")

        def pay():
            try:
                amt = float(amt_entry.get())
                record_payment(user_data[0], amt, method_combo.get())
                self.load_users()
                win.destroy()
                messagebox.showinfo("Éxito", "Abono registrado correctamente")
            except Exception as e:
                messagebox.showerror("Error", "Monto inválido")

        ctk.CTkButton(scroll, text="Confirmar Abono", command=pay, fg_color=Styles.SUCCESS).pack(pady=20)

    def delete_selected_user(self):
        selected = self.user_tree.selection()
        if not selected: return
        uid = self.user_tree.item(selected[0])['values'][0]
        if messagebox.askyesno("Confirmar", "¿Eliminar usuario?"):
            delete_user(uid)
            self.load_users()

    def show_sales(self):
        self.clear_container()
        
        scroll = ctk.CTkScrollableFrame(self.main_container, fg_color="transparent")
        scroll.pack(fill="both", expand=True)

        ctk.CTkLabel(scroll, text="REGISTRAR NUEVA VENTA", font=Styles.FONT_SUBHEADER).pack(pady=(0, 20), anchor="w")

        sales_card = self.create_card(scroll)
        sales_card.pack(pady=10, fill="both", expand=True)

        # Only allow selling "Productos" and "Productos Compuestos"
        self.all_products = [p for p in get_products() if p[5] != "INSUMO"]
        self.all_users = get_users()
        
        # Row 0: Search Product
        r0 = ctk.CTkFrame(sales_card, fg_color="transparent")
        r0.pack(fill="x", padx=30, pady=(20, 10))
        ctk.CTkLabel(r0, text="🔍 Buscar:", font=Styles.FONT_LABEL).pack(side="left", padx=10)
        self.sales_search_var = tk.StringVar()
        self.sales_search_var.trace("w", self.update_sales_combos)
        search_entry = ctk.CTkEntry(r0, textvariable=self.sales_search_var, placeholder_text="Nombre del producto...", width=350)
        search_entry.pack(side="left", padx=10)

        # Row 1: Product Selection
        r1 = ctk.CTkFrame(sales_card, fg_color="transparent")
        r1.pack(fill="x", padx=30, pady=10)
        ctk.CTkLabel(r1, text="Producto:", font=Styles.FONT_LABEL).pack(side="left", padx=10)
        self.prod_combo = ctk.CTkComboBox(r1, values=[], width=350)
        self.prod_combo.pack(side="left", padx=10)

        # Row 2: User Selection (Wallet)
        r2 = ctk.CTkFrame(sales_card, fg_color="transparent")
        r2.pack(fill="x", padx=30, pady=10)
        ctk.CTkLabel(r2, text="Cliente/Cartera:", font=Styles.FONT_LABEL).pack(side="left", padx=10)
        user_names = ["-- Venta Directa (Contado) --"] + [f"{u[1]} (Saldo: ${u[3]:.2f})" for u in self.all_users]
        self.user_combo = ctk.CTkComboBox(r2, values=user_names, width=350)
        self.user_combo.pack(side="left", padx=10)

        # Row 3: Quantity
        r3 = ctk.CTkFrame(sales_card, fg_color="transparent")
        r3.pack(fill="x", padx=30, pady=10)
        ctk.CTkLabel(r3, text="Cantidad:", font=Styles.FONT_LABEL).pack(side="left", padx=10)
        self.qty_entry = ctk.CTkEntry(r3, width=100)
        self.qty_entry.pack(side="left", padx=10)
        self.qty_entry.insert(0, "1")

        def process_sale():
            try:
                # Get and validate quantity
                qty_str = self.qty_entry.get()
                if not qty_str or not qty_str.isdigit():
                    messagebox.showerror("Error", "Por favor ingresa una cantidad válida")
                    return
                qty = int(qty_str)

                # Get and validate product selection
                selection = self.prod_combo.get()
                if not selection:
                    messagebox.showerror("Error", "Por favor selecciona un producto")
                    return
                
                # More robust matching: Extract name and price to find the product
                # Format is "Name - $Price (S: Stock)"
                prod = None
                for p in self.all_products:
                    match_str = f"{p[1]} - ${p[2]:.2f} (S: {p[3]})"
                    if selection == match_str:
                        prod = p
                        break
                
                if not prod:
                    messagebox.showerror("Error", "Producto no encontrado en la selección")
                    return
                
                # Get and validate user selection
                u_sel = self.user_combo.get()
                user_id = None
                if u_sel != user_names[0]:
                    # Format is "Name (Saldo: $XX.XX)"
                    for u in self.all_users:
                        match_user = f"{u[1]} (Saldo: ${u[3]:.2f})"
                        if u_sel == match_user:
                            user_id = u[0]
                            break
                    if user_id is None:
                        messagebox.showerror("Error", "Usuario no encontrado")
                        return

                if qty > prod[3]:
                    messagebox.showerror("Error", "Stock insuficiente")
                    return
                
                total = prod[2] * qty
                record_sale(prod[0], qty, total, user_id)
                messagebox.showinfo("Éxito", f"Venta registrada correctamente por ${total:.2f}")
                self.show_sales() # Refresh view
            except Exception as e:
                messagebox.showerror("Error", f"Ocurrió un error inesperado: {str(e)}")

        ctk.CTkButton(sales_card, text="Confirmar Venta 💰", command=process_sale, fg_color=Styles.SUCCESS).pack(pady=20, padx=30, anchor="e")
        self.update_sales_combos()

    def update_sales_combos(self, *args):
        query = self.sales_search_var.get().lower()
        # Ensure only non-insumos appear here (safety check)
        filtered = [f"{p[1]} - ${p[2]:.2f} (S: {p[3]})" for p in self.all_products 
                    if (query in p[1].lower() or (p[4] and query in p[4].lower()))]
        self.prod_combo.configure(values=filtered)
        if filtered:
            self.prod_combo.set(filtered[0])
        else:
            self.prod_combo.set("")

    def load_products(self, query=""):
        for item in self.tree.get_children():
            self.tree.delete(item)
        query = query.lower()
        for prod in get_products():
            if query in prod[1].lower() or query in str(prod[4]).lower():
                p_list = list(prod)
                p_list[2] = f"${p_list[2]:.2f}"
                # The DB now has 'type' at index 5 potentially, but SELECT * might return it
                # I should check database.py SELECT * output
                self.tree.insert("", "end", values=p_list)

    def edit_selected_product(self):
        selected = self.tree.selection()
        if not selected: return
        # Format: (ID, Name, Price, Stock, Category, Type)
        prod = self.tree.item(selected[0], "values")
        
        # Check if it's an Insumo (index 5)
        if len(prod) > 5 and prod[5] == "INSUMO":
            messagebox.showwarning("Restricción", "Los insumos no se pueden modificar directamente para preservar la integridad de los costos y compras.")
            return
            
        self.open_product_window(prod)

    def delete_selected_product(self):
        selected = self.tree.selection()
        if not selected: return
        pid = self.tree.item(selected[0])['values'][0]
        if messagebox.askyesno("Confirmar", "¿Eliminar?"):
            delete_product(pid)
            self.load_products()

    def open_product_window(self, product=None):
        win = ctk.CTkToplevel(self)
        win.title("Producto")
        win.geometry("480x650")
        win.configure(fg_color=Styles.BG_COLOR)
        win.attributes("-topmost", True)
        win.grab_set()

        # Main scrollable container
        scroll_container = ctk.CTkScrollableFrame(win, fg_color="transparent", corner_radius=0)
        scroll_container.pack(fill="both", expand=True, padx=5, pady=5)

        form = self.create_card(scroll_container, "Detalles del Producto")
        form.pack(padx=10, pady=10, fill="both")

        entries = {}
        
        # Category entry (always visible)
        ctk.CTkLabel(form, text="Categoría").pack(pady=2, padx=20, anchor="w")
        entries["cat"] = ctk.CTkEntry(form, width=300)
        entries["cat"].pack(pady=5, padx=20)

        ctk.CTkLabel(form, text="Nombre del Item").pack(pady=2, padx=20, anchor="w")
        entries["name"] = ctk.CTkEntry(form, width=300)
        entries["name"].pack(pady=5, padx=20)

        # Type selector (now with 3 explicit options)
        ctk.CTkLabel(form, text="Tipo de Item:").pack(pady=2, padx=20, anchor="w")
        type_options = ["PRODUCTO SIMPLE", "INSUMO", "PRODUCTO COMPUESTO"]
        
        # Mapping old DB values to new UI values
        initial_type = "PRODUCTO SIMPLE"
        if product and len(product) > 5:
            db_type = product[5]
            if db_type == "INSUMO": initial_type = "INSUMO"
            elif db_type == "COMPUESTO": initial_type = "PRODUCTO COMPUESTO"
        
        type_var = ctk.StringVar(value=initial_type)
        type_menu = ctk.CTkSegmentedButton(form, values=type_options, variable=type_var)
        type_menu.pack(pady=5, padx=20)

        # Price section (visible for Products, hidden for Insumos)
        price_frame = ctk.CTkFrame(form, fg_color="transparent")
        ctk.CTkLabel(price_frame, text="Precio de Venta ($)").pack(pady=2, anchor="w")
        entries["price"] = ctk.CTkEntry(price_frame, width=300)
        entries["price"].pack(pady=5)

        ctk.CTkLabel(form, text="(El stock se gestiona en la pestaña 'Caja/Compras')", font=("Arial", 10), text_color="gray").pack(pady=2)

        # Unit section
        unit_frame = ctk.CTkFrame(form, fg_color="transparent")
        ctk.CTkLabel(unit_frame, text="Unidad de Medida (ml, gr, unid...)").pack(pady=2, anchor="w")
        entries["unit"] = ctk.CTkEntry(unit_frame, width=300)
        entries["unit"].pack(pady=5)
        entries["unit"].insert(0, "unid")

        if product:
            entries["name"].insert(0, product[1])
            entries["price"].insert(0, str(product[2]).replace("$", "").replace(".00", ""))
            entries["cat"].insert(0, product[4])
            if len(product) > 6:
                entries["unit"].delete(0, "end")
                entries["unit"].insert(0, product[6])

        # Recipe/Composition Section (only if COMPUESTO)
        recipe_frame = ctk.CTkFrame(win, fg_color="transparent")
        
        def toggle_ui(*args):
            p_type = type_var.get()
            if p_type in ["PRODUCTO SIMPLE", "PRODUCTO COMPUESTO"]:
                price_frame.pack(pady=5, padx=20, fill="x")
            else:
                price_frame.pack_forget()
                
            if p_type == "INSUMO":
                unit_frame.pack(pady=5, padx=20, fill="x")
            else:
                # We can keep it or hide it, but user mentioned it for Insumos
                unit_frame.pack(pady=5, padx=20, fill="x")
                
            if p_type == "PRODUCTO COMPUESTO":
                recipe_frame.pack(pady=10, padx=20, fill="both", expand=True)
            else:
                recipe_frame.pack_forget()
        
        type_var.trace("w", toggle_ui)
        
        ctk.CTkLabel(recipe_frame, text="Compuesto por (Uno o más productos):", font=Styles.FONT_LABEL).pack(pady=5, anchor="w")
        recipe_list = ctk.CTkScrollableFrame(recipe_frame, height=150)
        recipe_list.pack(fill="both", expand=True)
        
        ingredient_items = [] # List of (combo, qty_entry)
        
        all_prods = get_products()
        # Allow any existing product to be an ingredient
        item_choices = [f"{p[1]} (ID: {p[0]})" for p in all_prods]

        def add_ingredient_row(ing_id=None, qty=1):
            row = ctk.CTkFrame(recipe_list, fg_color="transparent")
            row.pack(fill="x", pady=2)
            
            # Label/Button combo instead of ComboBox for "Picking"
            item_id_var = ctk.StringVar(value=str(ing_id) if ing_id else "")
            name_var = ctk.StringVar(value="Seleccionar Item...")
            unit_var = ctk.StringVar(value="")
            
            if ing_id:
                matching = [p for p in all_prods if p[0] == ing_id]
                if matching: 
                    name_var.set(matching[0][1])
                    if len(matching[0]) > 6: unit_var.set(f"({matching[0][6]})")

            def pick_item(p, nv, iv, uv):
                nv.set(p[1])
                iv.set(str(p[0]))
                if len(p) > 6: uv.set(f"({p[6]})")
                else: uv.set("(unid)")

            btn = ctk.CTkButton(row, textvariable=name_var, width=180, anchor="w", 
                                fg_color=Styles.CARD_BG, border_width=1, border_color=Styles.BORDER_COLOR,
                                text_color=Styles.TEXT_COLOR,
                                command=lambda: self.open_product_picker(lambda p: pick_item(p, name_var, item_id_var, unit_var)))
            btn.pack(side="left", padx=2)
            
            # Unit label
            ctk.CTkLabel(row, textvariable=unit_var, font=("Arial", 10), width=40).pack(side="left", padx=2)

            qe = ctk.CTkEntry(row, width=60)
            qe.pack(side="left", padx=2)
            qe.insert(0, str(qty))
            
            ctk.CTkButton(row, text="X", width=30, fg_color=Styles.DANGER, command=lambda: remove_row(row, (item_id_var, qe, row))).pack(side="right")
            ingredient_items.append((item_id_var, qe, row))

        def remove_row(row, item):
            if item in ingredient_items:
                ingredient_items.remove(item)
            row.destroy()

        ctk.CTkButton(recipe_frame, text="+ Añadir Ingrediente", command=add_ingredient_row, height=25).pack(pady=5)

        if product:
            # Load existing recipe
            recipe_data = get_recipe(product[0])
            for ing_id, name, qty in recipe_data:
                add_ingredient_row(ing_id, qty)
        
        toggle_ui() # Initial check

        def save():
            try:
                name = entries["name"].get().strip()
                price_str = entries["price"].get().strip()
                category = entries["cat"].get().strip()
                unit = entries["unit"].get().strip()
                ui_type = type_var.get()
                
                # Convert UI type to DB type
                p_type = "PRODUCTO"
                if ui_type == "INSUMO": p_type = "INSUMO"
                elif ui_type == "PRODUCTO COMPUESTO": p_type = "COMPUESTO"

                if not name:
                    messagebox.showerror("Error", "Falta el nombre")
                    return

                # Price is mandatory for Products
                if ui_type != "INSUMO":
                    try:
                        price = float(price_str)
                    except:
                        messagebox.showerror("Error", "Precio de venta inválido")
                        return
                else:
                    price = product[2] if product else 0

                stock = product[3] if product else 0

                if product: 
                    update_product(product[0], name, price, stock, category, p_type, unit)
                    pid = product[0]
                else: 
                    add_product(name, price, stock, category, p_type, unit)
                    # Need to get the last ID for new product
                    pid = get_products()[-1][0]
                
                # Save Recipe/Composition
                delete_recipe(pid)
                if ui_type == "PRODUCTO COMPUESTO":
                    for iv, qe, r in ingredient_items:
                        sel_id = iv.get()
                        if sel_id:
                            add_recipe_item(pid, int(sel_id), float(qe.get()))
                
                self.load_products()
                win.destroy()
                messagebox.showinfo("Éxito", "Guardado correctamente")
            except Exception as e:
                messagebox.showerror("Error", f"Error: {str(e)}")

        ctk.CTkButton(scroll_container, text="Guardar Cambios", command=save, fg_color=Styles.ACCENT_COLOR, text_color="black").pack(pady=20)

    def show_history(self):
        self.clear_container()
        ctk.CTkLabel(self.main_container, text="HISTORIAL DE MOVIMIENTOS (VENTAS Y ABONOS)", font=Styles.FONT_SUBHEADER).pack(pady=(0, 20), anchor="w")
        table_card = self.create_card(self.main_container)
        table_card.pack(fill="both", expand=True)

        # Columns: ID, Tipo (VENTA/PAGO), Detalle (Producto/Usuario), Info/Método (Cant/Nequi/Efectivo), Total, Fecha
        columns = ("ID", "Tipo", "Detalle", "Info/Método", "Total", "Fecha")
        tree = self.create_styled_tree(table_card, columns)
        
        for trans in get_combined_history():
            t_list = list(trans)
            t_list[4] = f"${t_list[4]:.2f}"
            tree.insert("", "end", values=t_list)

    def show_financial_summary(self):
        self.clear_container()
        
        scroll = ctk.CTkScrollableFrame(self.main_container, fg_color="transparent")
        scroll.pack(fill="both", expand=True)

        header = ctk.CTkFrame(scroll, fg_color="transparent")
        header.pack(fill="x", pady=(0, 20))
        ctk.CTkLabel(header, text="RESUMEN FINANCIERO Y ENTRADAS", font=Styles.FONT_SUBHEADER).pack(side="left")
        
        ctk.CTkButton(header, text="+ REGISTRAR ENTRADA (COMPRA)", command=self.open_purchase_window,
                      fg_color=Styles.ACCENT_COLOR, text_color="black").pack(side="right")

        # Top Stats
        total_s, total_p, user_stats = get_financial_summary()
        
        stats_frame = ctk.CTkFrame(scroll, fg_color="transparent")
        stats_frame.pack(fill="x", pady=10)
        
        # Total Sales Card
        c1 = self.create_card(stats_frame, "Ingresos (Ventas)")
        c1.pack(side="left", fill="both", expand=True, padx=5)
        ctk.CTkLabel(c1, text=f"${total_s:.2f}", font=Styles.FONT_HEADER, text_color=Styles.SUCCESS).pack(pady=10)

        # Total Purchases Card
        c2 = self.create_card(stats_frame, "Inversión (Compras)")
        c2.pack(side="left", fill="both", expand=True, padx=5)
        ctk.CTkLabel(c2, text=f"${total_p:.2f}", font=Styles.FONT_HEADER, text_color=Styles.DANGER).pack(pady=10)

        # Profit Card
        c3 = self.create_card(stats_frame, "Balance Neto")
        c3.pack(side="left", fill="both", expand=True, padx=5)
        balance_color = Styles.SUCCESS if (total_s - total_p) >= 0 else Styles.DANGER
        ctk.CTkLabel(c3, text=f"${(total_s - total_p):.2f}", font=Styles.FONT_HEADER, text_color=balance_color).pack(pady=10)

        # User Sales List
        list_card = self.create_card(scroll, "Ventas por Cliente")
        list_card.pack(fill="both", expand=True, pady=10)
        
        ctk.CTkLabel(list_card, text="(Doble clic para ver historial completo de cartera)", font=("Arial", 10), text_color="gray").pack(pady=2)

        columns = ("ID", "Cliente", "Total Comprado", "Saldo Actual")
        tree = self.create_styled_tree(list_card, columns)
        
        # Hide the ID column
        tree.column("ID", width=0, stretch=False)
        
        for uid, name, amount, balance in user_stats:
            tree.insert("", "end", values=(uid, name, f"${amount:.2f}", f"${balance:.2f}"))

        def open_detailed_from_summary(event):
            selected = tree.selection()
            if not selected: return
            data = tree.item(selected[0])['values']
            self.open_user_details_window(user_id=data[0], user_name=data[1], balance=data[3])

        tree.bind("<Double-1>", open_detailed_from_summary)

    def open_purchase_window(self):
        win = ctk.CTkToplevel(self)
        win.title("Registrar Entrada")
        win.geometry("450x550")
        win.attributes("-topmost", True)
        win.grab_set()

        scroll = ctk.CTkScrollableFrame(win, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=5, pady=5)

        form = self.create_card(scroll, "Entrada de Mercancía")
        form.pack(padx=10, pady=10, fill="both")

        ctk.CTkLabel(form, text="Producto / Insumo:").pack(pady=5, anchor="w", padx=20)
        prods = get_products()
        prod_names = [f"{p[1]} [{p[5]}] (Stock: {p[3]})" for p in prods]
        prod_combo = ctk.CTkComboBox(form, values=prod_names, width=300)
        prod_combo.pack(pady=5, padx=20)

        ctk.CTkLabel(form, text="Cantidad que entra:").pack(pady=5, anchor="w", padx=20)
        qty_frame = ctk.CTkFrame(form, fg_color="transparent")
        qty_frame.pack(fill="x", padx=20)
        qty_e = ctk.CTkEntry(qty_frame, width=200)
        qty_e.pack(side="left", pady=5)
        
        unit_label_p = ctk.CTkLabel(qty_frame, text="(unid)", font=Styles.FONT_BODY)
        unit_label_p.pack(side="left", padx=10)

        cost_prompt_label = ctk.CTkLabel(form, text="Costo Total de esta compra ($):", anchor="w")
        cost_prompt_label.pack(pady=5, anchor="w", padx=20)
        cost_e = ctk.CTkEntry(form, width=300)
        cost_e.pack(pady=5, padx=20)

        # Dynamic cost feedback
        cost_label = ctk.CTkLabel(form, text="-- Esperando valores --", font=Styles.FONT_LABEL, text_color=Styles.ACCENT_COLOR)
        cost_label.pack(pady=10)

        def on_prod_change(choice):
            matching = [p for p in prods if f"{p[1]} [{p[5]}]" in choice]
            if matching:
                prod = matching[0]
                if len(prod) > 6: unit_label_p.configure(text=f"({prod[6]})")
                else: unit_label_p.configure(text="(unid)")
                
                # Logic: INSUMO = Total Cost | PRODUCTO = Unit Price
                if prod[5] == "INSUMO":
                    cost_prompt_label.configure(text="Costo TOTAL de esta compra ($):")
                else:
                    cost_prompt_label.configure(text="Costo UNITARIO por item ($):")
            else:
                unit_label_p.configure(text="(unid)")
                cost_prompt_label.configure(text="Costo Total de esta compra ($):")
            
            update_suggested_cost()

        prod_combo.configure(command=on_prod_change)

        def update_suggested_cost(*args):
            try:
                q = float(qty_e.get())
                c = float(cost_e.get())
                sel = prod_combo.get()
                matching = [p for p in prods if f"{p[1]} [{p[5]}]" in sel]
                p_type = matching[0][5] if matching else "PRODUCTO"

                if q > 0:
                    if p_type == "INSUMO":
                        cost_label.configure(text=f"Valor Unitario Resultante: ${c/q:.2f}")
                    else:
                        cost_label.configure(text=f"Inversión Total Estimada: ${c*q:.2f}")
            except:
                cost_label.configure(text="-- Esperando valores --")

        qty_e.bind("<KeyRelease>", update_suggested_cost)
        cost_e.bind("<KeyRelease>", update_suggested_cost)

        def save():
            try:
                sel = prod_combo.get()
                matching = [p for p in prods if f"{p[1]} [{p[5]}]" in sel]
                if not matching: return
                prod = matching[0]
                p_id, p_type = prod[0], prod[5]
                
                q, c = float(qty_e.get()), float(cost_e.get())
                
                # Financial Total: Total for Insumo, Unit*Qty for Product
                cost_to_record = c
                if p_type != "INSUMO":
                    cost_to_record = c * q
                
                record_purchase(p_id, q, cost_to_record)
                
                if p_type == "INSUMO":
                    update_ingredient_unit_cost(p_id, c, q)
                
                win.destroy()
                self.show_financial_summary()
                msg = f"Entrada registrada satisfactoriamente."
                if p_type == "INSUMO":
                    msg += f"\nEl costo de '{prod[1]}' se actualizó a ${c/q:.2f} por unidad."
                messagebox.showinfo("Éxito", msg)
            except Exception as e:
                messagebox.showerror("Error", f"Datos inválidos: {str(e)}")

        ctk.CTkButton(scroll, text="Guardar Entrada", command=save, fg_color=Styles.ACCENT_COLOR, text_color="black").pack(pady=20)

    def open_product_picker(self, callback):
        win = ctk.CTkToplevel(self)
        win.title("Seleccionar Item")
        win.geometry("700x500") # Increased size
        win.attributes("-topmost", True)
        win.grab_set()

        ctk.CTkLabel(win, text="Selecciona el item de la lista (Doble clic para confirmar):", font=Styles.FONT_LABEL).pack(pady=10)
        
        container = ctk.CTkFrame(win, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=20, pady=(0, 10))
        
        columns = ("ID", "Nombre", "Precio", "Stock", "Tipo")
        tree = self.create_styled_tree(container, columns)
        
        for p in get_products():
            tree.insert("", "end", values=p)

        def select():
            selected = tree.selection()
            if not selected: return
            item_data = tree.item(selected[0], "values")
            callback(item_data)
            win.destroy()

        # Add double-click to select
        tree.bind("<Double-1>", lambda e: select())

        btn = ctk.CTkButton(win, text="Confirmar Selección", command=select, 
                            fg_color=Styles.ACCENT_COLOR, text_color="black", height=40)
        btn.pack(pady=15)

if __name__ == "__main__":
    app = AfterwordApp()
    app.mainloop()
