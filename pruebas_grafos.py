"""
Suite de Pruebas para Estructuras de Grafos
==========================================

Pruebas unitarias y de integración para validar la implementación
de grafos en el sistema de gestión de biblioteca.

Autor: Sistema de Biblioteca Virtual
Fecha: 2024
Curso: Estructuras de Datos - Unidad 2 (Grafos)
"""

import unittest
import sys
import os

# Agregar el directorio actual al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from estructuras_grafos import Grafo, GrafoBipartito
from gestor_grafos import GestorGrafoBiblioteca
from modelos import BibliotecaManager, Libro, Usuario


class TestGrafoBasico(unittest.TestCase):
    """Pruebas para la clase Grafo base."""
    
    def setUp(self):
        """Configuración inicial para cada prueba."""
        self.grafo_no_dirigido = Grafo(dirigido=False, ponderado=False)
        self.grafo_dirigido = Grafo(dirigido=True, ponderado=False)
        self.grafo_ponderado = Grafo(dirigido=False, ponderado=True)
    
    def test_agregar_vertices_y_aristas(self):
        """Prueba agregar vértices y aristas básicas."""
        g = self.grafo_no_dirigido
        
        # Agregar vértices
        g.agregar_vertice("A")
        g.agregar_vertice("B")
        g.agregar_vertice("C")
        
        self.assertEqual(len(g.vertices), 3)
        
        # Agregar aristas
        g.agregar_arista("A", "B")
        g.agregar_arista("B", "C")
        
        self.assertTrue(g.tiene_arista("A", "B"))
        self.assertTrue(g.tiene_arista("B", "C"))
        # En grafo no dirigido, las aristas son bidireccionales
        self.assertTrue(g.tiene_arista("B", "A"))
    
    def test_grafo_dirigido(self):
        """Prueba que las aristas dirigidas sean unidireccionales."""
        g = self.grafo_dirigido
        
        g.agregar_arista("A", "B")
        
        self.assertTrue(g.tiene_arista("A", "B"))
        self.assertFalse(g.tiene_arista("B", "A"))
    
    def test_grafo_ponderado(self):
        """Prueba grafos con pesos en las aristas."""
        g = self.grafo_ponderado
        
        g.agregar_arista("A", "B", peso=5)
        g.agregar_arista("B", "C", peso=10)
        
        self.assertEqual(g.obtener_peso_arista("A", "B"), 5)
        self.assertEqual(g.obtener_peso_arista("B", "C"), 10)
    
    def test_eliminar_arista(self):
        """Prueba eliminación de aristas."""
        g = self.grafo_no_dirigido
        
        g.agregar_arista("A", "B")
        self.assertTrue(g.tiene_arista("A", "B"))
        
        g.eliminar_arista("A", "B")
        self.assertFalse(g.tiene_arista("A", "B"))
    
    def test_obtener_grado(self):
        """Prueba el cálculo del grado de un vértice."""
        g = self.grafo_no_dirigido
        
        g.agregar_arista("A", "B")
        g.agregar_arista("A", "C")
        g.agregar_arista("A", "D")
        
        self.assertEqual(g.obtener_grado("A"), 3)
        self.assertEqual(g.obtener_grado("B"), 1)


class TestAlgoritmosBFS_DFS(unittest.TestCase):
    """Pruebas para algoritmos de recorrido."""
    
    def setUp(self):
        """Crear un grafo de ejemplo."""
        self.grafo = Grafo(dirigido=False, ponderado=False)
        
        # Crear un grafo simple
        #     A --- B
        #     |     |
        #     C --- D
        self.grafo.agregar_arista("A", "B")
        self.grafo.agregar_arista("A", "C")
        self.grafo.agregar_arista("B", "D")
        self.grafo.agregar_arista("C", "D")
    
    def test_bfs_recorrido(self):
        """Prueba el recorrido BFS."""
        visitados = self.grafo.bfs("A")
        
        # BFS debe visitar todos los nodos
        self.assertEqual(len(visitados), 4)
        self.assertIn("A", visitados)
        self.assertIn("B", visitados)
        self.assertIn("C", visitados)
        self.assertIn("D", visitados)
        
        # El primer visitado debe ser el inicio
        self.assertEqual(visitados[0], "A")
    
    def test_dfs_recorrido(self):
        """Prueba el recorrido DFS."""
        visitados = self.grafo.dfs("A")
        
        # DFS debe visitar todos los nodos
        self.assertEqual(len(visitados), 4)
        self.assertIn("A", visitados)
        self.assertIn("B", visitados)
        self.assertIn("C", visitados)
        self.assertIn("D", visitados)
        
        # El primer visitado debe ser el inicio
        self.assertEqual(visitados[0], "A")
    
    def test_camino_mas_corto_bfs(self):
        """Prueba encontrar el camino más corto con BFS."""
        camino = self.grafo.camino_mas_corto_bfs("A", "D")
        
        self.assertIsNotNone(camino)
        self.assertEqual(camino[0], "A")
        self.assertEqual(camino[-1], "D")
        # El camino más corto tiene longitud 3 (A-B-D o A-C-D)
        self.assertEqual(len(camino), 3)
    
    def test_camino_inexistente(self):
        """Prueba buscar camino entre nodos no conectados."""
        self.grafo.agregar_vertice("E")  # Nodo aislado
        
        camino = self.grafo.camino_mas_corto_bfs("A", "E")
        self.assertIsNone(camino)


class TestDijkstra(unittest.TestCase):
    """Pruebas para el algoritmo de Dijkstra."""
    
    def setUp(self):
        """Crear un grafo ponderado."""
        self.grafo = Grafo(dirigido=True, ponderado=True)
        
        # Crear grafo con pesos
        #     A --5--> B
        #     |        |
        #     2        1
        #     |        |
        #     v        v
        #     C --3--> D
        self.grafo.agregar_arista("A", "B", 5)
        self.grafo.agregar_arista("A", "C", 2)
        self.grafo.agregar_arista("B", "D", 1)
        self.grafo.agregar_arista("C", "D", 3)
    
    def test_dijkstra_distancias(self):
        """Prueba que Dijkstra calcule correctamente las distancias mínimas."""
        distancias, padres = self.grafo.dijkstra("A")
        
        # Verificar distancias
        self.assertEqual(distancias["A"], 0)
        self.assertEqual(distancias["B"], 5)
        self.assertEqual(distancias["C"], 2)
        # A->C->D (2+3=5) vs A->B->D (5+1=6), debe elegir A->C->D
        self.assertEqual(distancias["D"], 5)
    
    def test_dijkstra_reconstruir_camino(self):
        """Prueba reconstrucción del camino más corto."""
        distancias, padres = self.grafo.dijkstra("A")
        camino = self.grafo.reconstruir_camino_dijkstra("A", "D", padres)
        
        self.assertIsNotNone(camino)
        self.assertEqual(camino[0], "A")
        self.assertEqual(camino[-1], "D")
        # El camino debe ser A -> C -> D
        self.assertEqual(camino, ["A", "C", "D"])


class TestGrafoConexo(unittest.TestCase):
    """Pruebas para verificar conectividad y componentes."""
    
    def test_grafo_conexo(self):
        """Prueba verificar si un grafo es conexo."""
        g = Grafo(dirigido=False, ponderado=False)
        
        # Crear grafo conexo
        g.agregar_arista("A", "B")
        g.agregar_arista("B", "C")
        g.agregar_arista("C", "D")
        
        self.assertTrue(g.es_conexo())
    
    def test_grafo_no_conexo(self):
        """Prueba grafo con componentes separadas."""
        g = Grafo(dirigido=False, ponderado=False)
        
        # Crear dos componentes separadas
        g.agregar_arista("A", "B")
        g.agregar_arista("C", "D")
        
        self.assertFalse(g.es_conexo())
    
    def test_componentes_conexas(self):
        """Prueba detectar todas las componentes conexas."""
        g = Grafo(dirigido=False, ponderado=False)
        
        # Componente 1: A-B-C
        g.agregar_arista("A", "B")
        g.agregar_arista("B", "C")
        
        # Componente 2: D-E
        g.agregar_arista("D", "E")
        
        # Componente 3: F (aislado)
        g.agregar_vertice("F")
        
        componentes = g.obtener_componentes_conexas()
        
        self.assertEqual(len(componentes), 3)
        # Verificar que cada componente tenga el tamaño correcto
        tamaños = sorted([len(c) for c in componentes])
        self.assertEqual(tamaños, [1, 2, 3])


class TestGrafoBipartito(unittest.TestCase):
    """Pruebas para el grafo bipartito usuario-libro."""
    
    def setUp(self):
        """Configuración inicial."""
        self.grafo = GrafoBipartito(ponderado=True)
    
    def test_agregar_usuarios_y_libros(self):
        """Prueba agregar usuarios y libros al grafo bipartito."""
        self.grafo.agregar_usuario("U001")
        self.grafo.agregar_usuario("U002")
        self.grafo.agregar_libro("L001")
        self.grafo.agregar_libro("L002")
        
        self.assertEqual(len(self.grafo.conjunto_a), 2)  # Usuarios
        self.assertEqual(len(self.grafo.conjunto_b), 2)  # Libros
    
    def test_agregar_interacciones(self):
        """Prueba registrar interacciones usuario-libro."""
        self.grafo.agregar_interaccion("U001", "L001", peso=1)
        self.grafo.agregar_interaccion("U001", "L002", peso=1)
        self.grafo.agregar_interaccion("U002", "L001", peso=2)
        
        # Verificar las interacciones
        libros_u001 = self.grafo.obtener_libros_de_usuario("U001")
        self.assertEqual(len(libros_u001), 2)
        
        usuarios_l001 = self.grafo.obtener_usuarios_de_libro("L001")
        self.assertEqual(len(usuarios_l001), 2)
    
    def test_incrementar_peso_interaccion(self):
        """Prueba que múltiples interacciones incrementen el peso."""
        self.grafo.agregar_interaccion("U001", "L001", peso=1)
        self.grafo.agregar_interaccion("U001", "L001", peso=1)
        
        peso = self.grafo.obtener_peso_arista("U001", "L001")
        self.assertEqual(peso, 2)
    
    def test_recomendar_libros(self):
        """Prueba el sistema de recomendaciones."""
        # Usuario 1 lee libros A y B
        self.grafo.agregar_interaccion("U001", "LA", 1)
        self.grafo.agregar_interaccion("U001", "LB", 1)
        
        # Usuario 2 lee libros A, B y C
        self.grafo.agregar_interaccion("U002", "LA", 1)
        self.grafo.agregar_interaccion("U002", "LB", 1)
        self.grafo.agregar_interaccion("U002", "LC", 1)
        
        # Usuario 3 lee libros B y C
        self.grafo.agregar_interaccion("U003", "LB", 1)
        self.grafo.agregar_interaccion("U003", "LC", 1)
        
        # Recomendar a usuario 1 (debería recomendar LC)
        recomendaciones = self.grafo.recomendar_libros("U001", top_n=5)
        
        self.assertGreater(len(recomendaciones), 0)
        # LC debe ser recomendado
        libros_recomendados = [libro for libro, _ in recomendaciones]
        self.assertIn("LC", libros_recomendados)
    
    def test_libros_populares(self):
        """Prueba obtener libros más populares."""
        # Simular múltiples préstamos
        self.grafo.agregar_interaccion("U001", "L001", 5)
        self.grafo.agregar_interaccion("U002", "L001", 3)
        self.grafo.agregar_interaccion("U003", "L002", 2)
        
        populares = self.grafo.obtener_libros_populares(top_n=2)
        
        # L001 debe ser el más popular (8 préstamos total)
        self.assertEqual(populares[0][0], "L001")
        self.assertEqual(populares[0][1], 8)


class TestGestorGrafoBiblioteca(unittest.TestCase):
    """Pruebas de integración para el gestor de grafos."""
    
    def setUp(self):
        """Configuración inicial."""
        self.biblioteca = BibliotecaManager()
        self.gestor = GestorGrafoBiblioteca(self.biblioteca)
    
    def test_inicializacion_desde_prestamos(self):
        """Prueba que el grafo se inicialice con préstamos existentes."""
        # El sistema puede o no tener préstamos iniciales
        stats = self.gestor.obtener_estadisticas_grafo()
        
        # Verificar que las estructuras existan
        self.assertIsNotNone(stats)
        self.assertIn('interacciones', stats)
        self.assertGreaterEqual(stats['interacciones']['total_interacciones'], 0)
    
    def test_registrar_interaccion(self):
        """Prueba registrar una nueva interacción."""
        num_inicial = self.gestor.num_interacciones
        
        # Registrar nueva interacción
        self.gestor.registrar_interaccion("U001", "978-84-376-0494-7", peso=1)
        
        # Verificar que se incrementó
        self.assertEqual(self.gestor.num_interacciones, num_inicial + 1)
    
    def test_recomendar_libros_usuario(self):
        """Prueba el sistema de recomendaciones integrado."""
        # Usar un usuario del sistema
        recomendaciones = self.gestor.recomendar_libros_usuario("U001", top_n=3)
        
        # Debe retornar recomendaciones
        self.assertIsInstance(recomendaciones, list)
        # Cada recomendación debe tener la estructura correcta
        if len(recomendaciones) > 0:
            self.assertIn('libro', recomendaciones[0])
            self.assertIn('score', recomendaciones[0])
            self.assertIn('razon', recomendaciones[0])
    
    def test_libros_populares(self):
        """Prueba obtener libros populares."""
        populares = self.gestor.obtener_libros_populares(top_n=5)
        
        self.assertIsInstance(populares, list)
        # Debe estar ordenado por popularidad
        if len(populares) > 1:
            self.assertGreaterEqual(
                populares[0]['num_prestamos'],
                populares[1]['num_prestamos']
            )
    
    def test_usuarios_activos(self):
        """Prueba obtener usuarios más activos."""
        activos = self.gestor.obtener_usuarios_activos(top_n=5)
        
        self.assertIsInstance(activos, list)
        # Debe retornar tuplas (usuario_id, num_prestamos)
        if len(activos) > 0:
            self.assertIsInstance(activos[0], tuple)
            self.assertEqual(len(activos[0]), 2)
    
    def test_detectar_comunidades(self):
        """Prueba detección de comunidades de lectores."""
        comunidades = self.gestor.detectar_comunidades_lectores()
        
        self.assertIsInstance(comunidades, list)
        # Cada comunidad debe ser una lista de usuarios
        if len(comunidades) > 0:
            self.assertIsInstance(comunidades[0], list)
    
    def test_estadisticas_completas(self):
        """Prueba obtener estadísticas completas."""
        stats = self.gestor.obtener_estadisticas_grafo()
        
        # Verificar que tenga todas las secciones esperadas
        self.assertIn('interacciones', stats)
        self.assertIn('grafo_usuarios', stats)
        self.assertIn('grafo_libros', stats)
        self.assertIn('comunidades', stats)


def ejecutar_pruebas_grafos():
    """
    Ejecuta todas las pruebas de grafos y retorna el resultado.
    
    Returns:
        True si todas las pruebas pasan, False en caso contrario
    """
    print("=" * 70)
    print("EJECUTANDO PRUEBAS DE ESTRUCTURAS DE GRAFOS")
    print("=" * 70)
    print()
    
    # Crear suite de pruebas
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Agregar todas las clases de prueba
    suite.addTests(loader.loadTestsFromTestCase(TestGrafoBasico))
    suite.addTests(loader.loadTestsFromTestCase(TestAlgoritmosBFS_DFS))
    suite.addTests(loader.loadTestsFromTestCase(TestDijkstra))
    suite.addTests(loader.loadTestsFromTestCase(TestGrafoConexo))
    suite.addTests(loader.loadTestsFromTestCase(TestGrafoBipartito))
    suite.addTests(loader.loadTestsFromTestCase(TestGestorGrafoBiblioteca))
    
    # Ejecutar pruebas
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Resumen
    print("\n" + "=" * 70)
    print("RESUMEN DE PRUEBAS - GRAFOS")
    print("=" * 70)
    print(f"Pruebas ejecutadas: {result.testsRun}")
    print(f"Exitosas: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Fallidas: {len(result.failures)}")
    print(f"Errores: {len(result.errors)}")
    
    if result.wasSuccessful():
        print("\n🎉 TODAS LAS PRUEBAS DE GRAFOS PASARON EXITOSAMENTE")
        return True
    else:
        print("\n❌ ALGUNAS PRUEBAS FALLARON")
        return False


if __name__ == "__main__":
    print("SISTEMA DE PRUEBAS - GRAFOS")
    print("Curso: Estructuras de Datos - Unidad 2")
    print("Implementación de Grafos para Sistema de Biblioteca\n")
    
    exito = ejecutar_pruebas_grafos()
    
    if not exito:
        sys.exit(1)
