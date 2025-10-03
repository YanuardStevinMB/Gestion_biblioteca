"""
Sistema de Pruebas para el Sistema de Gestión de Biblioteca
==========================================================

Este módulo contiene las pruebas unitarias y de integración
para validar el funcionamiento correcto del sistema de gestión
de biblioteca y sus estructuras de datos lineales.

Autor: [Tu nombre]
Fecha: 2024
Curso: Estructuras de Datos - Unidad 1
"""

import unittest
import sys
import os
from datetime import datetime, timedelta

# Agregar el directorio actual al path para importaciones
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from estructuras_datos import ListaEnlazada, Pila, Cola, ArregloDinamico
from modelos import Libro, Usuario, Prestamo, BibliotecaManager

class TestEstructurasDatos(unittest.TestCase):
    """
    Conjunto de pruebas para validar las estructuras de datos lineales.
    
    Estas pruebas demuestran que las implementaciones personalizadas
    funcionan correctamente según las especificaciones.
    """
    
    def setUp(self):
        """Configuración inicial para cada prueba."""
        self.lista = ListaEnlazada()
        self.pila = Pila()
        self.cola = Cola()
        self.arreglo = ArregloDinamico()
    
    def test_lista_enlazada_operaciones_basicas(self):
        """Prueba las operaciones básicas de la lista enlazada."""
        print("\n=== PRUEBAS DE LISTA ENLAZADA ===")
        
        # Inserción
        self.lista.insertar_al_inicio("Elemento 1")
        self.lista.insertar_al_final("Elemento 2")
        self.lista.insertar_al_final("Elemento 3")
        
        self.assertEqual(self.lista.obtener_tamaño(), 3)
        self.assertFalse(self.lista.esta_vacia())
        
        # Búsqueda
        elementos = self.lista.buscar(lambda x: "2" in x)
        self.assertEqual(len(elementos), 1)
        self.assertEqual(elementos[0], "Elemento 2")
        
        # Obtener todos
        todos = self.lista.obtener_todos()
        self.assertEqual(len(todos), 3)
        
        # Eliminación
        eliminado = self.lista.eliminar(lambda x: x == "Elemento 2")
        self.assertTrue(eliminado)
        self.assertEqual(self.lista.obtener_tamaño(), 2)
        
        print("✓ Lista enlazada: Inserción, búsqueda y eliminación funcionan correctamente")
    
    def test_pila_operaciones_lifo(self):
        """Prueba el comportamiento LIFO de la pila."""
        print("\n=== PRUEBAS DE PILA (LIFO) ===")
        
        # Verificar pila vacía
        self.assertTrue(self.pila.esta_vacia())
        self.assertIsNone(self.pila.desapilar())
        self.assertIsNone(self.pila.ver_tope())
        
        # Apilar elementos
        self.pila.apilar("Primero")
        self.pila.apilar("Segundo")
        self.pila.apilar("Tercero")
        
        self.assertEqual(self.pila.obtener_tamaño(), 3)
        self.assertFalse(self.pila.esta_vacia())
        
        # Verificar LIFO
        self.assertEqual(self.pila.ver_tope(), "Tercero")
        
        desapilado1 = self.pila.desapilar()
        desapilado2 = self.pila.desapilar()
        desapilado3 = self.pila.desapilar()
        
        self.assertEqual(desapilado1, "Tercero")
        self.assertEqual(desapilado2, "Segundo")
        self.assertEqual(desapilado3, "Primero")
        self.assertTrue(self.pila.esta_vacia())
        
        print("✓ Pila: Comportamiento LIFO verificado correctamente")
    
    def test_cola_operaciones_fifo(self):
        """Prueba el comportamiento FIFO de la cola."""
        print("\n=== PRUEBAS DE COLA (FIFO) ===")
        
        # Verificar cola vacía
        self.assertTrue(self.cola.esta_vacia())
        self.assertIsNone(self.cola.desencolar())
        self.assertIsNone(self.cola.ver_frente())
        
        # Encolar elementos
        self.cola.encolar("Primero")
        self.cola.encolar("Segundo")
        self.cola.encolar("Tercero")
        
        self.assertEqual(self.cola.obtener_tamaño(), 3)
        self.assertFalse(self.cola.esta_vacia())
        
        # Verificar FIFO
        self.assertEqual(self.cola.ver_frente(), "Primero")
        
        desencolado1 = self.cola.desencolar()
        desencolado2 = self.cola.desencolar()
        desencolado3 = self.cola.desencolar()
        
        self.assertEqual(desencolado1, "Primero")
        self.assertEqual(desencolado2, "Segundo")
        self.assertEqual(desencolado3, "Tercero")
        self.assertTrue(self.cola.esta_vacia())
        
        print("✓ Cola: Comportamiento FIFO verificado correctamente")
    
    def test_arreglo_dinamico_operaciones(self):
        """Prueba las operaciones del arreglo dinámico."""
        print("\n=== PRUEBAS DE ARREGLO DINÁMICO ===")
        
        # Verificar arreglo vacío
        self.assertTrue(self.arreglo.esta_vacio())
        self.assertEqual(self.arreglo.obtener_tamaño(), 0)
        
        # Agregar elementos
        for i in range(15):  # Más que la capacidad inicial
            self.arreglo.agregar(f"Elemento {i}")
        
        self.assertEqual(self.arreglo.obtener_tamaño(), 15)
        self.assertFalse(self.arreglo.esta_vacio())
        
        # Acceso indexado
        self.assertEqual(self.arreglo.obtener(0), "Elemento 0")
        self.assertEqual(self.arreglo.obtener(14), "Elemento 14")
        
        # Establecer valor
        self.arreglo.establecer(5, "Elemento Modificado")
        self.assertEqual(self.arreglo.obtener(5), "Elemento Modificado")
        
        # Búsqueda
        modificados = self.arreglo.buscar(lambda x: "Modificado" in x)
        self.assertEqual(len(modificados), 1)
        
        # Eliminación
        eliminado = self.arreglo.eliminar(5)
        self.assertEqual(eliminado, "Elemento Modificado")
        self.assertEqual(self.arreglo.obtener_tamaño(), 14)
        
        print("✓ Arreglo dinámico: Redimensionamiento automático y operaciones funcionan correctamente")

class TestModelosDatos(unittest.TestCase):
    """
    Conjunto de pruebas para validar las clases del modelo de datos.
    """
    
    def test_libro_creacion_y_propiedades(self):
        """Prueba la creación y propiedades de un libro."""
        print("\n=== PRUEBAS DEL MODELO LIBRO ===")
        
        libro = Libro("978-84-376-0494-7", "Cien años de soledad", 
                     "Gabriel García Márquez", "Realismo Mágico", 1967)
        
        self.assertEqual(libro.isbn, "978-84-376-0494-7")
        self.assertEqual(libro.titulo, "Cien años de soledad")
        self.assertEqual(libro.autor, "Gabriel García Márquez")
        self.assertTrue(libro.disponible)
        
        info = libro.obtener_info_completa()
        self.assertIsInstance(info, dict)
        self.assertEqual(info['isbn'], "978-84-376-0494-7")
        
        print("✓ Libro: Creación y propiedades funcionan correctamente")
    
    def test_usuario_creacion_y_propiedades(self):
        """Prueba la creación y propiedades de un usuario."""
        print("\n=== PRUEBAS DEL MODELO USUARIO ===")
        
        usuario = Usuario("U001", "Juan Pérez", "juan@email.com", "123-456-7890")
        
        self.assertEqual(usuario.id_usuario, "U001")
        self.assertEqual(usuario.nombre, "Juan Pérez")
        self.assertEqual(usuario.prestamos_activos, 0)
        self.assertEqual(len(usuario.historial_prestamos), 0)
        
        info = usuario.obtener_info_completa()
        self.assertIsInstance(info, dict)
        self.assertEqual(info['id_usuario'], "U001")
        
        print("✓ Usuario: Creación y propiedades funcionan correctamente")
    
    def test_prestamo_creacion_y_estados(self):
        """Prueba la creación y manejo de estados de préstamos."""
        print("\n=== PRUEBAS DEL MODELO PRÉSTAMO ===")
        
        prestamo = Prestamo("P001", "978-84-376-0494-7", "U001", 7)
        
        self.assertEqual(prestamo.id_prestamo, "P001")
        self.assertEqual(prestamo.estado, "activo")
        self.assertIsNone(prestamo.fecha_devolucion)
        
        # Verificar días restantes
        dias = prestamo.dias_restantes()
        self.assertGreaterEqual(dias, 0)
        
        # Devolver el préstamo
        prestamo.devolver()
        self.assertEqual(prestamo.estado, "devuelto")
        self.assertIsNotNone(prestamo.fecha_devolucion)
        
        print("✓ Préstamo: Estados y transiciones funcionan correctamente")

class TestSistemaBiblioteca(unittest.TestCase):
    """
    Conjunto de pruebas para validar el sistema completo de biblioteca.
    """
    
    def setUp(self):
        """Configuración inicial para cada prueba."""
        self.biblioteca = BibliotecaManager()
    
    def test_registro_y_busqueda_libros(self):
        """Prueba el registro y búsqueda de libros."""
        print("\n=== PRUEBAS DE GESTIÓN DE LIBROS ===")
        
        # Registrar libro nuevo
        resultado = self.biblioteca.registrar_libro(
            "978-test-001", "Libro de Prueba", "Autor Test", "Prueba", 2024
        )
        self.assertTrue(resultado)
        
        # Intentar registrar el mismo libro (debe fallar)
        resultado_duplicado = self.biblioteca.registrar_libro(
            "978-test-001", "Otro Título", "Otro Autor", "Otra Categoría", 2024
        )
        self.assertFalse(resultado_duplicado)
        
        # Búsqueda por título
        libros_titulo = self.biblioteca.buscar_libros("titulo", "Prueba")
        self.assertGreater(len(libros_titulo), 0)
        
        # Búsqueda por autor
        libros_autor = self.biblioteca.buscar_libros("autor", "Test")
        self.assertGreater(len(libros_autor), 0)
        
        print("✓ Gestión de libros: Registro y búsqueda funcionan correctamente")
    
    def test_registro_y_busqueda_usuarios(self):
        """Prueba el registro y búsqueda de usuarios."""
        print("\n=== PRUEBAS DE GESTIÓN DE USUARIOS ===")
        
        # Registrar usuario nuevo
        user_id = self.biblioteca.registrar_usuario(
            "Usuario Test", "test@email.com", "555-0123"
        )
        self.assertIsNotNone(user_id)
        
        # Intentar registrar usuario con mismo email (debe fallar)
        user_id_duplicado = self.biblioteca.registrar_usuario(
            "Otro Usuario", "test@email.com", "555-0124"
        )
        self.assertIsNone(user_id_duplicado)
        
        # Búsqueda por nombre
        usuarios_nombre = self.biblioteca.buscar_usuarios("nombre", "Test")
        self.assertGreater(len(usuarios_nombre), 0)
        
        # Búsqueda por ID
        usuario = self.biblioteca.obtener_usuario_por_id(user_id)
        self.assertIsNotNone(usuario)
        self.assertEqual(usuario.id_usuario, user_id)
        
        print("✓ Gestión de usuarios: Registro y búsqueda funcionan correctamente")
    
    def test_sistema_prestamos_completo(self):
        """Prueba el sistema completo de préstamos."""
        print("\n=== PRUEBAS DE SISTEMA DE PRÉSTAMOS ===")
        
        # Obtener un libro disponible y un usuario existente
        libros = self.biblioteca.obtener_todos_los_libros()
        usuarios = self.biblioteca.obtener_todos_los_usuarios()
        
        self.assertGreater(len(libros), 0)
        self.assertGreater(len(usuarios), 0)
        
        libro_disponible = None
        for libro in libros:
            if libro.disponible:
                libro_disponible = libro
                break
        
        self.assertIsNotNone(libro_disponible)
        usuario = usuarios[0]
        
        # Realizar préstamo
        loan_id = self.biblioteca.realizar_prestamo(
            libro_disponible.isbn, usuario.id_usuario
        )
        self.assertIsNotNone(loan_id)
        
        # Verificar que el libro ya no está disponible
        libro_prestado = self.biblioteca.obtener_libro_por_isbn(libro_disponible.isbn)
        self.assertFalse(libro_prestado.disponible)
        
        # Verificar préstamos activos
        prestamos_activos = self.biblioteca.obtener_prestamos_activos()
        self.assertGreater(len(prestamos_activos), 0)
        
        # Devolver el libro
        resultado_devolucion = self.biblioteca.devolver_libro(loan_id)
        self.assertTrue(resultado_devolucion)
        
        # Verificar que el libro está disponible nuevamente
        libro_devuelto = self.biblioteca.obtener_libro_por_isbn(libro_disponible.isbn)
        self.assertTrue(libro_devuelto.disponible)
        
        print("✓ Sistema de préstamos: Préstamo y devolución funcionan correctamente")
    
    def test_estadisticas_sistema(self):
        """Prueba las estadísticas del sistema."""
        print("\n=== PRUEBAS DE ESTADÍSTICAS ===")
        
        stats = self.biblioteca.obtener_estadisticas()
        
        # Verificar que las estadísticas contienen los campos esperados
        campos_esperados = [
            'total_libros', 'libros_disponibles', 'libros_prestados',
            'total_usuarios', 'prestamos_activos', 'solicitudes_pendientes'
        ]
        
        for campo in campos_esperados:
            self.assertIn(campo, stats)
            self.assertIsInstance(stats[campo], int)
        
        # Verificar coherencia de datos
        self.assertEqual(
            stats['total_libros'],
            stats['libros_disponibles'] + stats['libros_prestados']
        )
        
        print("✓ Estadísticas: Cálculos y coherencia verificados correctamente")

def demostrar_estructuras_datos():
    """
    Función de demostración que muestra el uso de las estructuras de datos
    en contextos reales del sistema de biblioteca.
    """
    print("\n" + "="*60)
    print("DEMOSTRACIÓN DEL USO DE ESTRUCTURAS DE DATOS LINEALES")
    print("="*60)
    
    biblioteca = BibliotecaManager()
    
    print("\n1. LISTA ENLAZADA (Gestión de Libros)")
    print("-" * 40)
    libros = biblioteca.obtener_todos_los_libros()
    print(f"Total de libros almacenados: {len(libros)}")
    for i, libro in enumerate(libros[:3]):
        print(f"  {i+1}. {libro.titulo} - {libro.autor}")
    
    print("\n2. ARREGLO DINÁMICO (Gestión de Usuarios)")
    print("-" * 40)
    usuarios = biblioteca.obtener_todos_los_usuarios()
    print(f"Total de usuarios registrados: {len(usuarios)}")
    for i, usuario in enumerate(usuarios):
        print(f"  {i+1}. {usuario.nombre} ({usuario.id_usuario})")
    
    print("\n3. PILA (Historial de Préstamos)")
    print("-" * 40)
    
    # Realizar algunos préstamos de demostración
    if len(libros) > 0 and len(usuarios) > 0:
        libro_test = libros[0]
        usuario_test = usuarios[0]
        
        if libro_test.disponible:
            loan_id = biblioteca.realizar_prestamo(libro_test.isbn, usuario_test.id_usuario)
            if loan_id:
                print(f"  Préstamo realizado: {loan_id}")
                
                # Mostrar historial reciente
                historial = biblioteca.obtener_historial_prestamos(5)
                print(f"  Últimos {len(historial)} préstamos en la pila:")
                for prestamo in historial:
                    print(f"    - {prestamo.id_prestamo}: {prestamo.isbn_libro}")
    
    print("\n4. COLA (Solicitudes Pendientes)")
    print("-" * 40)
    
    # Agregar algunas solicitudes de ejemplo
    if len(libros) > 1 and len(usuarios) > 1:
        biblioteca.agregar_solicitud_prestamo(libros[1].isbn, usuarios[1].id_usuario)
        solicitudes = biblioteca.obtener_solicitudes_pendientes()
        print(f"  Solicitudes en cola: {len(solicitudes)}")
        
        for i, solicitud in enumerate(solicitudes):
            print(f"    {i+1}. Usuario {solicitud['id_usuario']} - Libro {solicitud['isbn_libro']}")
    
    print("\n5. ESTADÍSTICAS GENERALES")
    print("-" * 40)
    stats = biblioteca.obtener_estadisticas()
    for clave, valor in stats.items():
        print(f"  {clave.replace('_', ' ').title()}: {valor}")

def ejecutar_pruebas_completas():
    """
    Ejecuta todas las pruebas del sistema y muestra los resultados.
    """
    print("INICIANDO PRUEBAS DEL SISTEMA DE GESTIÓN DE BIBLIOTECA")
    print("=" * 60)
    
    # Crear suite de pruebas usando TestLoader
    loader = unittest.TestLoader()
    test_suite = unittest.TestSuite()
    
    # Agregar pruebas de estructuras de datos
    test_suite.addTests(loader.loadTestsFromTestCase(TestEstructurasDatos))
    test_suite.addTests(loader.loadTestsFromTestCase(TestModelosDatos))
    test_suite.addTests(loader.loadTestsFromTestCase(TestSistemaBiblioteca))
    
    # Ejecutar pruebas
    runner = unittest.TextTestRunner(verbosity=2)
    resultado = runner.run(test_suite)
    
    # Mostrar resumen
    print("\n" + "="*60)
    print("RESUMEN DE PRUEBAS")
    print("="*60)
    print(f"Pruebas ejecutadas: {resultado.testsRun}")
    print(f"Exitosas: {resultado.testsRun - len(resultado.failures) - len(resultado.errors)}")
    print(f"Fallidas: {len(resultado.failures)}")
    print(f"Errores: {len(resultado.errors)}")
    
    if resultado.failures:
        print("\nFALLAS:")
        for test, traceback in resultado.failures:
            print(f"  - {test}: {traceback}")
    
    if resultado.errors:
        print("\nERRORES:")
        for test, traceback in resultado.errors:
            print(f"  - {test}: {traceback}")
    
    # Ejecutar demostración
    demostrar_estructuras_datos()
    
    return resultado.wasSuccessful()

if __name__ == "__main__":
    print("SISTEMA DE PRUEBAS - GESTIÓN DE BIBLIOTECA")
    print("Curso: Estructuras de Datos - Unidad 1")
    print("Implementación de Estructuras de Datos Lineales\n")
    
    exito = ejecutar_pruebas_completas()
    
    if exito:
        print("\n🎉 TODAS LAS PRUEBAS PASARON EXITOSAMENTE")
        print("El sistema está funcionando correctamente.")
    else:
        print("\n❌ ALGUNAS PRUEBAS FALLARON")
        print("Revisar los errores mostrados arriba.")