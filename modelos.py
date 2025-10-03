"""
Modelos de datos para el Sistema de Gestión de Biblioteca
========================================================

Este módulo contiene las clases principales que representan las entidades
del sistema de gestión de biblioteca:
- Libro: Representa un libro con sus atributos
- Usuario: Representa un usuario de la biblioteca
- Prestamo: Representa un préstamo de libro
- BibliotecaManager: Administra todas las operaciones del sistema

Autor: [Tu nombre]
Fecha: 2024
Curso: Estructuras de Datos - Unidad 1
"""

from datetime import datetime, timedelta
from estructuras_datos import ListaEnlazada, Pila, Cola, ArregloDinamico

class Libro:
    """
    Clase que representa un libro en el sistema de biblioteca.
    
    Atributos:
        isbn: Código ISBN único del libro
        titulo: Título del libro
        autor: Autor del libro
        categoria: Categoría o género del libro
        año_publicacion: Año de publicación
        disponible: Estado de disponibilidad (True/False)
        fecha_registro: Fecha cuando se registró en el sistema
    """
    
    def __init__(self, isbn, titulo, autor, categoria, año_publicacion):
        self.isbn = isbn
        self.titulo = titulo
        self.autor = autor
        self.categoria = categoria
        self.año_publicacion = año_publicacion
        self.disponible = True
        self.fecha_registro = datetime.now()
    
    def __str__(self):
        """Representación en cadena del libro."""
        estado = "Disponible" if self.disponible else "Prestado"
        return f"ISBN: {self.isbn} | {self.titulo} por {self.autor} ({self.año_publicacion}) - {estado}"
    
    def __repr__(self):
        """Representación detallada del libro."""
        return (f"Libro(isbn='{self.isbn}', titulo='{self.titulo}', "
                f"autor='{self.autor}', categoria='{self.categoria}', "
                f"año={self.año_publicacion}, disponible={self.disponible})")
    
    def obtener_info_completa(self):
        """Retorna información completa del libro como diccionario."""
        return {
            'isbn': self.isbn,
            'titulo': self.titulo,
            'autor': self.autor,
            'categoria': self.categoria,
            'año_publicacion': self.año_publicacion,
            'disponible': self.disponible,
            'fecha_registro': self.fecha_registro.strftime("%d/%m/%Y %H:%M")
        }

class Usuario:
    """
    Clase que representa un usuario de la biblioteca.
    
    Atributos:
        id_usuario: Identificador único del usuario
        nombre: Nombre completo del usuario
        email: Correo electrónico del usuario
        telefono: Número de teléfono
        fecha_registro: Fecha de registro en el sistema
        prestamos_activos: Número de préstamos activos
        historial_prestamos: Lista de préstamos realizados
    """
    
    def __init__(self, id_usuario, nombre, email, telefono):
        self.id_usuario = id_usuario
        self.nombre = nombre
        self.email = email
        self.telefono = telefono
        self.fecha_registro = datetime.now()
        self.prestamos_activos = 0
        self.historial_prestamos = []
    
    def __str__(self):
        """Representación en cadena del usuario."""
        return f"ID: {self.id_usuario} | {self.nombre} | {self.email} | Préstamos activos: {self.prestamos_activos}"
    
    def __repr__(self):
        """Representación detallada del usuario."""
        return (f"Usuario(id='{self.id_usuario}', nombre='{self.nombre}', "
                f"email='{self.email}', prestamos_activos={self.prestamos_activos})")
    
    def obtener_info_completa(self):
        """Retorna información completa del usuario como diccionario."""
        return {
            'id_usuario': self.id_usuario,
            'nombre': self.nombre,
            'email': self.email,
            'telefono': self.telefono,
            'fecha_registro': self.fecha_registro.strftime("%d/%m/%Y %H:%M"),
            'prestamos_activos': self.prestamos_activos,
            'total_prestamos': len(self.historial_prestamos)
        }

class Prestamo:
    """
    Clase que representa un préstamo de libro.
    
    Atributos:
        id_prestamo: Identificador único del préstamo
        isbn_libro: ISBN del libro prestado
        id_usuario: ID del usuario que realiza el préstamo
        fecha_prestamo: Fecha del préstamo
        fecha_vencimiento: Fecha límite de devolución
        fecha_devolucion: Fecha real de devolución (None si está activo)
        estado: Estado del préstamo (activo, devuelto, vencido)
    """
    
    def __init__(self, id_prestamo, isbn_libro, id_usuario, dias_prestamo=14):
        self.id_prestamo = id_prestamo
        self.isbn_libro = isbn_libro
        self.id_usuario = id_usuario
        self.fecha_prestamo = datetime.now()
        self.fecha_vencimiento = self.fecha_prestamo + timedelta(days=dias_prestamo)
        self.fecha_devolucion = None
        self.estado = "activo"
    
    def devolver(self):
        """Marca el préstamo como devuelto."""
        self.fecha_devolucion = datetime.now()
        self.estado = "devuelto"
    
    def esta_vencido(self):
        """Verifica si el préstamo está vencido."""
        if self.estado == "activo" and datetime.now() > self.fecha_vencimiento:
            self.estado = "vencido"
            return True
        return self.estado == "vencido"
    
    def dias_restantes(self):
        """Calcula los días restantes para la devolución."""
        if self.estado != "activo":
            return 0
        dias = (self.fecha_vencimiento - datetime.now()).days
        return max(0, dias)
    
    def __str__(self):
        """Representación en cadena del préstamo."""
        return (f"Préstamo #{self.id_prestamo} | Libro: {self.isbn_libro} | "
                f"Usuario: {self.id_usuario} | Estado: {self.estado}")
    
    def obtener_info_completa(self):
        """Retorna información completa del préstamo como diccionario."""
        return {
            'id_prestamo': self.id_prestamo,
            'isbn_libro': self.isbn_libro,
            'id_usuario': self.id_usuario,
            'fecha_prestamo': self.fecha_prestamo.strftime("%d/%m/%Y %H:%M"),
            'fecha_vencimiento': self.fecha_vencimiento.strftime("%d/%m/%Y"),
            'fecha_devolucion': self.fecha_devolucion.strftime("%d/%m/%Y %H:%M") if self.fecha_devolucion else "Pendiente",
            'estado': self.estado,
            'dias_restantes': self.dias_restantes()
        }

class BibliotecaManager:
    """
    Clase principal que gestiona todas las operaciones del sistema de biblioteca.
    
    Utiliza diferentes estructuras de datos lineales:
    - ListaEnlazada: Para almacenar libros (inserción/eliminación frecuente)
    - ArregloDinamico: Para almacenar usuarios (acceso indexado rápido)
    - Pila: Para historial de préstamos recientes
    - Cola: Para solicitudes de préstamos pendientes
    """
    
    def __init__(self):
        # Estructuras de datos principales
        self.libros = ListaEnlazada()          # Lista enlazada para libros
        self.usuarios = ArregloDinamico()      # Arreglo dinámico para usuarios
        self.historial_prestamos = Pila()     # Pila para historial reciente
        self.cola_solicitudes = Cola()        # Cola para solicitudes pendientes
        
        # Contadores para IDs únicos
        self.siguiente_id_usuario = 1
        self.siguiente_id_prestamo = 1
        
        # Préstamos activos (diccionario para búsqueda rápida)
        self.prestamos_activos = {}
        
        # Inicializar con datos de ejemplo
        self._inicializar_datos_ejemplo()
    
    def _inicializar_datos_ejemplo(self):
        """Inicializa el sistema con algunos datos de ejemplo para demostración."""
        # Libros de ejemplo
        libros_ejemplo = [
            ("978-84-376-0494-7", "Cien años de soledad", "Gabriel García Márquez", "Realismo Mágico", 1967),
            ("978-84-663-0016-6", "Don Quijote de la Mancha", "Miguel de Cervantes", "Clásico", 1605),
            ("978-84-376-0485-5", "1984", "George Orwell", "Distopía", 1949),
            ("978-84-206-6764-4", "El principito", "Antoine de Saint-Exupéry", "Filosofía", 1943),
            ("978-84-663-2946-4", "Crónica de una muerte anunciada", "Gabriel García Márquez", "Realismo Mágico", 1981)
        ]
        
        for isbn, titulo, autor, categoria, año in libros_ejemplo:
            libro = Libro(isbn, titulo, autor, categoria, año)
            self.libros.insertar_al_final(libro)
        
        # Usuarios de ejemplo
        usuarios_ejemplo = [
            ("Juan Pérez", "juan.perez@email.com", "123-456-7890"),
            ("María García", "maria.garcia@email.com", "098-765-4321"),
            ("Carlos López", "carlos.lopez@email.com", "555-123-4567")
        ]
        
        for nombre, email, telefono in usuarios_ejemplo:
            usuario = Usuario(f"U{self.siguiente_id_usuario:03d}", nombre, email, telefono)
            self.usuarios.agregar(usuario)
            self.siguiente_id_usuario += 1
    
    # ==================== GESTIÓN DE LIBROS ====================
    
    def registrar_libro(self, isbn, titulo, autor, categoria, año_publicacion):
        """
        Registra un nuevo libro en el sistema.
        
        Args:
            isbn: Código ISBN del libro
            titulo: Título del libro
            autor: Autor del libro
            categoria: Categoría del libro
            año_publicacion: Año de publicación
            
        Returns:
            True si se registró correctamente, False si ya existe
        """
        # Verificar si el libro ya existe
        libros_existentes = self.libros.buscar(lambda l: l.isbn == isbn)
        if libros_existentes:
            return False
        
        # Crear y registrar el nuevo libro
        nuevo_libro = Libro(isbn, titulo, autor, categoria, año_publicacion)
        self.libros.insertar_al_final(nuevo_libro)
        return True
    
    def buscar_libros(self, criterio="", valor=""):
        """
        Busca libros por diferentes criterios.
        
        Args:
            criterio: Tipo de búsqueda (titulo, autor, categoria, isbn)
            valor: Valor a buscar
            
        Returns:
            Lista de libros que coinciden con el criterio
        """
        if not criterio or not valor:
            return self.libros.obtener_todos()
        
        valor_lower = valor.lower()
        
        def buscar_por_criterio(libro):
            if criterio == "titulo":
                return valor_lower in libro.titulo.lower()
            elif criterio == "autor":
                return valor_lower in libro.autor.lower()
            elif criterio == "categoria":
                return valor_lower in libro.categoria.lower()
            elif criterio == "isbn":
                return valor_lower in libro.isbn.lower()
            return False
        
        return self.libros.buscar(buscar_por_criterio)
    
    def obtener_libro_por_isbn(self, isbn):
        """Obtiene un libro específico por su ISBN."""
        libros_encontrados = self.libros.buscar(lambda l: l.isbn == isbn)
        return libros_encontrados[0] if libros_encontrados else None
    
    def obtener_todos_los_libros(self):
        """Retorna todos los libros registrados."""
        return self.libros.obtener_todos()
    
    def eliminar_libro(self, isbn):
        """
        Elimina un libro del sistema.
        
        Args:
            isbn: ISBN del libro a eliminar
            
        Returns:
            True si se eliminó correctamente, False si no se encontró
        """
        return self.libros.eliminar(lambda l: l.isbn == isbn)
    
    # ==================== GESTIÓN DE USUARIOS ====================
    
    def registrar_usuario(self, nombre, email, telefono):
        """
        Registra un nuevo usuario en el sistema.
        
        Args:
            nombre: Nombre completo del usuario
            email: Correo electrónico
            telefono: Número de teléfono
            
        Returns:
            ID del usuario creado o None si el email ya existe
        """
        # Verificar si el usuario ya existe por email
        usuarios_existentes = self.usuarios.buscar(lambda u: u.email == email)
        if usuarios_existentes:
            return None
        
        # Crear nuevo usuario
        id_usuario = f"U{self.siguiente_id_usuario:03d}"
        nuevo_usuario = Usuario(id_usuario, nombre, email, telefono)
        self.usuarios.agregar(nuevo_usuario)
        self.siguiente_id_usuario += 1
        
        return id_usuario
    
    def buscar_usuarios(self, criterio="", valor=""):
        """
        Busca usuarios por diferentes criterios.
        
        Args:
            criterio: Tipo de búsqueda (nombre, email, id)
            valor: Valor a buscar
            
        Returns:
            Lista de usuarios que coinciden con el criterio
        """
        if not criterio or not valor:
            return self.usuarios.obtener_todos()
        
        valor_lower = valor.lower()
        
        def buscar_por_criterio(usuario):
            if criterio == "nombre":
                return valor_lower in usuario.nombre.lower()
            elif criterio == "email":
                return valor_lower in usuario.email.lower()
            elif criterio == "id":
                return valor_lower in usuario.id_usuario.lower()
            return False
        
        return self.usuarios.buscar(buscar_por_criterio)
    
    def obtener_usuario_por_id(self, id_usuario):
        """Obtiene un usuario específico por su ID."""
        usuarios_encontrados = self.usuarios.buscar(lambda u: u.id_usuario == id_usuario)
        return usuarios_encontrados[0] if usuarios_encontrados else None
    
    def obtener_todos_los_usuarios(self):
        """Retorna todos los usuarios registrados."""
        return self.usuarios.obtener_todos()
    
    # ==================== GESTIÓN DE PRÉSTAMOS ====================
    
    def realizar_prestamo(self, isbn_libro, id_usuario):
        """
        Realiza un préstamo de libro a un usuario.
        
        Args:
            isbn_libro: ISBN del libro a prestar
            id_usuario: ID del usuario
            
        Returns:
            ID del préstamo creado o None si no es posible
        """
        # Verificar que el libro existe y está disponible
        libro = self.obtener_libro_por_isbn(isbn_libro)
        if not libro or not libro.disponible:
            return None
        
        # Verificar que el usuario existe
        usuario = self.obtener_usuario_por_id(id_usuario)
        if not usuario:
            return None
        
        # Crear el préstamo
        id_prestamo = f"P{self.siguiente_id_prestamo:03d}"
        prestamo = Prestamo(id_prestamo, isbn_libro, id_usuario)
        
        # Actualizar estados
        libro.disponible = False
        usuario.prestamos_activos += 1
        usuario.historial_prestamos.append(prestamo)
        
        # Almacenar en estructuras de datos
        self.prestamos_activos[id_prestamo] = prestamo
        self.historial_prestamos.apilar(prestamo)
        
        self.siguiente_id_prestamo += 1
        return id_prestamo
    
    def devolver_libro(self, id_prestamo):
        """
        Procesa la devolución de un libro.
        
        Args:
            id_prestamo: ID del préstamo a devolver
            
        Returns:
            True si se procesó correctamente, False si no se encontró
        """
        if id_prestamo not in self.prestamos_activos:
            return False
        
        prestamo = self.prestamos_activos[id_prestamo]
        
        # Actualizar estados
        prestamo.devolver()
        libro = self.obtener_libro_por_isbn(prestamo.isbn_libro)
        usuario = self.obtener_usuario_por_id(prestamo.id_usuario)
        
        if libro:
            libro.disponible = True
        if usuario:
            usuario.prestamos_activos -= 1
        
        # Remover de préstamos activos
        del self.prestamos_activos[id_prestamo]
        
        return True
    
    def obtener_prestamos_activos(self):
        """Retorna lista de todos los préstamos activos."""
        return list(self.prestamos_activos.values())
    
    def obtener_historial_prestamos(self, limite=10):
        """
        Obtiene el historial reciente de préstamos.
        
        Args:
            limite: Número máximo de préstamos a retornar
            
        Returns:
            Lista de préstamos recientes
        """
        historial = self.historial_prestamos.obtener_todos()
        return historial[:limite]
    
    def obtener_prestamos_usuario(self, id_usuario):
        """Obtiene los préstamos activos de un usuario específico."""
        return [p for p in self.prestamos_activos.values() if p.id_usuario == id_usuario]
    
    # ==================== GESTIÓN DE SOLICITUDES ====================
    
    def agregar_solicitud_prestamo(self, isbn_libro, id_usuario):
        """Agrega una solicitud de préstamo a la cola."""
        solicitud = {
            'isbn_libro': isbn_libro,
            'id_usuario': id_usuario,
            'fecha_solicitud': datetime.now()
        }
        self.cola_solicitudes.encolar(solicitud)
    
    def procesar_siguiente_solicitud(self):
        """Procesa la siguiente solicitud en la cola."""
        if self.cola_solicitudes.esta_vacia():
            return None
        
        solicitud = self.cola_solicitudes.desencolar()
        
        # Intentar realizar el préstamo
        id_prestamo = self.realizar_prestamo(solicitud['isbn_libro'], solicitud['id_usuario'])
        
        return {
            'solicitud': solicitud,
            'prestamo_id': id_prestamo,
            'exitoso': id_prestamo is not None
        }
    
    def obtener_solicitudes_pendientes(self):
        """Retorna todas las solicitudes pendientes."""
        return self.cola_solicitudes.obtener_todos()
    
    # ==================== ESTADÍSTICAS Y REPORTES ====================
    
    def obtener_estadisticas(self):
        """Genera estadísticas del sistema."""
        total_libros = self.libros.obtener_tamaño()
        libros_disponibles = len([l for l in self.libros.obtener_todos() if l.disponible])
        total_usuarios = self.usuarios.obtener_tamaño()
        prestamos_activos = len(self.prestamos_activos)
        solicitudes_pendientes = self.cola_solicitudes.obtener_tamaño()
        
        return {
            'total_libros': total_libros,
            'libros_disponibles': libros_disponibles,
            'libros_prestados': total_libros - libros_disponibles,
            'total_usuarios': total_usuarios,
            'prestamos_activos': prestamos_activos,
            'solicitudes_pendientes': solicitudes_pendientes
        }