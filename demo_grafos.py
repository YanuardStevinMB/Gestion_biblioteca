"""
Script de Demostración del Sistema de Grafos
===========================================

Este script demuestra todas las funcionalidades implementadas
en la Fase 3 del proyecto de biblioteca.

Autor: Sistema de Biblioteca Virtual
Fecha: 2024
Curso: Estructuras de Datos - Unidad 2 (Grafos)
"""

import sys
import os

# Agregar el directorio actual al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from modelos import BibliotecaManager
from gestor_grafos import GestorGrafoBiblioteca


def imprimir_seccion(titulo):
    """Imprime un título de sección formateado."""
    print("\n" + "="*70)
    print(f"{titulo}")
    print("="*70)


def demostrar_sistema_completo():
    """Demostración completa del sistema de grafos."""
    
    print("="*70)
    print("     DEMOSTRACIÓN DEL SISTEMA DE GRAFOS")
    print("     Sistema de Gestión de Biblioteca - Fase 3")
    print("="*70)
    
    # 1. Inicializar sistema
    print("\n🔧 Inicializando sistema...")
    biblioteca = BibliotecaManager()
    gestor = GestorGrafoBiblioteca(biblioteca)
    print("✅ Sistema inicializado correctamente")
    
    # 2. Mostrar estadísticas iniciales
    imprimir_seccion("📊 ESTADÍSTICAS DEL SISTEMA DE GRAFOS")
    gestor.imprimir_estadisticas()
    
    # 3. Demostrar recomendaciones para un usuario
    imprimir_seccion("🎯 SISTEMA DE RECOMENDACIONES")
    
    usuario_id = "U001"
    usuario = biblioteca.obtener_usuario_por_id(usuario_id)
    
    if usuario:
        print(f"\nUsuario: {usuario.nombre} ({usuario_id})")
        print(f"Email: {usuario.email}")
        
        # Mostrar libros que ha leído
        libros_leidos = gestor.grafo_interacciones.obtener_libros_de_usuario(usuario_id)
        print(f"\n📚 Libros leídos: {len(libros_leidos)}")
        for libro_id, veces in list(libros_leidos)[:3]:
            libro = biblioteca.obtener_libro_por_isbn(libro_id)
            if libro:
                print(f"  • {libro.titulo} ({int(veces)} veces)")
        
        # Obtener recomendaciones
        print("\n💡 RECOMENDACIONES PERSONALIZADAS:")
        recomendaciones = gestor.recomendar_libros_usuario(usuario_id, top_n=5)
        
        if recomendaciones:
            for i, rec in enumerate(recomendaciones, 1):
                print(f"\n{i}. 📖 {rec['libro'].titulo}")
                print(f"   Autor: {rec['libro'].autor}")
                print(f"   Categoría: {rec['libro'].categoria}")
                print(f"   {rec['razon']}")
        else:
            print("  No hay suficientes datos para generar recomendaciones.")
    
    # 4. Usuarios similares
    imprimir_seccion("👥 ANÁLISIS DE USUARIOS SIMILARES")
    
    print(f"\nUsuarios con gustos similares a {usuario.nombre}:")
    similares = gestor.usuarios_similares(usuario_id, top_n=5)
    
    if similares:
        for otro_id, libros_comunes in similares:
            otro_usuario = biblioteca.obtener_usuario_por_id(otro_id)
            if otro_usuario:
                print(f"\n  • {otro_usuario.nombre}")
                print(f"    Email: {otro_usuario.email}")
                print(f"    Libros en común: {int(libros_comunes)}")
    else:
        print("  No se encontraron usuarios similares.")
    
    # 5. Libros más populares
    imprimir_seccion("📈 TOP 10 LIBROS MÁS POPULARES")
    
    populares = gestor.obtener_libros_populares(top_n=10)
    
    print("\nRanking de libros por número de préstamos:\n")
    for i, libro_info in enumerate(populares, 1):
        libro = libro_info['libro']
        num_prestamos = libro_info['num_prestamos']
        print(f"{i:2d}. {libro.titulo}")
        print(f"    Autor: {libro.autor}")
        print(f"    Categoría: {libro.categoria}")
        print(f"    Total de préstamos: {num_prestamos}")
        print()
    
    # 6. Usuarios más activos
    imprimir_seccion("🏆 USUARIOS MÁS ACTIVOS")
    
    activos = gestor.obtener_usuarios_activos(top_n=10)
    
    print("\nUsuarios con más préstamos:\n")
    for i, (user_id, num_prestamos) in enumerate(activos, 1):
        user = biblioteca.obtener_usuario_por_id(user_id)
        if user:
            print(f"{i:2d}. {user.nombre}")
            print(f"    Total de préstamos: {num_prestamos}")
            print()
    
    # 7. Comunidades de lectores
    imprimir_seccion("🏘️  COMUNIDADES DE LECTORES")
    
    comunidades = gestor.detectar_comunidades_lectores()
    
    print(f"\nSe detectaron {len(comunidades)} comunidad(es) de lectores:\n")
    
    for i, comunidad in enumerate(comunidades, 1):
        print(f"Comunidad #{i}: {len(comunidad)} usuarios")
        
        # Mostrar algunos usuarios de la comunidad
        for user_id in list(comunidad)[:3]:
            user = biblioteca.obtener_usuario_por_id(user_id)
            if user:
                print(f"  • {user.nombre}")
        
        if len(comunidad) > 3:
            print(f"  ... y {len(comunidad) - 3} más")
        print()
    
    # 8. Tendencias por categoría
    imprimir_seccion("📊 TENDENCIAS POR CATEGORÍA")
    
    tendencias = gestor.analizar_tendencias_categoria()
    
    print("\nCategorías ordenadas por número de préstamos:\n")
    for i, (categoria, num_prestamos) in enumerate(list(tendencias.items())[:10], 1):
        print(f"{i:2d}. {categoria}: {int(num_prestamos)} préstamos")
    
    # 9. Libros relacionados (ejemplo con un libro específico)
    imprimir_seccion("🔗 LIBROS RELACIONADOS")
    
    # Tomar el libro más popular como ejemplo
    if populares:
        libro_ejemplo = populares[0]['libro']
        print(f"\nLibros relacionados con '{libro_ejemplo.titulo}':")
        
        relacionados = gestor.recomendar_libros_similares(libro_ejemplo.isbn, top_n=5)
        
        if relacionados:
            for i, rel in enumerate(relacionados, 1):
                print(f"\n{i}. {rel['libro'].titulo}")
                print(f"   Autor: {rel['libro'].autor}")
                print(f"   {rel['razon']}")
        else:
            print("  No se encontraron libros relacionados.")
    
    # 10. Reporte completo para un usuario
    imprimir_seccion("📋 REPORTE COMPLETO DE USUARIO")
    
    reporte = gestor.generar_reporte_recomendaciones(usuario_id)
    
    if reporte:
        print(f"\nREPORTE PERSONALIZADO PARA: {reporte['usuario'].nombre}")
        print(f"\n  📚 Libros leídos: {reporte['libros_leidos']}")
        print(f"  📖 Total de préstamos: {reporte['total_prestamos']}")
        print(f"  👥 Conexiones sociales: {reporte['conexiones_sociales']}")
        
        print("\n  💡 Top 3 Recomendaciones:")
        for i, rec in enumerate(reporte['recomendaciones'][:3], 1):
            print(f"    {i}. {rec['libro'].titulo}")
        
        print("\n  👤 Usuarios similares:")
        for otro_id, score in reporte['usuarios_similares'][:3]:
            otro = biblioteca.obtener_usuario_por_id(otro_id)
            if otro:
                print(f"    • {otro.nombre} ({int(score)} libros en común)")
    
    # Resumen final
    imprimir_seccion("✅ DEMOSTRACIÓN COMPLETADA")
    
    print("\nEl sistema de grafos ha sido implementado exitosamente con:")
    print("  ✓ Grafo bipartito Usuario-Libro")
    print("  ✓ Grafo de usuarios similares")
    print("  ✓ Grafo de libros relacionados")
    print("  ✓ Algoritmos de recorrido (BFS, DFS)")
    print("  ✓ Algoritmo de Dijkstra")
    print("  ✓ Sistema de recomendaciones")
    print("  ✓ Detección de comunidades")
    print("  ✓ Análisis de tendencias")
    print("\n" + "="*70)


def demostrar_algoritmos_basicos():
    """Demuestra los algoritmos básicos de grafos."""
    
    from estructuras_grafos import Grafo
    
    imprimir_seccion("🧮 DEMOSTRACIÓN DE ALGORITMOS BÁSICOS")
    
    # Crear un grafo de ejemplo
    print("\nCreando grafo de ejemplo (red social)...")
    grafo = Grafo(dirigido=False, ponderado=False)
    
    # Agregar conexiones
    conexiones = [
        ("Alice", "Bob"),
        ("Alice", "Carol"),
        ("Bob", "David"),
        ("Carol", "David"),
        ("David", "Eve"),
        ("Eve", "Frank")
    ]
    
    for origen, destino in conexiones:
        grafo.agregar_arista(origen, destino)
    
    print("✅ Grafo creado con 6 personas y 6 conexiones")
    
    # BFS
    print("\n1️⃣ ALGORITMO BFS (Breadth-First Search):")
    print("   Recorrido desde 'Alice':")
    recorrido_bfs = grafo.bfs("Alice")
    print(f"   {' → '.join(recorrido_bfs)}")
    
    # DFS
    print("\n2️⃣ ALGORITMO DFS (Depth-First Search):")
    print("   Recorrido desde 'Alice':")
    recorrido_dfs = grafo.dfs("Alice")
    print(f"   {' → '.join(recorrido_dfs)}")
    
    # Camino más corto
    print("\n3️⃣ CAMINO MÁS CORTO (BFS):")
    print("   De 'Alice' a 'Frank':")
    camino = grafo.camino_mas_corto_bfs("Alice", "Frank")
    if camino:
        print(f"   {' → '.join(camino)}")
        print(f"   Distancia: {len(camino) - 1} pasos")
    
    # Componentes conexas
    print("\n4️⃣ COMPONENTES CONEXAS:")
    componentes = grafo.obtener_componentes_conexas()
    print(f"   El grafo tiene {len(componentes)} componente(s)")
    for i, comp in enumerate(componentes, 1):
        print(f"   Componente {i}: {', '.join(comp)}")
    
    # Estadísticas
    print("\n5️⃣ ESTADÍSTICAS DEL GRAFO:")
    stats = grafo.obtener_estadisticas()
    print(f"   Vértices: {stats['num_vertices']}")
    print(f"   Aristas: {stats['num_aristas']}")
    print(f"   Grado promedio: {stats['grado_promedio']:.2f}")
    print(f"   Densidad: {stats['densidad']:.2%}")
    print(f"   Es conexo: {'Sí' if stats['es_conexo'] else 'No'}")


def demostrar_dijkstra():
    """Demuestra el algoritmo de Dijkstra."""
    
    from estructuras_grafos import Grafo
    
    imprimir_seccion("🛣️  ALGORITMO DE DIJKSTRA (CAMINOS MÍNIMOS)")
    
    print("\nCreando mapa de ciudades con distancias...")
    mapa = Grafo(dirigido=False, ponderado=True)
    
    # Agregar rutas con kilómetros
    rutas = [
        ("Madrid", "Barcelona", 620),
        ("Madrid", "Valencia", 350),
        ("Madrid", "Sevilla", 530),
        ("Barcelona", "Valencia", 350),
        ("Barcelona", "Zaragoza", 300),
        ("Valencia", "Sevilla", 650),
        ("Sevilla", "Lisboa", 400)
    ]
    
    for origen, destino, km in rutas:
        mapa.agregar_arista(origen, destino, km)
    
    print("✅ Mapa creado")
    
    # Ejecutar Dijkstra desde Madrid
    origen = "Madrid"
    print(f"\nCalculando distancias mínimas desde {origen}...\n")
    
    distancias, padres = mapa.dijkstra(origen)
    
    # Mostrar distancias
    print("Distancias mínimas:")
    for ciudad in sorted(distancias.keys()):
        if ciudad != origen:
            dist = distancias[ciudad]
            if dist < float('inf'):
                print(f"  {origen} → {ciudad}: {dist} km")
                
                # Reconstruir camino
                camino = mapa.reconstruir_camino_dijkstra(origen, ciudad, padres)
                if camino:
                    print(f"    Ruta: {' → '.join(camino)}")


def menu_principal():
    """Menú principal de demostración."""
    
    while True:
        print("\n" + "="*70)
        print("MENÚ DE DEMOSTRACIÓN - SISTEMA DE GRAFOS")
        print("="*70)
        print("\n1. Demostración completa del sistema")
        print("2. Demostración de algoritmos básicos (BFS, DFS)")
        print("3. Demostración de Dijkstra")
        print("4. Ejecutar todas las demostraciones")
        print("0. Salir")
        
        try:
            opcion = input("\nSeleccione una opción: ").strip()
            
            if opcion == "0":
                print("\n¡Gracias por usar el sistema de demostración!")
                break
            
            elif opcion == "1":
                demostrar_sistema_completo()
                input("\nPresione Enter para continuar...")
            
            elif opcion == "2":
                demostrar_algoritmos_basicos()
                input("\nPresione Enter para continuar...")
            
            elif opcion == "3":
                demostrar_dijkstra()
                input("\nPresione Enter para continuar...")
            
            elif opcion == "4":
                demostrar_algoritmos_basicos()
                input("\nPresione Enter para continuar...")
                demostrar_dijkstra()
                input("\nPresione Enter para continuar...")
                demostrar_sistema_completo()
                input("\nPresione Enter para continuar...")
            
            else:
                print("\n❌ Opción inválida. Por favor, intente nuevamente.")
        
        except KeyboardInterrupt:
            print("\n\n¡Hasta luego!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")


if __name__ == "__main__":
    print("=" * 70)
    print("SISTEMA DE DEMOSTRACIÓN - GRAFOS")
    print("Curso: Estructuras de Datos - Unidad 2")
    print("Implementación de Grafos para Sistema de Biblioteca")
    print("=" * 70)
    
    menu_principal()
