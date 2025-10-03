"""
Interfaz Gráfica para el Sistema de Gestión de Biblioteca
========================================================

Este módulo contiene la implementación de la interfaz gráfica usando Tkinter
para el sistema de gestión de biblioteca. Proporciona una interfaz intuitiva
para gestionar libros, usuarios y préstamos.

Autor: [Tu nombre]
Fecha: 2024
Curso: Estructuras de Datos - Unidad 1
"""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from modelos import BibliotecaManager
from datetime import datetime

class BibliotecaGUI:
    """
    Clase principal de la interfaz gráfica del sistema de biblioteca.
    
    Proporciona una interfaz completa para:
    - Gestión de libros (registro, búsqueda, eliminación)
    - Gestión de usuarios (registro, búsqueda)
    - Gestión de préstamos (realizar, devolver, consultar)
    - Visualización de estadísticas y reportes
    """
    
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Gestión de Biblioteca - Estructuras de Datos Lineales")
        self.root.geometry("1200x800")
        self.root.configure(bg='#f0f0f0')
        
        # Inicializar el gestor de la biblioteca
        self.biblioteca = BibliotecaManager()
        
        # Crear el estilo personalizado
        self.setup_styles()
        
        # Crear la interfaz principal
        self.create_main_interface()
        
        # Actualizar estadísticas al inicio
        self.update_statistics()
    
    def setup_styles(self):
        """Configura los estilos personalizados para la interfaz."""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Estilo para botones principales
        style.configure('Main.TButton', 
                       padding=(10, 5),
                       font=('Arial', 10, 'bold'))
        
        # Estilo para labels de títulos
        style.configure('Title.TLabel',
                       font=('Arial', 14, 'bold'),
                       background='#f0f0f0')
        
        # Estilo para estadísticas
        style.configure('Stats.TLabel',
                       font=('Arial', 12),
                       background='#e6f3ff',
                       padding=5)
    
    def create_main_interface(self):
        """Crea la interfaz principal con pestañas."""
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configurar redimensionado
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # Título principal
        title_label = ttk.Label(main_frame, 
                               text="Sistema de Gestión de Biblioteca", 
                               style='Title.TLabel')
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Panel de estadísticas (izquierda)
        self.create_statistics_panel(main_frame)
        
        # Panel de pestañas (derecha)
        self.create_tabs_panel(main_frame)
    
    def create_statistics_panel(self, parent):
        """Crea el panel de estadísticas en tiempo real."""
        stats_frame = ttk.LabelFrame(parent, text="Estadísticas del Sistema", padding="10")
        stats_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        
        # Variables para las estadísticas
        self.stats_vars = {
            'total_libros': tk.StringVar(value="0"),
            'libros_disponibles': tk.StringVar(value="0"),
            'libros_prestados': tk.StringVar(value="0"),
            'total_usuarios': tk.StringVar(value="0"),
            'prestamos_activos': tk.StringVar(value="0"),
            'solicitudes_pendientes': tk.StringVar(value="0")
        }
        
        # Labels de estadísticas
        stats_labels = [
            ("Total de Libros:", self.stats_vars['total_libros']),
            ("Libros Disponibles:", self.stats_vars['libros_disponibles']),
            ("Libros Prestados:", self.stats_vars['libros_prestados']),
            ("Total de Usuarios:", self.stats_vars['total_usuarios']),
            ("Préstamos Activos:", self.stats_vars['prestamos_activos']),
            ("Solicitudes Pendientes:", self.stats_vars['solicitudes_pendientes'])
        ]
        
        for i, (label_text, var) in enumerate(stats_labels):
            ttk.Label(stats_frame, text=label_text, font=('Arial', 10, 'bold')).grid(
                row=i, column=0, sticky=tk.W, pady=5)
            ttk.Label(stats_frame, textvariable=var, style='Stats.TLabel').grid(
                row=i, column=1, sticky=(tk.W, tk.E), padx=(10, 0), pady=5)
        
        # Botón de actualizar estadísticas
        ttk.Button(stats_frame, text="Actualizar Estadísticas", 
                  command=self.update_statistics, style='Main.TButton').grid(
                  row=len(stats_labels), column=0, columnspan=2, pady=(20, 0))
        
        # Configurar redimensionado
        stats_frame.columnconfigure(1, weight=1)
    
    def create_tabs_panel(self, parent):
        """Crea el panel de pestañas con las diferentes funcionalidades."""
        notebook = ttk.Notebook(parent)
        notebook.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Pestaña de Libros
        self.create_books_tab(notebook)
        
        # Pestaña de Usuarios
        self.create_users_tab(notebook)
        
        # Pestaña de Préstamos
        self.create_loans_tab(notebook)
        
        # Pestaña de Historial
        self.create_history_tab(notebook)
    
    def create_books_tab(self, notebook):
        """Crea la pestaña de gestión de libros."""
        books_frame = ttk.Frame(notebook, padding="10")
        notebook.add(books_frame, text="Gestión de Libros")
        
        # Frame para registro de libros
        register_frame = ttk.LabelFrame(books_frame, text="Registrar Nuevo Libro", padding="10")
        register_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Campos de entrada
        ttk.Label(register_frame, text="ISBN:").grid(row=0, column=0, sticky=tk.W)
        self.isbn_entry = ttk.Entry(register_frame, width=20)
        self.isbn_entry.grid(row=0, column=1, padx=(5, 20))
        
        ttk.Label(register_frame, text="Título:").grid(row=0, column=2, sticky=tk.W)
        self.title_entry = ttk.Entry(register_frame, width=30)
        self.title_entry.grid(row=0, column=3, padx=(5, 0))
        
        ttk.Label(register_frame, text="Autor:").grid(row=1, column=0, sticky=tk.W)
        self.author_entry = ttk.Entry(register_frame, width=20)
        self.author_entry.grid(row=1, column=1, padx=(5, 20), pady=(5, 0))
        
        ttk.Label(register_frame, text="Categoría:").grid(row=1, column=2, sticky=tk.W)
        self.category_entry = ttk.Entry(register_frame, width=20)
        self.category_entry.grid(row=1, column=3, padx=(5, 0), pady=(5, 0))
        
        ttk.Label(register_frame, text="Año:").grid(row=2, column=0, sticky=tk.W)
        self.year_entry = ttk.Entry(register_frame, width=10)
        self.year_entry.grid(row=2, column=1, padx=(5, 20), pady=(5, 0))
        
        ttk.Button(register_frame, text="Registrar Libro", 
                  command=self.register_book, style='Main.TButton').grid(
                  row=2, column=2, columnspan=2, pady=(5, 0))
        
        # Frame para búsqueda de libros
        search_frame = ttk.LabelFrame(books_frame, text="Buscar Libros", padding="10")
        search_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Label(search_frame, text="Buscar por:").grid(row=0, column=0, sticky=tk.W)
        self.book_search_combo = ttk.Combobox(search_frame, 
                                            values=["titulo", "autor", "categoria", "isbn"],
                                            state="readonly", width=15)
        self.book_search_combo.grid(row=0, column=1, padx=(5, 10))
        self.book_search_combo.set("titulo")
        
        ttk.Label(search_frame, text="Valor:").grid(row=0, column=2, sticky=tk.W)
        self.book_search_entry = ttk.Entry(search_frame, width=20)
        self.book_search_entry.grid(row=0, column=3, padx=(5, 10))
        
        ttk.Button(search_frame, text="Buscar", 
                  command=self.search_books).grid(row=0, column=4)
        ttk.Button(search_frame, text="Mostrar Todos", 
                  command=self.show_all_books).grid(row=0, column=5, padx=(5, 0))
        
        # Tabla de libros
        self.create_books_table(books_frame)
        
        # Configurar redimensionado
        books_frame.columnconfigure(0, weight=1)
        books_frame.rowconfigure(2, weight=1)
        register_frame.columnconfigure(3, weight=1)
        search_frame.columnconfigure(3, weight=1)
    
    def create_books_table(self, parent):
        """Crea la tabla para mostrar los libros."""
        table_frame = ttk.LabelFrame(parent, text="Lista de Libros", padding="10")
        table_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Crear Treeview
        columns = ("ISBN", "Título", "Autor", "Categoría", "Año", "Estado")
        self.books_tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=15)
        
        # Configurar columnas
        self.books_tree.heading("ISBN", text="ISBN")
        self.books_tree.heading("Título", text="Título")
        self.books_tree.heading("Autor", text="Autor")
        self.books_tree.heading("Categoría", text="Categoría")
        self.books_tree.heading("Año", text="Año")
        self.books_tree.heading("Estado", text="Estado")
        
        self.books_tree.column("ISBN", width=120)
        self.books_tree.column("Título", width=200)
        self.books_tree.column("Autor", width=150)
        self.books_tree.column("Categoría", width=100)
        self.books_tree.column("Año", width=60)
        self.books_tree.column("Estado", width=80)
        
        # Scrollbars
        books_scrolly = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.books_tree.yview)
        books_scrollx = ttk.Scrollbar(table_frame, orient=tk.HORIZONTAL, command=self.books_tree.xview)
        self.books_tree.configure(yscrollcommand=books_scrolly.set, xscrollcommand=books_scrollx.set)
        
        # Grid
        self.books_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        books_scrolly.grid(row=0, column=1, sticky=(tk.N, tk.S))
        books_scrollx.grid(row=1, column=0, sticky=(tk.W, tk.E))
        
        # Botones de acciones
        actions_frame = ttk.Frame(table_frame)
        actions_frame.grid(row=2, column=0, columnspan=2, pady=(10, 0))
        
        ttk.Button(actions_frame, text="Eliminar Libro Seleccionado", 
                  command=self.delete_selected_book).pack(side=tk.LEFT, padx=(0, 10))
        
        # Configurar redimensionado
        table_frame.columnconfigure(0, weight=1)
        table_frame.rowconfigure(0, weight=1)
        
        # Poblar la tabla inicialmente
        self.populate_books_table()
    
    def create_users_tab(self, notebook):
        """Crea la pestaña de gestión de usuarios."""
        users_frame = ttk.Frame(notebook, padding="10")
        notebook.add(users_frame, text="Gestión de Usuarios")
        
        # Frame para registro de usuarios
        register_frame = ttk.LabelFrame(users_frame, text="Registrar Nuevo Usuario", padding="10")
        register_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Label(register_frame, text="Nombre:").grid(row=0, column=0, sticky=tk.W)
        self.user_name_entry = ttk.Entry(register_frame, width=30)
        self.user_name_entry.grid(row=0, column=1, padx=(5, 20))
        
        ttk.Label(register_frame, text="Email:").grid(row=0, column=2, sticky=tk.W)
        self.user_email_entry = ttk.Entry(register_frame, width=30)
        self.user_email_entry.grid(row=0, column=3, padx=(5, 0))
        
        ttk.Label(register_frame, text="Teléfono:").grid(row=1, column=0, sticky=tk.W)
        self.user_phone_entry = ttk.Entry(register_frame, width=20)
        self.user_phone_entry.grid(row=1, column=1, padx=(5, 20), pady=(5, 0))
        
        ttk.Button(register_frame, text="Registrar Usuario", 
                  command=self.register_user, style='Main.TButton').grid(
                  row=1, column=2, columnspan=2, pady=(5, 0))
        
        # Frame para búsqueda de usuarios
        search_frame = ttk.LabelFrame(users_frame, text="Buscar Usuarios", padding="10")
        search_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Label(search_frame, text="Buscar por:").grid(row=0, column=0, sticky=tk.W)
        self.user_search_combo = ttk.Combobox(search_frame, 
                                            values=["nombre", "email", "id"],
                                            state="readonly", width=15)
        self.user_search_combo.grid(row=0, column=1, padx=(5, 10))
        self.user_search_combo.set("nombre")
        
        ttk.Label(search_frame, text="Valor:").grid(row=0, column=2, sticky=tk.W)
        self.user_search_entry = ttk.Entry(search_frame, width=20)
        self.user_search_entry.grid(row=0, column=3, padx=(5, 10))
        
        ttk.Button(search_frame, text="Buscar", 
                  command=self.search_users).grid(row=0, column=4)
        ttk.Button(search_frame, text="Mostrar Todos", 
                  command=self.show_all_users).grid(row=0, column=5, padx=(5, 0))
        
        # Tabla de usuarios
        self.create_users_table(users_frame)
        
        # Configurar redimensionado
        users_frame.columnconfigure(0, weight=1)
        users_frame.rowconfigure(2, weight=1)
    
    def create_users_table(self, parent):
        """Crea la tabla para mostrar los usuarios."""
        table_frame = ttk.LabelFrame(parent, text="Lista de Usuarios", padding="10")
        table_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Crear Treeview
        columns = ("ID", "Nombre", "Email", "Teléfono", "Fecha Registro", "Préstamos Activos")
        self.users_tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=15)
        
        # Configurar columnas
        for col in columns:
            self.users_tree.heading(col, text=col)
        
        self.users_tree.column("ID", width=80)
        self.users_tree.column("Nombre", width=200)
        self.users_tree.column("Email", width=200)
        self.users_tree.column("Teléfono", width=120)
        self.users_tree.column("Fecha Registro", width=120)
        self.users_tree.column("Préstamos Activos", width=120)
        
        # Scrollbars
        users_scrolly = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.users_tree.yview)
        users_scrollx = ttk.Scrollbar(table_frame, orient=tk.HORIZONTAL, command=self.users_tree.xview)
        self.users_tree.configure(yscrollcommand=users_scrolly.set, xscrollcommand=users_scrollx.set)
        
        # Grid
        self.users_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        users_scrolly.grid(row=0, column=1, sticky=(tk.N, tk.S))
        users_scrollx.grid(row=1, column=0, sticky=(tk.W, tk.E))
        
        # Configurar redimensionado
        table_frame.columnconfigure(0, weight=1)
        table_frame.rowconfigure(0, weight=1)
        
        # Poblar la tabla inicialmente
        self.populate_users_table()
    
    def create_loans_tab(self, notebook):
        """Crea la pestaña de gestión de préstamos."""
        loans_frame = ttk.Frame(notebook, padding="10")
        notebook.add(loans_frame, text="Gestión de Préstamos")
        
        # Frame para realizar préstamos
        loan_frame = ttk.LabelFrame(loans_frame, text="Realizar Préstamo", padding="10")
        loan_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Label(loan_frame, text="ISBN del Libro:").grid(row=0, column=0, sticky=tk.W)
        self.loan_isbn_entry = ttk.Entry(loan_frame, width=20)
        self.loan_isbn_entry.grid(row=0, column=1, padx=(5, 20))
        
        ttk.Label(loan_frame, text="ID del Usuario:").grid(row=0, column=2, sticky=tk.W)
        self.loan_user_entry = ttk.Entry(loan_frame, width=15)
        self.loan_user_entry.grid(row=0, column=3, padx=(5, 10))
        
        ttk.Button(loan_frame, text="Realizar Préstamo", 
                  command=self.make_loan, style='Main.TButton').grid(
                  row=0, column=4)
        
        # Frame para devolución
        return_frame = ttk.LabelFrame(loans_frame, text="Devolver Libro", padding="10")
        return_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Label(return_frame, text="ID del Préstamo:").grid(row=0, column=0, sticky=tk.W)
        self.return_loan_entry = ttk.Entry(return_frame, width=15)
        self.return_loan_entry.grid(row=0, column=1, padx=(5, 20))
        
        ttk.Button(return_frame, text="Devolver Libro", 
                  command=self.return_book, style='Main.TButton').grid(
                  row=0, column=2)
        
        # Tabla de préstamos activos
        self.create_loans_table(loans_frame)
        
        # Configurar redimensionado
        loans_frame.columnconfigure(0, weight=1)
        loans_frame.rowconfigure(2, weight=1)
    
    def create_loans_table(self, parent):
        """Crea la tabla para mostrar los préstamos activos."""
        table_frame = ttk.LabelFrame(parent, text="Préstamos Activos", padding="10")
        table_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Crear Treeview
        columns = ("ID Préstamo", "ISBN Libro", "ID Usuario", "Fecha Préstamo", "Fecha Vencimiento", "Días Restantes", "Estado")
        self.loans_tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=12)
        
        # Configurar columnas
        for col in columns:
            self.loans_tree.heading(col, text=col)
        
        self.loans_tree.column("ID Préstamo", width=100)
        self.loans_tree.column("ISBN Libro", width=120)
        self.loans_tree.column("ID Usuario", width=80)
        self.loans_tree.column("Fecha Préstamo", width=120)
        self.loans_tree.column("Fecha Vencimiento", width=120)
        self.loans_tree.column("Días Restantes", width=100)
        self.loans_tree.column("Estado", width=80)
        
        # Scrollbars
        loans_scrolly = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.loans_tree.yview)
        loans_scrollx = ttk.Scrollbar(table_frame, orient=tk.HORIZONTAL, command=self.loans_tree.xview)
        self.loans_tree.configure(yscrollcommand=loans_scrolly.set, xscrollcommand=loans_scrollx.set)
        
        # Grid
        self.loans_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        loans_scrolly.grid(row=0, column=1, sticky=(tk.N, tk.S))
        loans_scrollx.grid(row=1, column=0, sticky=(tk.W, tk.E))
        
        # Configurar redimensionado
        table_frame.columnconfigure(0, weight=1)
        table_frame.rowconfigure(0, weight=1)
        
        # Poblar la tabla inicialmente
        self.populate_loans_table()
    
    def create_history_tab(self, notebook):
        """Crea la pestaña de historial y estadísticas avanzadas."""
        history_frame = ttk.Frame(notebook, padding="10")
        notebook.add(history_frame, text="Historial y Reportes")
        
        # Frame para historial de préstamos
        history_loans_frame = ttk.LabelFrame(history_frame, text="Historial Reciente de Préstamos", padding="10")
        history_loans_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Tabla de historial
        columns = ("ID Préstamo", "ISBN Libro", "Título", "Usuario", "Fecha Préstamo", "Estado")
        self.history_tree = ttk.Treeview(history_loans_frame, columns=columns, show="headings", height=20)
        
        # Configurar columnas
        for col in columns:
            self.history_tree.heading(col, text=col)
        
        self.history_tree.column("ID Préstamo", width=100)
        self.history_tree.column("ISBN Libro", width=120)
        self.history_tree.column("Título", width=200)
        self.history_tree.column("Usuario", width=100)
        self.history_tree.column("Fecha Préstamo", width=120)
        self.history_tree.column("Estado", width=80)
        
        # Scrollbars para historial
        history_scrolly = ttk.Scrollbar(history_loans_frame, orient=tk.VERTICAL, command=self.history_tree.yview)
        history_scrollx = ttk.Scrollbar(history_loans_frame, orient=tk.HORIZONTAL, command=self.history_tree.xview)
        self.history_tree.configure(yscrollcommand=history_scrolly.set, xscrollcommand=history_scrollx.set)
        
        # Grid para historial
        self.history_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        history_scrolly.grid(row=0, column=1, sticky=(tk.N, tk.S))
        history_scrollx.grid(row=1, column=0, sticky=(tk.W, tk.E))
        
        # Botón para actualizar historial
        ttk.Button(history_loans_frame, text="Actualizar Historial", 
                  command=self.populate_history_table).grid(row=2, column=0, pady=(10, 0))
        
        # Configurar redimensionado
        history_frame.columnconfigure(0, weight=1)
        history_frame.rowconfigure(0, weight=1)
        history_loans_frame.columnconfigure(0, weight=1)
        history_loans_frame.rowconfigure(0, weight=1)
        
        # Poblar historial inicialmente
        self.populate_history_table()
    
    # ==================== MÉTODOS DE GESTIÓN DE LIBROS ====================
    
    def register_book(self):
        """Registra un nuevo libro en el sistema."""
        try:
            isbn = self.isbn_entry.get().strip()
            title = self.title_entry.get().strip()
            author = self.author_entry.get().strip()
            category = self.category_entry.get().strip()
            year = int(self.year_entry.get().strip())
            
            if not all([isbn, title, author, category]):
                messagebox.showerror("Error", "Todos los campos son obligatorios")
                return
            
            if self.biblioteca.registrar_libro(isbn, title, author, category, year):
                messagebox.showinfo("Éxito", f"Libro '{title}' registrado correctamente")
                self.clear_book_entries()
                self.populate_books_table()
                self.update_statistics()
            else:
                messagebox.showerror("Error", "El libro ya existe en el sistema")
                
        except ValueError:
            messagebox.showerror("Error", "El año debe ser un número válido")
        except Exception as e:
            messagebox.showerror("Error", f"Error inesperado: {str(e)}")
    
    def clear_book_entries(self):
        """Limpia los campos de entrada de libros."""
        self.isbn_entry.delete(0, tk.END)
        self.title_entry.delete(0, tk.END)
        self.author_entry.delete(0, tk.END)
        self.category_entry.delete(0, tk.END)
        self.year_entry.delete(0, tk.END)
    
    def search_books(self):
        """Busca libros según el criterio especificado."""
        criterion = self.book_search_combo.get()
        value = self.book_search_entry.get().strip()
        
        if not value:
            messagebox.showwarning("Advertencia", "Ingrese un valor de búsqueda")
            return
        
        books = self.biblioteca.buscar_libros(criterion, value)
        self.populate_books_table(books)
    
    def show_all_books(self):
        """Muestra todos los libros."""
        self.book_search_entry.delete(0, tk.END)
        self.populate_books_table()
    
    def populate_books_table(self, books=None):
        """Pobla la tabla de libros."""
        # Limpiar tabla
        for item in self.books_tree.get_children():
            self.books_tree.delete(item)
        
        # Obtener libros
        if books is None:
            books = self.biblioteca.obtener_todos_los_libros()
        
        # Poblar tabla
        for book in books:
            status = "Disponible" if book.disponible else "Prestado"
            self.books_tree.insert("", tk.END, values=(
                book.isbn, book.titulo, book.autor, 
                book.categoria, book.año_publicacion, status
            ))
    
    def delete_selected_book(self):
        """Elimina el libro seleccionado."""
        selection = self.books_tree.selection()
        if not selection:
            messagebox.showwarning("Advertencia", "Seleccione un libro para eliminar")
            return
        
        item = self.books_tree.item(selection[0])
        isbn = item['values'][0]
        title = item['values'][1]
        
        if messagebox.askyesno("Confirmar", f"¿Está seguro de eliminar '{title}'?"):
            if self.biblioteca.eliminar_libro(isbn):
                messagebox.showinfo("Éxito", f"Libro '{title}' eliminado correctamente")
                self.populate_books_table()
                self.update_statistics()
            else:
                messagebox.showerror("Error", "No se pudo eliminar el libro")
    
    # ==================== MÉTODOS DE GESTIÓN DE USUARIOS ====================
    
    def register_user(self):
        """Registra un nuevo usuario en el sistema."""
        try:
            name = self.user_name_entry.get().strip()
            email = self.user_email_entry.get().strip()
            phone = self.user_phone_entry.get().strip()
            
            if not all([name, email, phone]):
                messagebox.showerror("Error", "Todos los campos son obligatorios")
                return
            
            user_id = self.biblioteca.registrar_usuario(name, email, phone)
            if user_id:
                messagebox.showinfo("Éxito", f"Usuario '{name}' registrado con ID: {user_id}")
                self.clear_user_entries()
                self.populate_users_table()
                self.update_statistics()
            else:
                messagebox.showerror("Error", "El email ya está registrado en el sistema")
                
        except Exception as e:
            messagebox.showerror("Error", f"Error inesperado: {str(e)}")
    
    def clear_user_entries(self):
        """Limpia los campos de entrada de usuarios."""
        self.user_name_entry.delete(0, tk.END)
        self.user_email_entry.delete(0, tk.END)
        self.user_phone_entry.delete(0, tk.END)
    
    def search_users(self):
        """Busca usuarios según el criterio especificado."""
        criterion = self.user_search_combo.get()
        value = self.user_search_entry.get().strip()
        
        if not value:
            messagebox.showwarning("Advertencia", "Ingrese un valor de búsqueda")
            return
        
        users = self.biblioteca.buscar_usuarios(criterion, value)
        self.populate_users_table(users)
    
    def show_all_users(self):
        """Muestra todos los usuarios."""
        self.user_search_entry.delete(0, tk.END)
        self.populate_users_table()
    
    def populate_users_table(self, users=None):
        """Pobla la tabla de usuarios."""
        # Limpiar tabla
        for item in self.users_tree.get_children():
            self.users_tree.delete(item)
        
        # Obtener usuarios
        if users is None:
            users = self.biblioteca.obtener_todos_los_usuarios()
        
        # Poblar tabla
        for user in users:
            self.users_tree.insert("", tk.END, values=(
                user.id_usuario, user.nombre, user.email, 
                user.telefono, user.fecha_registro.strftime("%d/%m/%Y"), 
                user.prestamos_activos
            ))
    
    # ==================== MÉTODOS DE GESTIÓN DE PRÉSTAMOS ====================
    
    def make_loan(self):
        """Realiza un préstamo de libro."""
        try:
            isbn = self.loan_isbn_entry.get().strip()
            user_id = self.loan_user_entry.get().strip()
            
            if not all([isbn, user_id]):
                messagebox.showerror("Error", "Todos los campos son obligatorios")
                return
            
            loan_id = self.biblioteca.realizar_prestamo(isbn, user_id)
            if loan_id:
                messagebox.showinfo("Éxito", f"Préstamo realizado con ID: {loan_id}")
                self.clear_loan_entries()
                self.populate_loans_table()
                self.populate_books_table()
                self.populate_users_table()
                self.update_statistics()
            else:
                messagebox.showerror("Error", "No se pudo realizar el préstamo. Verifique que el libro esté disponible y el usuario exista.")
                
        except Exception as e:
            messagebox.showerror("Error", f"Error inesperado: {str(e)}")
    
    def return_book(self):
        """Procesa la devolución de un libro."""
        try:
            loan_id = self.return_loan_entry.get().strip()
            
            if not loan_id:
                messagebox.showerror("Error", "Ingrese el ID del préstamo")
                return
            
            if self.biblioteca.devolver_libro(loan_id):
                messagebox.showinfo("Éxito", f"Libro devuelto correctamente (Préstamo: {loan_id})")
                self.return_loan_entry.delete(0, tk.END)
                self.populate_loans_table()
                self.populate_books_table()
                self.populate_users_table()
                self.update_statistics()
            else:
                messagebox.showerror("Error", "No se encontró el préstamo especificado")
                
        except Exception as e:
            messagebox.showerror("Error", f"Error inesperado: {str(e)}")
    
    def clear_loan_entries(self):
        """Limpia los campos de entrada de préstamos."""
        self.loan_isbn_entry.delete(0, tk.END)
        self.loan_user_entry.delete(0, tk.END)
    
    def populate_loans_table(self):
        """Pobla la tabla de préstamos activos."""
        # Limpiar tabla
        for item in self.loans_tree.get_children():
            self.loans_tree.delete(item)
        
        # Obtener préstamos activos
        loans = self.biblioteca.obtener_prestamos_activos()
        
        # Poblar tabla
        for loan in loans:
            # Verificar si está vencido
            loan.esta_vencido()  # Actualiza el estado si es necesario
            
            self.loans_tree.insert("", tk.END, values=(
                loan.id_prestamo, loan.isbn_libro, loan.id_usuario,
                loan.fecha_prestamo.strftime("%d/%m/%Y %H:%M"),
                loan.fecha_vencimiento.strftime("%d/%m/%Y"),
                loan.dias_restantes(), loan.estado
            ))
    
    def populate_history_table(self):
        """Pobla la tabla de historial de préstamos."""
        # Limpiar tabla
        for item in self.history_tree.get_children():
            self.history_tree.delete(item)
        
        # Obtener historial
        history = self.biblioteca.obtener_historial_prestamos(20)  # Últimos 20 préstamos
        
        # Poblar tabla
        for loan in history:
            # Obtener información del libro para mostrar el título
            book = self.biblioteca.obtener_libro_por_isbn(loan.isbn_libro)
            book_title = book.titulo if book else "Libro no encontrado"
            
            self.history_tree.insert("", tk.END, values=(
                loan.id_prestamo, loan.isbn_libro, book_title,
                loan.id_usuario, loan.fecha_prestamo.strftime("%d/%m/%Y %H:%M"),
                loan.estado
            ))
    
    # ==================== MÉTODOS DE ESTADÍSTICAS ====================
    
    def update_statistics(self):
        """Actualiza las estadísticas mostradas en el panel."""
        stats = self.biblioteca.obtener_estadisticas()
        
        self.stats_vars['total_libros'].set(str(stats['total_libros']))
        self.stats_vars['libros_disponibles'].set(str(stats['libros_disponibles']))
        self.stats_vars['libros_prestados'].set(str(stats['libros_prestados']))
        self.stats_vars['total_usuarios'].set(str(stats['total_usuarios']))
        self.stats_vars['prestamos_activos'].set(str(stats['prestamos_activos']))
        self.stats_vars['solicitudes_pendientes'].set(str(stats['solicitudes_pendientes']))

def main():
    """Función principal para ejecutar la aplicación."""
    root = tk.Tk()
    app = BibliotecaGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()