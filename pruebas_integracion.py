"""
Pruebas de Integración - Sistema de Biblioteca con Árboles
==========================================================

Este módulo contiene pruebas que verifican la integración completa
del sistema de biblioteca con estructuras de datos lineales y árboles.

Autor: Equipo de Desarrollo Biblioteca Virtual
Fecha: 2025
Curso: Estructuras de Datos - Unidad 2
"""

import unittest
from modelos import BibliotecaManager, Libro, Usuario, Prestamo
from datetime import datetime


class TestIntegracionSistemaCompleto(unittest.TestCase):
    """
    Pruebas de integración que verifican el funcionamiento completo
    del sistema con estructuras lineales y árboles.
    """

    def setUp(self):
        """Configuración inicial para cada prueba."""
        self.biblioteca = BibliotecaManager()
        print("\n=== PRUEBA DE INTEGRACIÓN ===")

    def test_integracion_registro_y_busqueda_libros(self):
        """Prueba la integración completa de registro y búsqueda de libros."""
        print("Prueba: Registro y búsqueda integrada de libros")

        # Constantes para evitar duplicación
        LIBRO_PRUEBA_1 = "Libro de Prueba 1"
        LIBRO_PRUEBA_2 = "Libro de Prueba 2"
        AUTOR_A = "Autor A"
        AUTOR_B = "Autor B"
        CATEGORIA_TECNOLOGIA = "Tecnología"
        CATEGORIA_CIENCIA = "Ciencia"

        # Registrar libros adicionales
        libros_prueba = [
            ("978-1-234-56789-0", LIBRO_PRUEBA_1, AUTOR_A, CATEGORIA_TECNOLOGIA, 2020),
            ("978-2-345-67890-1", LIBRO_PRUEBA_2, AUTOR_B, CATEGORIA_CIENCIA, 2021),
            ("978-3-456-78901-2", "Otro Libro", AUTOR_A, CATEGORIA_TECNOLOGIA, 2019)
        ]

        for isbn, titulo, autor, categoria, anio in libros_prueba:
            resultado = self.biblioteca.registrar_libro(isbn, titulo, autor, categoria, anio)
            self.assertTrue(resultado, f"No se pudo registrar libro: {titulo}")

        # Verificar que se registraron en todas las estructuras
        self.assertEqual(self.biblioteca.libros.obtener_tamaño(), 8)  # 5 iniciales + 3 nuevas
        self.assertEqual(self.biblioteca.arbol_libros_isbn.obtener_tamaño(), 8)
        self.assertEqual(self.biblioteca.arbol_libros_titulo.obtener_tamaño(), 8)
        self.assertEqual(self.biblioteca.trie_titulos.obtener_tamaño(), 8)

        # Probar búsqueda por ISBN (usando AVL)
        libro_encontrado = self.biblioteca.buscar_libros("isbn", "978-1-234-56789-0")
        self.assertEqual(len(libro_encontrado), 1)
        self.assertEqual(libro_encontrado[0].titulo, LIBRO_PRUEBA_1)

        # Probar búsqueda por título (usando AVL)
        libro_titulo = self.biblioteca.buscar_libros("titulo", LIBRO_PRUEBA_1)
        self.assertEqual(len(libro_titulo), 1)
        self.assertEqual(libro_titulo[0].titulo, LIBRO_PRUEBA_1)

        # Probar búsqueda por categoría (usando árbol N-ario)
        libros_tecnologia = self.biblioteca.buscar_libros("categoria", CATEGORIA_TECNOLOGIA)
        self.assertEqual(len(libros_tecnologia), 2)  # 2 libros en Tecnología

        # Probar autocompletado
        sugerencias = self.biblioteca.autocompletar_titulos("Libro", 5)
        self.assertGreater(len(sugerencias), 0)
        titulos_sugeridos = [titulo for titulo, _, _ in sugerencias]
        self.assertIn("libro de prueba 1", titulos_sugeridos)

        print("✓ Integración de libros funciona correctamente")

    def test_integracion_registro_y_busqueda_usuarios(self):
        """Prueba la integración completa de registro y búsqueda de usuarios."""
        print("Prueba: Registro y búsqueda integrada de usuarios")

        # Registrar usuarios adicionales
        usuarios_prueba = [
            ("Ana López", "ana.lopez@email.com", "111-222-333"),
            ("Carlos Ruiz", "carlos.ruiz@email.com", "444-555-666")
        ]

        for nombre, email, telefono in usuarios_prueba:
            id_usuario = self.biblioteca.registrar_usuario(nombre, email, telefono)
            self.assertIsNotNone(id_usuario, f"No se pudo registrar usuario: {nombre}")

        # Verificar que se registraron en todas las estructuras
        self.assertEqual(self.biblioteca.usuarios.obtener_tamaño(), 5)  # 3 iniciales + 2 nuevas
        self.assertEqual(self.biblioteca.arbol_usuarios_id.obtener_tamaño(), 5)
        self.assertEqual(self.biblioteca.arbol_usuarios_email.obtener_tamaño(), 5)

        # Probar búsqueda por ID (usando AVL)
        usuario_id = self.biblioteca.buscar_usuarios("id", "U004")  # Ana López
        self.assertEqual(len(usuario_id), 1)
        self.assertEqual(usuario_id[0].nombre, "Ana López")

        # Probar búsqueda por email (usando AVL)
        usuario_email = self.biblioteca.buscar_usuarios("email", "carlos.ruiz@email.com")
        self.assertEqual(len(usuario_email), 1)
        self.assertEqual(usuario_email[0].nombre, "Carlos Ruiz")

        print("✓ Integración de usuarios funciona correctamente")

    def test_integracion_sistema_prestamos_completo(self):
        """Prueba la integración completa del sistema de préstamos."""
        print("Prueba: Sistema de préstamos integrado")

        # Realizar préstamos
        prestamo1 = self.biblioteca.realizar_prestamo("978-84-376-0494-7", "U001")
        prestamo2 = self.biblioteca.realizar_prestamo("978-84-663-0016-6", "U002")

        self.assertIsNotNone(prestamo1)
        self.assertIsNotNone(prestamo2)

        # Verificar estados actualizados
        libro1 = self.biblioteca.obtener_libro_por_isbn("978-84-376-0494-7")
        libro2 = self.biblioteca.obtener_libro_por_isbn("978-84-663-0016-6")
        usuario1 = self.biblioteca.obtener_usuario_por_id("U001")
        usuario2 = self.biblioteca.obtener_usuario_por_id("U002")

        self.assertFalse(libro1.disponible)
        self.assertFalse(libro2.disponible)
        self.assertEqual(usuario1.prestamos_activos, 1)
        self.assertEqual(usuario2.prestamos_activos, 1)

        # Verificar que están en el heap
        self.assertEqual(self.biblioteca.heap_prestamos_vencimiento.obtener_tamaño(), 2)

        # Obtener préstamo más urgente
        prestamo_urgente = self.biblioteca.obtener_prestamo_mas_urgente()
        self.assertIsNotNone(prestamo_urgente)

        # Devolver un libro
        resultado_devolucion = self.biblioteca.devolver_libro(prestamo1)
        self.assertTrue(resultado_devolucion)

        # Verificar estados después de devolución
        libro1_actualizado = self.biblioteca.obtener_libro_por_isbn("978-84-376-0494-7")
        usuario1_actualizado = self.biblioteca.obtener_usuario_por_id("U001")

        self.assertTrue(libro1_actualizado.disponible)
        self.assertEqual(usuario1_actualizado.prestamos_activos, 0)

        print("✓ Sistema de préstamos integrado funciona correctamente")

    def test_integracion_busqueda_avanzada(self):
        """Prueba la búsqueda avanzada con múltiples criterios."""
        print("Prueba: Búsqueda avanzada integrada")

        # Constantes para evitar duplicación
        AUTOR_PYTHON = "Autor Python"
        CATEGORIA_PROGRAMACION = "Programación"

        # Registrar libros para prueba
        self.biblioteca.registrar_libro("978-9-999-99999-9", "Python Avanzado", AUTOR_PYTHON, CATEGORIA_PROGRAMACION, 2023)
        self.biblioteca.registrar_libro("978-8-888-88888-8", "Java Básico", "Autor Java", CATEGORIA_PROGRAMACION, 2022)

        # Búsqueda avanzada por categoría
        filtros = {"categoria": CATEGORIA_PROGRAMACION}
        resultados = self.biblioteca.buscar_libros_avanzada(filtros)
        self.assertEqual(len(resultados), 2)

        # Búsqueda avanzada por autor
        filtros_autor = {"autor": AUTOR_PYTHON}
        resultados_autor = self.biblioteca.buscar_libros_avanzada(filtros_autor)
        self.assertEqual(len(resultados_autor), 1)
        self.assertEqual(resultados_autor[0].titulo, "Python Avanzado")

        # Búsqueda avanzada múltiple
        filtros_multiples = {"categoria": CATEGORIA_PROGRAMACION, "autor": AUTOR_PYTHON}
        resultados_multiples = self.biblioteca.buscar_libros_avanzada(filtros_multiples)
        self.assertEqual(len(resultados_multiples), 1)

        print("✓ Búsqueda avanzada integrada funciona correctamente")

    def test_integracion_estadisticas_completas(self):
        """Prueba las estadísticas completas del sistema integrado."""
        print("Prueba: Estadísticas completas del sistema integrado")

        # Realizar algunas operaciones para tener datos
        self.biblioteca.registrar_libro("978-7-777-77777-7", "Libro Estadísticas", "Autor Estadísticas", "Estadística", 2024)
        self.biblioteca.registrar_usuario("Usuario Estadísticas", "usuario@estadisticas.com", "777-888-999")
        self.biblioteca.realizar_prestamo("978-84-376-0494-7", "U001")

        # Obtener estadísticas completas
        stats = self.biblioteca.obtener_estadisticas()

        # Verificar estadísticas básicas
        self.assertGreater(stats['total_libros'], 0)
        self.assertGreater(stats['total_usuarios'], 0)

        # Verificar estadísticas de índices
        self.assertIsInstance(stats['altura_arbol_libros_isbn'], int)
        self.assertIsInstance(stats['altura_arbol_usuarios_id'], int)
        self.assertIsInstance(stats['tamaño_trie_titulos'], int)
        self.assertIsInstance(stats['tamaño_heap_prestamos'], int)
        self.assertTrue(stats['indices_optimizados'])

        # Verificar mejoras de rendimiento
        self.assertGreaterEqual(stats['mejora_busqueda_libros_x'], 1)
        self.assertGreaterEqual(stats['mejora_busqueda_usuarios_x'], 1)

        print("✓ Estadísticas completas del sistema integrado funcionan correctamente")

    def test_integracion_arbol_categorias(self):
        """Prueba la integración del árbol de categorías."""
        print("Prueba: Árbol de categorías integrado")

        # Verificar categorías iniciales
        categorias = self.biblioteca.obtener_categorias_disponibles()
        self.assertGreater(len(categorias), 0)
        self.assertIn("Realismo Mágico", categorias)

        # Obtener libros por categoría
        libros_ficcion = self.biblioteca.obtener_libros_por_categoria("Realismo Mágico")
        self.assertGreater(len(libros_ficcion), 0)  # Debería haber libros en esta categoría

        # Verificar que incluye subcategorías
        libros_ficcion_completo = self.biblioteca.obtener_libros_por_categoria("Realismo Mágico", incluir_subcategorias=True)
        self.assertEqual(len(libros_ficcion_completo), len(libros_ficcion))  # No hay subcategorías

        print("✓ Árbol de categorías integrado funciona correctamente")

    def test_integracion_rendimiento_comparado(self):
        """Prueba comparativa de rendimiento entre estructuras lineales y árboles."""
        print("Prueba: Comparación de rendimiento integrado")

        # Agregar más libros para prueba de rendimiento
        for i in range(10, 50):  # Agregar 40 libros más
            isbn = f"978-9{i:03d}-00000-0"
            titulo = f"Libro de Rendimiento {i}"
            autor = f"Autor {i % 5}"
            categoria = ["Tecnología", "Ciencia", "Historia", "Literatura", "Arte"][i % 5]
            anio = 2000 + (i % 25)

            self.biblioteca.registrar_libro(isbn, titulo, autor, categoria, anio)

        # Verificar que todas las búsquedas funcionan
        # Buscar uno de los libros de ejemplo que siempre están disponibles
        libro_especifico = self.biblioteca.buscar_libros("isbn", "978-84-376-0494-7")  # "Cien años de soledad"
        self.assertEqual(len(libro_especifico), 1)  # Este libro debería existir

        # Verificar autocompletado con muchos libros
        sugerencias = self.biblioteca.autocompletar_titulos("Libro", 10)
        self.assertGreater(len(sugerencias), 0)

        # Verificar estadísticas finales
        stats_final = self.biblioteca.obtener_estadisticas()
        self.assertGreater(stats_final['altura_arbol_libros_isbn'], 0)
        self.assertGreater(stats_final['mejora_busqueda_libros_x'], 1)

        print("✓ Comparación de rendimiento integrado funciona correctamente")


def ejecutar_pruebas_integracion():
    """
    Ejecuta todas las pruebas de integración y muestra los resultados.
    """
    print("="*80)
    print("INICIANDO PRUEBAS DE INTEGRACIÓN - SISTEMA COMPLETO")
    print("="*80)

    # Crear suite de pruebas
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Agregar pruebas de integración
    suite.addTests(loader.loadTestsFromTestCase(TestIntegracionSistemaCompleto))

    # Ejecutar pruebas
    runner = unittest.TextTestRunner(verbosity=2)
    resultado = runner.run(suite)

    # Mostrar resumen
    print("\n" + "="*80)
    print("RESUMEN DE PRUEBAS DE INTEGRACIÓN")
    print("="*80)
    print(f"Pruebas ejecutadas: {resultado.testsRun}")
    print(f"Exitosas: {resultado.testsRun - len(resultado.failures) - len(resultado.errors)}")
    print(f"Fallidas: {len(resultado.failures)}")
    print(f"Errores: {len(resultado.errors)}")

    if resultado.wasSuccessful():
        print("\n🎉 TODAS LAS PRUEBAS DE INTEGRACIÓN PASARON EXITOSAMENTE")
        print("El sistema integrado con estructuras de árboles funciona correctamente.")
        print("Las mejoras de rendimiento están operativas.")
    else:
        print("\n❌ ALGUNAS PRUEBAS DE INTEGRACIÓN FALLARON")
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

    print("\nSISTEMA DE PRUEBAS DE INTEGRACIÓN")
    print("Biblioteca Virtual - Estructuras Lineales + Árboles")
    print("Curso: Estructuras de Datos - Unidades 1 y 2\n")

    exito = ejecutar_pruebas_integracion()

    sys.exit(0 if exito else 1)