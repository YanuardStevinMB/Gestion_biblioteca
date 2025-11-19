"""
Sistema de Pruebas para Estructuras de Árboles
==============================================

Este módulo contiene las pruebas unitarias y de integración
para validar el funcionamiento correcto de las estructuras de
árboles implementadas en la Unidad 2.

Autor: Equipo de Desarrollo Biblioteca Virtual
Fecha: 2025
Curso: Estructuras de Datos - Unidad 2
"""

import unittest
from estructuras_arboles import ArbolAVL, MinHeap, Trie, ArbolCategorias
from modelos import Libro, Usuario, Prestamo
from datetime import datetime, timedelta


class TestArbolAVL(unittest.TestCase):
    """
    Conjunto de pruebas para validar el Árbol AVL.
    """
    
    def setUp(self):
        """Configuración inicial para cada prueba."""
        self.arbol = ArbolAVL()
    
    def test_avl_insercion_y_busqueda(self):
        """Prueba la inserción y búsqueda básica en el AVL."""
        print("\n=== PRUEBA AVL: Inserción y Búsqueda ===")
        
        # Insertar elementos
        self.assertTrue(self.arbol.insertar("Manzana", "manzana"))
        self.assertTrue(self.arbol.insertar("Banana", "banana"))
        self.assertTrue(self.arbol.insertar("Cereza", "cereza"))
        
        # Verificar tamaño
        self.assertEqual(self.arbol.obtener_tamaño(), 3)
        
        # Buscar elementos
        self.assertEqual(self.arbol.buscar("manzana"), "Manzana")
        self.assertEqual(self.arbol.buscar("banana"), "Banana")
        self.assertEqual(self.arbol.buscar("cereza"), "Cereza")
        self.assertIsNone(self.arbol.buscar("durazno"))
        
        print("✓ Inserción y búsqueda funcionan correctamente")
    
    def test_avl_no_permite_duplicados(self):
        """Verifica que el AVL no permite claves duplicadas."""
        print("\n=== PRUEBA AVL: No Permite Duplicados ===")
        
        self.assertTrue(self.arbol.insertar("Dato1", "clave1"))
        self.assertFalse(self.arbol.insertar("Dato2", "clave1"))  # Duplicado
        
        self.assertEqual(self.arbol.obtener_tamaño(), 1)
        print("✓ Duplicados rechazados correctamente")
    
    def test_avl_rotacion_simple_derecha(self):
        """Prueba la rotación simple derecha (caso LL)."""
        print("\n=== PRUEBA AVL: Rotación Simple Derecha (LL) ===")
        
        # Insertar en orden descendente para forzar rotación derecha
        self.arbol.insertar("C", "c")
        self.arbol.insertar("B", "b")
        self.arbol.insertar("A", "a")  # Esto debería causar rotación
        
        # Verificar que el árbol está balanceado
        self.assertTrue(self.arbol.verificar_balance())
        
        # Verificar el orden
        elementos = self.arbol.recorrido_inorden()
        self.assertEqual(elementos, ["A", "B", "C"])
        
        print("✓ Rotación simple derecha ejecutada correctamente")
    
    def test_avl_rotacion_simple_izquierda(self):
        """Prueba la rotación simple izquierda (caso RR)."""
        print("\n=== PRUEBA AVL: Rotación Simple Izquierda (RR) ===")
        
        # Insertar en orden ascendente para forzar rotación izquierda
        self.arbol.insertar("A", "a")
        self.arbol.insertar("B", "b")
        self.arbol.insertar("C", "c")  # Esto debería causar rotación
        
        # Verificar que el árbol está balanceado
        self.assertTrue(self.arbol.verificar_balance())
        
        # Verificar el orden
        elementos = self.arbol.recorrido_inorden()
        self.assertEqual(elementos, ["A", "B", "C"])
        
        print("✓ Rotación simple izquierda ejecutada correctamente")
    
    def test_avl_rotacion_doble_lr(self):
        """Prueba la rotación doble izquierda-derecha (caso LR)."""
        print("\n=== PRUEBA AVL: Rotación Doble LR ===")
        
        self.arbol.insertar("C", "c")
        self.arbol.insertar("A", "a")
        self.arbol.insertar("B", "b")  # Esto debería causar rotación doble
        
        self.assertTrue(self.arbol.verificar_balance())
        
        elementos = self.arbol.recorrido_inorden()
        self.assertEqual(elementos, ["A", "B", "C"])
        
        print("✓ Rotación doble LR ejecutada correctamente")
    
    def test_avl_rotacion_doble_rl(self):
        """Prueba la rotación doble derecha-izquierda (caso RL)."""
        print("\n=== PRUEBA AVL: Rotación Doble RL ===")
        
        self.arbol.insertar("A", "a")
        self.arbol.insertar("C", "c")
        self.arbol.insertar("B", "b")  # Esto debería causar rotación doble
        
        self.assertTrue(self.arbol.verificar_balance())
        
        elementos = self.arbol.recorrido_inorden()
        self.assertEqual(elementos, ["A", "B", "C"])
        
        print("✓ Rotación doble RL ejecutada correctamente")
    
    def test_avl_eliminacion(self):
        """Prueba la eliminación de elementos del AVL."""
        print("\n=== PRUEBA AVL: Eliminación ===")
        
        # Insertar elementos
        for i in range(1, 8):
            self.arbol.insertar(f"Dato{i}", i)
        
        self.assertEqual(self.arbol.obtener_tamaño(), 7)
        
        # Eliminar elementos
        self.assertTrue(self.arbol.eliminar(4))
        self.assertEqual(self.arbol.obtener_tamaño(), 6)
        self.assertIsNone(self.arbol.buscar(4))
        
        # Verificar que sigue balanceado después de eliminación
        self.assertTrue(self.arbol.verificar_balance())
        
        # Intentar eliminar elemento inexistente
        self.assertFalse(self.arbol.eliminar(100))
        
        print("✓ Eliminación funciona correctamente y mantiene balance")
    
    def test_avl_insercion_masiva(self):
        """Prueba inserción masiva y verifica balance."""
        print("\n=== PRUEBA AVL: Inserción Masiva ===")
        
        # Insertar 100 elementos
        for i in range(100):
            self.arbol.insertar(f"Dato{i}", i)
        
        self.assertEqual(self.arbol.obtener_tamaño(), 100)
        
        # Verificar que el árbol está balanceado
        self.assertTrue(self.arbol.verificar_balance())
        
        # Verificar altura (debe ser aproximadamente log2(100) ≈ 6.64)
        # La altura de un AVL con n nodos es máximo 1.44 * log2(n+2) - 1.328
        # Para n=100: h_max ≈ 9.2
        altura_esperada_max = 10  # Damos margen
        altura_real = self.arbol.obtener_altura(self.arbol.raiz)
        self.assertLessEqual(altura_real, altura_esperada_max)
        
        print(f"✓ Inserción masiva exitosa. Altura del árbol: {altura_real}")
    
    def test_avl_busqueda_prefijo(self):
        """Prueba la búsqueda por prefijo."""
        print("\n=== PRUEBA AVL: Búsqueda por Prefijo ===")
        
        # Insertar palabras con prefijos comunes
        palabras = ["manzana", "mandarina", "mango", "banana", "cereza"]
        for palabra in palabras:
            self.arbol.insertar(palabra, palabra)
        
        # Buscar por prefijo "man"
        resultados = self.arbol.buscar_por_prefijo("man")
        self.assertEqual(len(resultados), 3)  # manzana, mandarina, mango
        
        # Buscar por prefijo "b"
        resultados_b = self.arbol.buscar_por_prefijo("b")
        self.assertEqual(len(resultados_b), 1)  # banana
        
        print("✓ Búsqueda por prefijo funciona correctamente")
    
    def test_avl_con_libros(self):
        """Prueba el AVL con objetos Libro reales."""
        print("\n=== PRUEBA AVL: Con Objetos Libro ===")
        
        arbol_libros = ArbolAVL(funcion_clave=lambda libro: libro.isbn)
        
        # Crear libros
        libro1 = Libro("978-1", "Título A", "Autor A", "Ficción", 2020)
        libro2 = Libro("978-2", "Título B", "Autor B", "Ciencia", 2021)
        libro3 = Libro("978-3", "Título C", "Autor C", "Historia", 2022)
        
        # Insertar
        arbol_libros.insertar(libro1)
        arbol_libros.insertar(libro2)
        arbol_libros.insertar(libro3)
        
        # Buscar
        encontrado = arbol_libros.buscar("978-2")
        self.assertIsNotNone(encontrado)
        self.assertEqual(encontrado.titulo, "Título B")
        
        # Verificar balance
        self.assertTrue(arbol_libros.verificar_balance())
        
        print("✓ AVL funciona correctamente con objetos Libro")


class TestMinHeap(unittest.TestCase):
    """
    Conjunto de pruebas para validar el Min-Heap.
    """
    
    def setUp(self):
        """Configuración inicial para cada prueba."""
        self.heap = MinHeap()
    
    def test_heap_insercion_y_minimo(self):
        """Prueba la inserción y obtención del mínimo."""
        print("\n=== PRUEBA HEAP: Inserción y Mínimo ===")
        
        # Heap vacío
        self.assertTrue(self.heap.esta_vacio())
        self.assertIsNone(self.heap.obtener_minimo())
        
        # Insertar elementos
        self.heap.insertar(5)
        self.heap.insertar(3)
        self.heap.insertar(7)
        self.heap.insertar(1)
        
        # El mínimo debe ser 1
        self.assertEqual(self.heap.obtener_minimo(), 1)
        self.assertEqual(self.heap.obtener_tamaño(), 4)
        
        print("✓ Inserción y obtención del mínimo funcionan correctamente")
    
    def test_heap_extraccion_minimo(self):
        """Prueba la extracción del mínimo."""
        print("\n=== PRUEBA HEAP: Extracción del Mínimo ===")
        
        # Insertar elementos
        elementos = [10, 5, 3, 8, 2, 15, 1]
        for elem in elementos:
            self.heap.insertar(elem)
        
        # Extraer en orden (debe salir ordenado ascendente)
        orden_extraido = []
        while not self.heap.esta_vacio():
            orden_extraido.append(self.heap.extraer_minimo())
        
        self.assertEqual(orden_extraido, [1, 2, 3, 5, 8, 10, 15])
        
        print("✓ Extracción del mínimo mantiene el orden correcto")
    
    def test_heap_propiedad_heap(self):
        """Verifica que se mantiene la propiedad del heap."""
        print("\n=== PRUEBA HEAP: Propiedad del Heap ===")
        
        # Insertar 20 elementos aleatorios
        import random
        random.seed(42)
        for _ in range(20):
            self.heap.insertar(random.randint(1, 100))
        
        # Verificar que el mínimo es realmente el más pequeño
        todos_elementos = self.heap.obtener_todos()
        minimo_heap = self.heap.obtener_minimo()
        minimo_real = min(todos_elementos)
        
        self.assertEqual(minimo_heap, minimo_real)
        
        print("✓ Propiedad del heap se mantiene correctamente")
    
    def test_heap_con_prestamos(self):
        """Prueba el heap con objetos Préstamo reales."""
        print("\n=== PRUEBA HEAP: Con Objetos Préstamo ===")
        
        heap_prestamos = MinHeap(
            funcion_comparacion=lambda p1, p2: p1.fecha_vencimiento < p2.fecha_vencimiento
        )
        
        # Crear préstamos con diferentes fechas de vencimiento
        prestamo1 = Prestamo("P001", "978-1", "U001", dias_prestamo=14)
        prestamo2 = Prestamo("P002", "978-2", "U002", dias_prestamo=7)
        prestamo3 = Prestamo("P003", "978-3", "U003", dias_prestamo=21)
        
        heap_prestamos.insertar(prestamo1)
        heap_prestamos.insertar(prestamo2)
        heap_prestamos.insertar(prestamo3)
        
        # El préstamo más urgente debe ser el de 7 días
        mas_urgente = heap_prestamos.obtener_minimo()
        self.assertEqual(mas_urgente.id_prestamo, "P002")
        self.assertTrue(mas_urgente.dias_restantes() < prestamo1.dias_restantes())
        
        print("✓ Heap funciona correctamente con objetos Préstamo")
    
    def test_heap_insercion_y_extraccion_alternadas(self):
        """Prueba inserciones y extracciones alternadas."""
        print("\n=== PRUEBA HEAP: Operaciones Alternadas ===")
        
        self.heap.insertar(10)
        self.heap.insertar(5)
        self.assertEqual(self.heap.extraer_minimo(), 5)
        
        self.heap.insertar(3)
        self.heap.insertar(8)
        self.assertEqual(self.heap.extraer_minimo(), 3)
        
        self.heap.insertar(1)
        self.assertEqual(self.heap.extraer_minimo(), 1)
        self.assertEqual(self.heap.extraer_minimo(), 8)
        self.assertEqual(self.heap.extraer_minimo(), 10)
        
        self.assertTrue(self.heap.esta_vacio())
        
        print("✓ Operaciones alternadas funcionan correctamente")


class TestTrie(unittest.TestCase):
    """
    Conjunto de pruebas para validar el Trie.
    """
    
    def setUp(self):
        """Configuración inicial para cada prueba."""
        self.trie = Trie(case_sensitive=False)
    
    def test_trie_insercion_y_busqueda(self):
        """Prueba la inserción y búsqueda en el Trie."""
        print("\n=== PRUEBA TRIE: Inserción y Búsqueda ===")
        
        # Insertar palabras
        self.assertTrue(self.trie.insertar("manzana"))
        self.assertTrue(self.trie.insertar("mandarina"))
        self.assertTrue(self.trie.insertar("banana"))
        
        # No permite duplicados
        self.assertFalse(self.trie.insertar("manzana"))
        
        # Buscar palabras exactas
        self.assertEqual(self.trie.buscar("manzana"), "manzana")
        self.assertEqual(self.trie.buscar("banana"), "banana")
        self.assertIsNone(self.trie.buscar("pera"))
        
        # Case insensitive
        self.assertEqual(self.trie.buscar("MANZANA"), "manzana")
        
        print("✓ Inserción y búsqueda funcionan correctamente")
    
    def test_trie_comienza_con(self):
        """Prueba la verificación de prefijos."""
        print("\n=== PRUEBA TRIE: Comienza Con ===")
        
        self.trie.insertar("python")
        self.trie.insertar("javascript")
        self.trie.insertar("java")
        
        self.assertTrue(self.trie.comienza_con("py"))
        self.assertTrue(self.trie.comienza_con("java"))
        self.assertFalse(self.trie.comienza_con("ruby"))
        
        print("✓ Verificación de prefijos funciona correctamente")
    
    def test_trie_autocompletado(self):
        """Prueba el autocompletado."""
        print("\n=== PRUEBA TRIE: Autocompletado ===")
        
        # Insertar títulos de libros
        titulos = [
            "Don Quijote de la Mancha",
            "Don Juan Tenorio",
            "Doña Bárbara",
            "El principito",
            "Cien años de soledad"
        ]
        
        for titulo in titulos:
            self.trie.insertar(titulo)
        
        # Autocompletar "don"
        sugerencias = self.trie.autocompletar("don", limite=10)
        self.assertEqual(len(sugerencias), 2)  # Don Quijote, Don Juan (Doña starts with "doñ")
        
        # Autocompletar "cien"
        sugerencias_cien = self.trie.autocompletar("cien", limite=10)
        self.assertEqual(len(sugerencias_cien), 1)
        self.assertIn("cien años de soledad", [s[0] for s in sugerencias_cien])
        
        print("✓ Autocompletado funciona correctamente")
    
    def test_trie_frecuencias(self):
        """Prueba el tracking de frecuencias."""
        print("\n=== PRUEBA TRIE: Frecuencias ===")
        
        # Insertar la misma palabra varias veces
        self.trie.insertar("python")
        self.trie.insertar("python")  # Incrementa frecuencia
        self.trie.insertar("python")
        self.trie.insertar("java")
        
        # Obtener sugerencias (deben estar ordenadas por frecuencia)
        sugerencias = self.trie.autocompletar("", limite=10)
        
        # "python" debe tener frecuencia 3, "java" frecuencia 1
        python_freq = next(s[2] for s in sugerencias if s[0] == "python")
        java_freq = next(s[2] for s in sugerencias if s[0] == "java")
        
        self.assertEqual(python_freq, 3)
        self.assertEqual(java_freq, 1)
        
        print("✓ Tracking de frecuencias funciona correctamente")
    
    def test_trie_eliminacion(self):
        """Prueba la eliminación de palabras."""
        print("\n=== PRUEBA TRIE: Eliminación ===")
        
        self.trie.insertar("manzana")
        self.trie.insertar("mandarina")
        self.trie.insertar("mango")
        
        # Eliminar "mandarina"
        self.assertTrue(self.trie.eliminar("mandarina"))
        self.assertIsNone(self.trie.buscar("mandarina"))
        
        # Las demás palabras siguen
        self.assertIsNotNone(self.trie.buscar("manzana"))
        self.assertIsNotNone(self.trie.buscar("mango"))
        
        # Intentar eliminar palabra inexistente
        self.assertFalse(self.trie.eliminar("pera"))
        
        print("✓ Eliminación funciona correctamente")
    
    def test_trie_con_libros(self):
        """Prueba el Trie con títulos de libros reales."""
        print("\n=== PRUEBA TRIE: Con Títulos de Libros ===")
        
        # Crear libros
        libro1 = Libro("978-1", "Cien años de soledad", "García Márquez", "Ficción", 1967)
        libro2 = Libro("978-2", "Cien días en Somalia", "Autor B", "Historia", 2000)
        libro3 = Libro("978-3", "El amor en los tiempos del cólera", "García Márquez", "Ficción", 1985)
        
        # Insertar en Trie
        self.trie.insertar(libro1.titulo, libro1)
        self.trie.insertar(libro2.titulo, libro2)
        self.trie.insertar(libro3.titulo, libro3)
        
        # Autocompletar "cien"
        sugerencias = self.trie.autocompletar("cien", limite=10)
        self.assertEqual(len(sugerencias), 2)
        
        # Verificar que retorna objetos Libro
        for _, libro, _ in sugerencias:
            self.assertIsInstance(libro, Libro)
        
        print("✓ Trie funciona correctamente con objetos Libro")


class TestArbolCategorias(unittest.TestCase):
    """
    Conjunto de pruebas para validar el Árbol N-ario de Categorías.
    """
    
    def setUp(self):
        """Configuración inicial para cada prueba."""
        self.arbol = ArbolCategorias("Biblioteca")
    
    def test_arbol_agregar_categorias(self):
        """Prueba agregar categorías."""
        print("\n=== PRUEBA ÁRBOL N-ARIO: Agregar Categorías ===")
        
        # Agregar categorías de primer nivel
        self.assertTrue(self.arbol.agregar_categoria("Ficción", "Biblioteca"))
        self.assertTrue(self.arbol.agregar_categoria("No Ficción", "Biblioteca"))
        
        # Agregar subcategorías
        self.assertTrue(self.arbol.agregar_categoria("Ciencia Ficción", "Ficción"))
        self.assertTrue(self.arbol.agregar_categoria("Fantasía", "Ficción"))
        
        # Intentar agregar con padre inexistente
        self.assertFalse(self.arbol.agregar_categoria("Subcategoría", "Inexistente"))
        
        self.assertEqual(self.arbol.obtener_tamaño(), 5)  # Raíz + 4 categorías
        
        print("✓ Agregar categorías funciona correctamente")
    
    def test_arbol_buscar_categoria(self):
        """Prueba buscar categorías."""
        print("\n=== PRUEBA ÁRBOL N-ARIO: Buscar Categoría ===")
        
        self.arbol.agregar_categoria("Ficción", "Biblioteca")
        self.arbol.agregar_categoria("Ciencia Ficción", "Ficción")
        
        # Buscar categorías existentes
        ficcion = self.arbol.buscar_categoria("Ficción")
        self.assertIsNotNone(ficcion)
        self.assertEqual(ficcion.nombre, "Ficción")
        
        cf = self.arbol.buscar_categoria("Ciencia Ficción")
        self.assertIsNotNone(cf)
        self.assertEqual(cf.padre.nombre, "Ficción")
        
        # Buscar categoría inexistente
        inexistente = self.arbol.buscar_categoria("Terror")
        self.assertIsNone(inexistente)
        
        print("✓ Búsqueda de categorías funciona correctamente")
    
    def test_arbol_agregar_datos(self):
        """Prueba agregar datos a categorías."""
        print("\n=== PRUEBA ÁRBOL N-ARIO: Agregar Datos ===")
        
        self.arbol.agregar_categoria("Ficción", "Biblioteca")
        self.arbol.agregar_categoria("Distopía", "Ficción")
        
        # Crear libros
        libro1 = Libro("978-1", "1984", "Orwell", "Distopía", 1949)
        libro2 = Libro("978-2", "Fahrenheit 451", "Bradbury", "Distopía", 1953)
        
        # Agregar a categoría
        self.assertTrue(self.arbol.agregar_dato_a_categoria("Distopía", libro1))
        self.assertTrue(self.arbol.agregar_dato_a_categoria("Distopía", libro2))
        
        # Intentar agregar a categoría inexistente
        self.assertFalse(self.arbol.agregar_dato_a_categoria("Terror", libro1))
        
        # Obtener datos
        datos = self.arbol.obtener_datos_categoria("Distopía")
        self.assertEqual(len(datos), 2)
        
        print("✓ Agregar datos a categorías funciona correctamente")
    
    def test_arbol_datos_recursivos(self):
        """Prueba obtener datos incluyendo subcategorías."""
        print("\n=== PRUEBA ÁRBOL N-ARIO: Datos Recursivos ===")
        
        # Crear jerarquía
        self.arbol.agregar_categoria("Ficción", "Biblioteca")
        self.arbol.agregar_categoria("Ciencia Ficción", "Ficción")
        self.arbol.agregar_categoria("Distopía", "Ciencia Ficción")
        
        # Agregar libros a diferentes niveles
        libro1 = Libro("978-1", "Libro Ficción", "Autor", "Ficción", 2020)
        libro2 = Libro("978-2", "Libro CF", "Autor", "CF", 2020)
        libro3 = Libro("978-3", "Libro Distopía", "Autor", "Distopía", 2020)
        
        self.arbol.agregar_dato_a_categoria("Ficción", libro1)
        self.arbol.agregar_dato_a_categoria("Ciencia Ficción", libro2)
        self.arbol.agregar_dato_a_categoria("Distopía", libro3)
        
        # Obtener datos sin recursión
        datos_cf = self.arbol.obtener_datos_categoria("Ciencia Ficción", incluir_subcategorias=False)
        self.assertEqual(len(datos_cf), 1)  # Solo libro2
        
        # Obtener datos con recursión
        datos_cf_recursivo = self.arbol.obtener_datos_categoria("Ciencia Ficción", incluir_subcategorias=True)
        self.assertEqual(len(datos_cf_recursivo), 2)  # libro2 y libro3
        
        # Obtener datos de Ficción con recursión
        datos_ficcion = self.arbol.obtener_datos_categoria("Ficción", incluir_subcategorias=True)
        self.assertEqual(len(datos_ficcion), 3)  # Todos los libros
        
        print("✓ Obtención recursiva de datos funciona correctamente")
    
    def test_arbol_obtener_subcategorias(self):
        """Prueba obtener subcategorías directas."""
        print("\n=== PRUEBA ÁRBOL N-ARIO: Obtener Subcategorías ===")
        
        self.arbol.agregar_categoria("Ficción", "Biblioteca")
        self.arbol.agregar_categoria("Ciencia Ficción", "Ficción")
        self.arbol.agregar_categoria("Fantasía", "Ficción")
        self.arbol.agregar_categoria("Realismo", "Ficción")
        
        # Obtener subcategorías de Ficción
        subs = self.arbol.obtener_subcategorias("Ficción")
        self.assertEqual(len(subs), 3)
        self.assertIn("Ciencia Ficción", subs)
        self.assertIn("Fantasía", subs)
        self.assertIn("Realismo", subs)
        
        # Obtener subcategorías de hoja (no tiene)
        subs_cf = self.arbol.obtener_subcategorias("Ciencia Ficción")
        self.assertEqual(len(subs_cf), 0)
        
        print("✓ Obtención de subcategorías funciona correctamente")
    
    def test_arbol_altura(self):
        """Prueba el cálculo de altura del árbol."""
        print("\n=== PRUEBA ÁRBOL N-ARIO: Altura ===")
        
        # Árbol con solo raíz
        self.assertEqual(self.arbol.obtener_altura(), 0)
        
        # Agregar un nivel
        self.arbol.agregar_categoria("Nivel 1", "Biblioteca")
        self.assertEqual(self.arbol.obtener_altura(), 1)
        
        # Agregar otro nivel
        self.arbol.agregar_categoria("Nivel 2", "Nivel 1")
        self.assertEqual(self.arbol.obtener_altura(), 2)
        
        # Agregar hermano en nivel 1 (no aumenta altura)
        self.arbol.agregar_categoria("Nivel 1 Hermano", "Biblioteca")
        self.assertEqual(self.arbol.obtener_altura(), 2)
        
        print("✓ Cálculo de altura funciona correctamente")


def ejecutar_pruebas_arboles():
    """
    Ejecuta todas las pruebas de árboles y muestra los resultados.
    """
    print("="*70)
    print("INICIANDO PRUEBAS DE ESTRUCTURAS DE ÁRBOLES")
    print("="*70)
    
    # Crear suite de pruebas
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Agregar pruebas
    suite.addTests(loader.loadTestsFromTestCase(TestArbolAVL))
    suite.addTests(loader.loadTestsFromTestCase(TestMinHeap))
    suite.addTests(loader.loadTestsFromTestCase(TestTrie))
    suite.addTests(loader.loadTestsFromTestCase(TestArbolCategorias))
    
    # Ejecutar pruebas
    runner = unittest.TextTestRunner(verbosity=2)
    resultado = runner.run(suite)
    
    # Mostrar resumen
    print("\n" + "="*70)
    print("RESUMEN DE PRUEBAS DE ÁRBOLES")
    print("="*70)
    print(f"Pruebas ejecutadas: {resultado.testsRun}")
    print(f"Exitosas: {resultado.testsRun - len(resultado.failures) - len(resultado.errors)}")
    print(f"Fallidas: {len(resultado.failures)}")
    print(f"Errores: {len(resultado.errors)}")
    
    if resultado.wasSuccessful():
        print("\n🎉 TODAS LAS PRUEBAS DE ÁRBOLES PASARON EXITOSAMENTE")
        print("Las estructuras de árboles están implementadas correctamente.")
    else:
        print("\n❌ ALGUNAS PRUEBAS FALLARON")
        if resultado.failures:
            print("\nFALLAS:")
            for test, traceback in resultado.failures:
                print(f"  - {test}")
        if resultado.errors:
            print("\nERRORES:")
            for test, traceback in resultado.errors:
                print(f"  - {test}")
    
    return resultado.wasSuccessful()


if __name__ == "__main__":
    import sys
    
    print("\nSISTEMA DE PRUEBAS - ESTRUCTURAS DE ÁRBOLES")
    print("Curso: Estructuras de Datos - Unidad 2")
    print("Implementación de Árboles AVL, Heap, Trie y N-ario\n")
    
    exito = ejecutar_pruebas_arboles()
    
    sys.exit(0 if exito else 1)
