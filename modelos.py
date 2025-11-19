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
from estructuras_arboles import ArbolAVL, MinHeap, Trie, ArbolCategorias

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
    
    Utiliza estructuras de datos híbridas para optimizar rendimiento:
    - Estructuras Lineales: Lista, Pila, Cola, Arreglo (compatibilidad legacy)
    - Estructuras de Árboles: AVL, Heap, Trie, Árbol N-ario (rendimiento optimizado)
    
    Índices de Árboles:
    - AVL por ISBN: Búsqueda O(log n) de libros
    - AVL por título: Búsqueda O(log n) alfabética
    - AVL por ID usuario: Búsqueda O(log n) de usuarios
    - Heap por vencimiento: Acceso O(1) al préstamo más urgente
    - Trie para autocompletado: Sugerencias O(m) eficientes
    - Árbol N-ario de categorías: Jerarquía organizada
    """
    
    def __init__(self):
        # ===== ESTRUCTURAS LINEALES (LEGACY) =====
        self.libros = ListaEnlazada()          # Lista enlazada para libros
        self.usuarios = ArregloDinamico()      # Arreglo dinámico para usuarios
        self.historial_prestamos = Pila()     # Pila para historial reciente
        self.cola_solicitudes = Cola()        # Cola para solicitudes pendientes
        
        # ===== ÍNDICES DE ÁRBOLES (OPTIMIZACIÓN) =====
        # Índices para libros
        self.arbol_libros_isbn = ArbolAVL(lambda libro: libro.isbn)  # Búsqueda por ISBN
        self.arbol_libros_titulo = ArbolAVL(lambda libro: libro.titulo.lower())  # Búsqueda por título
        self.trie_titulos = Trie(case_sensitive=False)  # Autocompletado de títulos
        
        # Índices para usuarios
        self.arbol_usuarios_id = ArbolAVL(lambda usuario: usuario.id_usuario)  # Búsqueda por ID
        self.arbol_usuarios_email = ArbolAVL(lambda usuario: usuario.email.lower())  # Búsqueda por email
        
        # Gestión de préstamos con Heap
        self.heap_prestamos_vencimiento = MinHeap(
            funcion_comparacion=lambda p1, p2: p1.fecha_vencimiento < p2.fecha_vencimiento
        )
        
        # Árbol jerárquico de categorías
        self.arbol_categorias = ArbolCategorias("Biblioteca")
        
        # Contadores para IDs únicos
        self.siguiente_id_usuario = 1
        self.siguiente_id_prestamo = 1
        
        # Préstamos activos (diccionario para búsqueda rápida)
        self.prestamos_activos = {}
        
        # Inicializar con datos de ejemplo
        self._inicializar_datos_ejemplo()
    
    def _inicializar_datos_ejemplo(self):
        """Inicializa el sistema con algunos datos de ejemplo para demostración."""
        # Inicializar categorías en el árbol PRIMERO
        categorias = ["Realismo Mágico", "Clásico", "Distopía", "Filosofía"]
        for categoria in categorias:
            self.arbol_categorias.agregar_categoria(categoria, "Biblioteca")
        
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
            # Insertar en estructura lineal
            self.libros.insertar_al_final(libro)
            # Insertar en índices de árboles
            self.arbol_libros_isbn.insertar(libro)
            self.arbol_libros_titulo.insertar(libro)
            self.trie_titulos.insertar(titulo, libro)
            # Agregar a categoría en árbol jerárquico
            self.arbol_categorias.agregar_dato_a_categoria(categoria, libro)
        
        # Usuarios de ejemplo
        usuarios_ejemplo = [
            ("Juan Pérez", "juan.perez@email.com", "123-456-7890"),
            ("María García", "maria.garcia@email.com", "098-765-4321"),
            ("Carlos López", "carlos.lopez@email.com", "555-123-4567")
        ]
        
        for nombre, email, telefono in usuarios_ejemplo:
            usuario = Usuario(f"U{self.siguiente_id_usuario:03d}", nombre, email, telefono)
            # Insertar en estructura lineal
            self.usuarios.agregar(usuario)
            # Insertar en índices de árboles
            self.arbol_usuarios_id.insertar(usuario)
            self.arbol_usuarios_email.insertar(usuario)
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
        # Verificar si el libro ya existe (usando árbol AVL para búsqueda rápida)
        libro_existente = self.arbol_libros_isbn.buscar(isbn)
        if libro_existente:
            return False
        
        # Crear y registrar el nuevo libro
        nuevo_libro = Libro(isbn, titulo, autor, categoria, año_publicacion)
        
        # Insertar en estructura lineal (legacy)
        self.libros.insertar_al_final(nuevo_libro)
        
        # Insertar en índices de árboles (optimización)
        self.arbol_libros_isbn.insertar(nuevo_libro)
        self.arbol_libros_titulo.insertar(nuevo_libro)
        self.trie_titulos.insertar(titulo, nuevo_libro)
        
        # Agregar a categoría en árbol jerárquico
        if not self.arbol_categorias.buscar_categoria(categoria):
            self.arbol_categorias.agregar_categoria(categoria, "Biblioteca")
        self.arbol_categorias.agregar_dato_a_categoria(categoria, nuevo_libro)
        
        return True
    
    def buscar_libros(self, criterio="", valor=""):
        """
        Busca libros por diferentes criterios usando índices optimizados.
        
        Args:
            criterio: Tipo de búsqueda (titulo, autor, categoria, isbn)
            valor: Valor a buscar
            
        Returns:
            Lista de libros que coinciden con el criterio
        """
        if not criterio or not valor:
            return self.libros.obtener_todos()
        
        valor_lower = valor.lower()
        
        # Usar índices de árboles para búsquedas optimizadas
        if criterio == "isbn":
            # Búsqueda exacta por ISBN usando AVL - O(log n)
            libro = self.arbol_libros_isbn.buscar(valor)
            return [libro] if libro else []
        
        elif criterio == "titulo":
            # Búsqueda por título usando AVL - O(log n) para coincidencias exactas
            libro = self.arbol_libros_titulo.buscar(valor_lower)
            if libro:
                return [libro]
            # Si no hay coincidencia exacta, buscar en lista (contiene)
            return self.libros.buscar(lambda l: valor_lower in l.titulo.lower())
        
        elif criterio == "autor":
            # Búsqueda lineal por autor (no hay índice específico)
            return self.libros.buscar(lambda l: valor_lower in l.autor.lower())
        
        elif criterio == "categoria":
            # Búsqueda en árbol de categorías - O(k) donde k es tamaño de categoría
            return self.arbol_categorias.obtener_datos_categoria(valor) or []
        
        # Búsqueda general (fallback)
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
        """Obtiene un libro específico por su ISBN usando índice AVL - O(log n)."""
        return self.arbol_libros_isbn.buscar(isbn)
    
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
        # Verificar si el usuario ya existe por email (usando árbol AVL - O(log n))
        usuario_existente = self.arbol_usuarios_email.buscar(email.lower())
        if usuario_existente:
            return None
        
        # Crear nuevo usuario
        id_usuario = f"U{self.siguiente_id_usuario:03d}"
        nuevo_usuario = Usuario(id_usuario, nombre, email, telefono)
        
        # Insertar en estructura lineal (legacy)
        self.usuarios.agregar(nuevo_usuario)
        
        # Insertar en índices de árboles (optimización)
        self.arbol_usuarios_id.insertar(nuevo_usuario)
        self.arbol_usuarios_email.insertar(nuevo_usuario)
        
        self.siguiente_id_usuario += 1
        return id_usuario
    
    def buscar_usuarios(self, criterio="", valor=""):
        """
        Busca usuarios por diferentes criterios usando índices optimizados.
        
        Args:
            criterio: Tipo de búsqueda (nombre, email, id)
            valor: Valor a buscar
            
        Returns:
            Lista de usuarios que coinciden con el criterio
        """
        if not criterio or not valor:
            return self.usuarios.obtener_todos()
        
        valor_lower = valor.lower()
        
        # Usar índices de árboles para búsquedas optimizadas
        if criterio == "id":
            # Búsqueda exacta por ID usando AVL - O(log n)
            usuario = self.arbol_usuarios_id.buscar(valor)
            return [usuario] if usuario else []
        
        elif criterio == "email":
            # Búsqueda exacta por email usando AVL - O(log n)
            usuario = self.arbol_usuarios_email.buscar(valor_lower)
            return [usuario] if usuario else []
        
        elif criterio == "nombre":
            # Búsqueda lineal por nombre (no hay índice específico)
            return self.usuarios.buscar(lambda u: valor_lower in u.nombre.lower())
        
        # Búsqueda general (fallback)
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
        """Obtiene un usuario específico por su ID usando índice AVL - O(log n)."""
        return self.arbol_usuarios_id.buscar(id_usuario)
    
    def obtener_prestamos_activos(self):
        """Retorna la lista de préstamos activos."""
        return list(self.prestamos_activos.values())
    
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
        # Verificar que el libro existe y está disponible (usando árbol AVL - O(log n))
        libro = self.obtener_libro_por_isbn(isbn_libro)
        if not libro or not libro.disponible:
            return None
        
        # Verificar que el usuario existe (usando árbol AVL - O(log n))
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
        
        # Insertar en heap para gestión por vencimiento
        self.heap_prestamos_vencimiento.insertar(prestamo)
        
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
        
        # Nota: El heap mantiene el préstamo devuelto, pero en una implementación
        # completa se debería remover del heap también
        
        return True
    
    def autocompletar_titulos(self, prefijo, limite=10):
        """
        Proporciona sugerencias de autocompletado para títulos de libros.
        
        Args:
            prefijo: Prefijo a buscar
            limite: Número máximo de sugerencias
            
        Returns:
            Lista de tuplas (titulo, libro, frecuencia) ordenadas por frecuencia
        """
        return self.trie_titulos.autocompletar(prefijo, limite)
    
    def obtener_prestamo_mas_urgente(self):
        """
        Obtiene el préstamo más próximo a vencer usando Min-Heap.
        
        Returns:
            Préstamo más urgente o None si no hay préstamos activos
        """
        if self.heap_prestamos_vencimiento.obtener_tamaño() == 0:
            return None
        return self.heap_prestamos_vencimiento.obtener_minimo()
    
    def obtener_libros_por_categoria(self, categoria, incluir_subcategorias=True):
        """
        Obtiene libros de una categoría específica usando árbol N-ario.
        
        Args:
            categoria: Nombre de la categoría
            incluir_subcategorias: Si incluir libros de subcategorías
            
        Returns:
            Lista de libros en la categoría
        """
        return self.arbol_categorias.obtener_datos_categoria(
            categoria, incluir_subcategorias
        ) or []
    
    def obtener_categorias_disponibles(self):
        """
        Obtiene todas las categorías disponibles en el sistema.
        
        Returns:
            Lista de nombres de categorías
        """
        return self.arbol_categorias.obtener_subcategorias("Biblioteca") or []
    
    def buscar_libros_avanzada(self, filtros):
        """
        Búsqueda avanzada de libros usando múltiples criterios y índices.
        
        Args:
            filtros: Diccionario con criterios de búsqueda
                    {'titulo': str, 'autor': str, 'categoria': str, 'isbn': str}
        
        Returns:
            Lista de libros que cumplen todos los criterios
        """
        resultados = self.libros.obtener_todos()
        
        for criterio, valor in filtros.items():
            if not valor:
                continue
                
            valor_lower = valor.lower()
            
            if criterio == 'isbn':
                # Búsqueda exacta usando AVL
                libro = self.arbol_libros_isbn.buscar(valor)
                resultados = [libro] if libro else []
            elif criterio == 'titulo':
                # Búsqueda usando AVL o contiene
                libro = self.arbol_libros_titulo.buscar(valor_lower)
                if libro:
                    resultados = [r for r in resultados if r == libro]
                else:
                    resultados = [r for r in resultados if valor_lower in r.titulo.lower()]
            elif criterio == 'categoria':
                # Búsqueda usando árbol de categorías
                libros_categoria = self.obtener_libros_por_categoria(valor)
                resultados = [r for r in resultados if r in libros_categoria]
            elif criterio == 'autor':
                # Búsqueda lineal
                resultados = [r for r in resultados if valor_lower in r.autor.lower()]
        
        return resultados
    
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
        """Genera estadísticas completas del sistema incluyendo rendimiento de índices."""
        total_libros = self.libros.obtener_tamaño()
        libros_disponibles = len([l for l in self.libros.obtener_todos() if l.disponible])
        total_usuarios = self.usuarios.obtener_tamaño()
        prestamos_activos = len(self.prestamos_activos)
        solicitudes_pendientes = self.cola_solicitudes.obtener_tamaño()
        
        # Estadísticas de índices de árboles
        altura_arbol_isbn = self.arbol_libros_isbn.obtener_altura_arbol() if self.arbol_libros_isbn.raiz else 0
        altura_arbol_usuarios = self.arbol_usuarios_id.obtener_altura_arbol() if self.arbol_usuarios_id.raiz else 0
        tamaño_trie = self.trie_titulos.obtener_tamaño()
        tamaño_heap = self.heap_prestamos_vencimiento.obtener_tamaño()
        
        # Calcular mejoras de rendimiento estimadas
        mejora_busqueda_libros = total_libros // max(altura_arbol_isbn + 1, 1) if altura_arbol_isbn > 0 else 1
        mejora_busqueda_usuarios = total_usuarios // max(altura_arbol_usuarios + 1, 1) if altura_arbol_usuarios > 0 else 1
        
        return {
            # Estadísticas básicas
            'total_libros': total_libros,
            'libros_disponibles': libros_disponibles,
            'libros_prestados': total_libros - libros_disponibles,
            'total_usuarios': total_usuarios,
            'prestamos_activos': prestamos_activos,
            'solicitudes_pendientes': solicitudes_pendientes,
            
            # Estadísticas de índices de árboles
            'altura_arbol_libros_isbn': altura_arbol_isbn,
            'altura_arbol_usuarios_id': altura_arbol_usuarios,
            'tamaño_trie_titulos': tamaño_trie,
            'tamaño_heap_prestamos': tamaño_heap,
            'categorias_disponibles': len(self.obtener_categorias_disponibles()),
            
            # Métricas de rendimiento
            'mejora_busqueda_libros_x': mejora_busqueda_libros,
            'mejora_busqueda_usuarios_x': mejora_busqueda_usuarios,
            'indices_optimizados': True
        }
    
    def obtener_prestamos_activos(self):
        """Obtiene todos los préstamos activos."""
        return list(self.prestamos_activos.values())
    
    def obtener_todos_los_usuarios(self):
        """Obtiene todos los usuarios registrados."""
        return self.usuarios.obtener_todos()
    
    def obtener_todos_los_libros(self):
        """Obtiene todos los libros registrados."""
        return self.libros.obtener_todos()
    
    def obtener_historial_prestamos(self, limite=None):
        """Obtiene el historial de préstamos realizados."""
        historial = self.historial_prestamos.obtener_todos()
        if limite:
            return historial[-limite:]  # Los más recientes
        return historial