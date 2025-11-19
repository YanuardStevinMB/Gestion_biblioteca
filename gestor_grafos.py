"""
Gestor de Grafos para Sistema de Biblioteca
==========================================

Este módulo integra las estructuras de grafos con el sistema de gestión
de biblioteca existente, proporcionando funcionalidades de:

- Sistema de recomendaciones basado en grafos
- Análisis de interacciones usuario-libro
- Detección de comunidades de lectores
- Análisis de popularidad y tendencias

Autor: Sistema de Biblioteca Virtual
Fecha: 2024  
Curso: Estructuras de Datos - Unidad 2 (Grafos)
"""

from estructuras_grafos import Grafo, GrafoBipartito
from datetime import datetime
from typing import List, Dict, Tuple, Optional


class GestorGrafoBiblioteca:
    """
    Gestor principal que integra grafos con el sistema de biblioteca.
    
    Mantiene diferentes grafos para optimizar distintos casos de uso:
    - Grafo bipartito usuario-libro
    - Grafo de usuarios similares
    - Grafo de libros relacionados
    """
    
    def __init__(self, biblioteca_manager):
        """
        Inicializa el gestor de grafos.
        
        Args:
            biblioteca_manager: Instancia del BibliotecaManager existente
        """
        self.biblioteca = biblioteca_manager
        
        # Grafo bipartito principal: Usuario <-> Libro
        self.grafo_interacciones = GrafoBipartito(ponderado=True)
        
        # Grafo de usuarios (basado en similitud de lecturas)
        self.grafo_usuarios = Grafo(dirigido=False, ponderado=True)
        
        # Grafo de libros relacionados (basado en co-lecturas)
        self.grafo_libros = Grafo(dirigido=False, ponderado=True)
        
        # Estadísticas
        self.num_interacciones = 0
        self.ultima_actualizacion = None
        
        # Inicializar con datos existentes
        self._inicializar_desde_prestamos()
    
    def _inicializar_desde_prestamos(self):
        """
        Inicializa los grafos con los préstamos existentes en el sistema.
        """
        # Obtener todos los préstamos del historial
        try:
            historial = self.biblioteca.historial_prestamos.obtener_todos()
        except:
            historial = []
        
        # Registrar cada interacción en los grafos
        for prestamo in historial:
            self.registrar_interaccion(
                prestamo.id_usuario,
                prestamo.isbn_libro,
                peso=1
            )
        
        # También registrar préstamos activos
        prestamos_activos = self.biblioteca.obtener_prestamos_activos()
        for prestamo in prestamos_activos:
            self.registrar_interaccion(
                prestamo.id_usuario,
                prestamo.isbn_libro,
                peso=1
            )
        
        self.ultima_actualizacion = datetime.now()
    
    def registrar_interaccion(self, usuario_id, libro_id, peso=1):
        """
        Registra una interacción usuario-libro (préstamo).
        
        Esta operación actualiza múltiples grafos:
        1. Grafo bipartito usuario-libro
        2. Grafo de usuarios similares
        3. Grafo de libros relacionados
        
        Args:
            usuario_id: ID del usuario
            libro_id: ID/ISBN del libro
            peso: Peso de la interacción (por defecto 1)
        """
        # Actualizar grafo bipartito
        self.grafo_interacciones.agregar_interaccion(usuario_id, libro_id, peso)
        
        # Actualizar grafo de usuarios (conectar con usuarios que leyeron el mismo libro)
        usuarios_libro = self.grafo_interacciones.obtener_usuarios_de_libro(libro_id)
        for otro_usuario, _ in usuarios_libro:
            if otro_usuario != usuario_id:
                self._conectar_usuarios_similares(usuario_id, otro_usuario)
        
        # Actualizar grafo de libros (conectar libros leídos por el mismo usuario)
        libros_usuario = self.grafo_interacciones.obtener_libros_de_usuario(usuario_id)
        for otro_libro, _ in libros_usuario:
            if otro_libro != libro_id:
                self._conectar_libros_relacionados(libro_id, otro_libro)
        
        self.num_interacciones += 1
        self.ultima_actualizacion = datetime.now()
    
    def _conectar_usuarios_similares(self, usuario1, usuario2):
        """
        Conecta dos usuarios en el grafo de usuarios similares.
        El peso representa el número de libros en común.
        """
        peso_actual = self.grafo_usuarios.obtener_peso_arista(usuario1, usuario2) or 0
        if peso_actual > 0:
            self.grafo_usuarios.eliminar_arista(usuario1, usuario2)
        self.grafo_usuarios.agregar_arista(usuario1, usuario2, peso_actual + 1)
    
    def _conectar_libros_relacionados(self, libro1, libro2):
        """
        Conecta dos libros en el grafo de libros relacionados.
        El peso representa el número de usuarios que leyeron ambos.
        """
        peso_actual = self.grafo_libros.obtener_peso_arista(libro1, libro2) or 0
        if peso_actual > 0:
            self.grafo_libros.eliminar_arista(libro1, libro2)
        self.grafo_libros.agregar_arista(libro1, libro2, peso_actual + 1)
    
    # ========================================================================
    # SISTEMA DE RECOMENDACIONES
    # ========================================================================
    
    def recomendar_libros_usuario(self, usuario_id, top_n=5, excluir_leidos=True):
        """
        Recomienda libros a un usuario basado en el grafo de interacciones.
        
        Algoritmo de Filtrado Colaborativo:
        1. Encuentra usuarios similares (que leyeron libros en común)
        2. Obtiene libros que esos usuarios leyeron
        3. Rankea por popularidad entre usuarios similares
        
        Args:
            usuario_id: ID del usuario
            top_n: Número de recomendaciones a retornar
            excluir_leidos: Si True, excluye libros ya leídos por el usuario
            
        Returns:
            Lista de diccionarios con información de libros recomendados
        """
        # Usar el grafo bipartito para recomendaciones
        recomendaciones_raw = self.grafo_interacciones.recomendar_libros(
            usuario_id, 
            top_n=top_n * 2  # Pedir más para poder filtrar
        )
        
        resultados = []
        for libro_id, score in recomendaciones_raw:
            # Obtener información del libro
            libro = self.biblioteca.obtener_libro_por_isbn(libro_id)
            if libro:
                resultados.append({
                    'libro': libro,
                    'score': score,
                    'razon': f'Recomendado por {int(score)} usuarios similares'
                })
                
                if len(resultados) >= top_n:
                    break
        
        return resultados
    
    def recomendar_libros_similares(self, libro_id, top_n=5):
        """
        Recomienda libros similares a uno dado.
        
        Usa el grafo de libros relacionados (basado en co-lecturas).
        
        Args:
            libro_id: ID/ISBN del libro de referencia
            top_n: Número de recomendaciones
            
        Returns:
            Lista de diccionarios con libros similares
        """
        if libro_id not in self.grafo_libros.vertices:
            return []
        
        # Obtener vecinos en el grafo de libros
        vecinos = self.grafo_libros.obtener_vecinos(libro_id)
        
        # Ordenar por peso (más co-lecturas = más similar)
        vecinos_ordenados = sorted(vecinos, key=lambda x: x[1], reverse=True)
        
        resultados = []
        for otro_libro_id, peso in vecinos_ordenados[:top_n]:
            libro = self.biblioteca.obtener_libro_por_isbn(otro_libro_id)
            if libro:
                resultados.append({
                    'libro': libro,
                    'score': peso,
                    'razon': f'{int(peso)} usuarios leyeron ambos libros'
                })
        
        return resultados
    
    def usuarios_similares(self, usuario_id, top_n=5):
        """
        Encuentra usuarios con gustos similares.
        
        Args:
            usuario_id: ID del usuario
            top_n: Número de usuarios similares a retornar
                            
        Returns:
            Lista de tuplas (usuario, score)
        """
        if usuario_id not in self.grafo_usuarios.vertices:
            return []
        
        # Obtener vecinos del grafo de usuarios
        vecinos = self.grafo_usuarios.obtener_vecinos(usuario_id)
        
        # Ordenar por peso (más libros en común)
        vecinos_ordenados = sorted(vecinos, key=lambda x: x[1], reverse=True)
        
        return vecinos_ordenados[:top_n]
    
    # ========================================================================
    # ANÁLISIS Y MÉTRICAS
    # ========================================================================
    
    def obtener_libros_populares(self, top_n=10, categoria=None):
        """
        Obtiene los libros más populares según el grafo de interacciones.
        
        Args:
            top_n: Número de libros a retornar
            categoria: Filtrar por categoría (opcional)
            
        Returns:
            Lista de diccionarios con libros populares
        """
        populares = self.grafo_interacciones.obtener_libros_populares(top_n=top_n * 2)
        
        resultados = []
        for libro_id, num_prestamos in populares:
            libro = self.biblioteca.obtener_libro_por_isbn(libro_id)
            if libro:
                # Filtrar por categoría si se especifica
                if categoria and libro.categoria.lower() != categoria.lower():
                    continue
                
                resultados.append({
                    'libro': libro,
                    'num_prestamos': int(num_prestamos),
                    'score_popularidad': num_prestamos
                })
                
                if len(resultados) >= top_n:
                    break
        
        return resultados
    
    def obtener_usuarios_activos(self, top_n=10):
        """
        Obtiene los usuarios más activos (más libros prestados).
        
        Returns:
            Lista de tuplas (usuario_id, num_libros)
        """
        usuarios_activos = []
        
        for usuario_id in self.grafo_interacciones.conjunto_a:
            libros = self.grafo_interacciones.obtener_libros_de_usuario(usuario_id)
            total_prestamos = sum(peso for _, peso in libros)
            usuarios_activos.append((usuario_id, int(total_prestamos)))
        
        usuarios_activos.sort(key=lambda x: x[1], reverse=True)
        return usuarios_activos[:top_n]
    
    def detectar_comunidades_lectores(self):
        """
        Detecta comunidades de lectores con intereses similares.
        
        Usa el algoritmo de componentes conexas en el grafo de usuarios.
        
        Returns:
            Lista de comunidades (cada comunidad es una lista de usuario_ids)
        """
        return self.grafo_interacciones.detectar_comunidades_usuarios()
    
    def analizar_tendencias_categoria(self):
        """
        Analiza tendencias de préstamos por categoría.
        
        Returns:
            Diccionario con categorías y número de préstamos
        """
        tendencias = {}
        
        for libro_id in self.grafo_interacciones.conjunto_b:
            libro = self.biblioteca.obtener_libro_por_isbn(libro_id)
            if libro:
                categoria = libro.categoria
                usuarios = self.grafo_interacciones.obtener_usuarios_de_libro(libro_id)
                total = sum(peso for _, peso in usuarios)
                
                tendencias[categoria] = tendencias.get(categoria, 0) + total
        
        # Ordenar por popularidad
        return dict(sorted(tendencias.items(), key=lambda x: x[1], reverse=True))
    
    def camino_entre_usuarios(self, usuario1_id, usuario2_id):
        """
        Encuentra el camino de conexión entre dos usuarios en el grafo social.
        
        Usa BFS para encontrar el camino más corto.
        
        Args:
            usuario1_id: ID del primer usuario
            usuario2_id: ID del segundo usuario
            
        Returns:
            Lista de usuarios que conectan a ambos, o None si no hay conexión
        """
        return self.grafo_usuarios.camino_mas_corto_bfs(usuario1_id, usuario2_id)
    
    def distancia_entre_libros(self, libro1_id, libro2_id):
        """
        Calcula la "distancia" entre dos libros en términos de co-lecturas.
        
        Args:
            libro1_id: ID del primer libro
            libro2_id: ID del segundo libro
            
        Returns:
            Distancia (menor es más similar), o None si no hay conexión
        """
        if not self.grafo_libros.ponderado:
            camino = self.grafo_libros.camino_mas_corto_bfs(libro1_id, libro2_id)
            return len(camino) - 1 if camino else None
        
        # Para grafos ponderados, usar Dijkstra (invertir pesos para que mayor peso = menor distancia)
        # Crear grafo temporal con pesos invertidos
        grafo_temp = Grafo(dirigido=False, ponderado=True)
        for libro in self.grafo_libros.vertices:
            for otro_libro, peso in self.grafo_libros.obtener_vecinos(libro):
                # Invertir: a mayor co-lecturas, menor distancia
                distancia = 1.0 / peso if peso > 0 else float('inf')
                grafo_temp.agregar_arista(libro, otro_libro, distancia)
        
        distancias, _ = grafo_temp.dijkstra(libro1_id)
        return distancias.get(libro2_id)
    
    # ========================================================================
    # ESTADÍSTICAS DEL GRAFO
    # ========================================================================
    
    def obtener_estadisticas_grafo(self):
        """
        Obtiene estadísticas completas de todos los grafos.
        
        Returns:
            Diccionario con estadísticas detalladas
        """
        stats_interacciones = self.grafo_interacciones.obtener_estadisticas()
        stats_usuarios = self.grafo_usuarios.obtener_estadisticas()
        stats_libros = self.grafo_libros.obtener_estadisticas()
        
        # Comunidades
        comunidades = self.detectar_comunidades_lectores()
        
        return {
            'interacciones': {
                'total_usuarios': len(self.grafo_interacciones.conjunto_a),
                'total_libros': len(self.grafo_interacciones.conjunto_b),
                'total_interacciones': self.num_interacciones,
                'densidad': stats_interacciones['densidad']
            },
            'grafo_usuarios': {
                'num_conexiones': stats_usuarios['num_aristas'],
                'conexiones_promedio': stats_usuarios['grado_promedio'],
                'usuario_mas_conectado': stats_usuarios['grado_maximo'],
                'es_conexo': stats_usuarios['es_conexo']
            },
            'grafo_libros': {
                'num_relaciones': stats_libros['num_aristas'],
                'relaciones_promedio': stats_libros['grado_promedio'],
                'libro_mas_relacionado': stats_libros['grado_maximo']
            },
            'comunidades': {
                'num_comunidades': len(comunidades),
                'tamaño_promedio': sum(len(c) for c in comunidades) / len(comunidades) if comunidades else 0,
                'mayor_comunidad': max(len(c) for c in comunidades) if comunidades else 0
            },
            'ultima_actualizacion': self.ultima_actualizacion.strftime('%Y-%m-%d %H:%M:%S') if self.ultima_actualizacion else 'N/A'
        }
    
    def imprimir_estadisticas(self):
        """Imprime las estadísticas de forma legible."""
        stats = self.obtener_estadisticas_grafo()
        
        print("=" * 70)
        print("ESTADÍSTICAS DEL SISTEMA DE GRAFOS")
        print("=" * 70)
        
        print("\n📊 GRAFO DE INTERACCIONES (Usuario-Libro):")
        print(f"  • Total usuarios: {stats['interacciones']['total_usuarios']}")
        print(f"  • Total libros: {stats['interacciones']['total_libros']}")
        print(f"  • Total interacciones: {stats['interacciones']['total_interacciones']}")
        print(f"  • Densidad: {stats['interacciones']['densidad']:.4f}")
        
        print("\n👥 GRAFO DE USUARIOS (Red Social de Lectores):")
        print(f"  • Conexiones entre usuarios: {stats['grafo_usuarios']['num_conexiones']}")
        print(f"  • Conexiones promedio: {stats['grafo_usuarios']['conexiones_promedio']:.2f}")
        print(f"  • Usuario más conectado: {stats['grafo_usuarios']['usuario_mas_conectado']} conexiones")
        print(f"  • Red conexa: {'Sí' if stats['grafo_usuarios']['es_conexo'] else 'No'}")
        
        print("\n📚 GRAFO DE LIBROS (Libros Relacionados):")
        print(f"  • Relaciones entre libros: {stats['grafo_libros']['num_relaciones']}")
        print(f"  • Relaciones promedio: {stats['grafo_libros']['relaciones_promedio']:.2f}")
        print(f"  • Libro más relacionado: {stats['grafo_libros']['libro_mas_relacionado']} relaciones")
        
        print("\n🏘️  COMUNIDADES DE LECTORES:")
        print(f"  • Número de comunidades: {stats['comunidades']['num_comunidades']}")
        print(f"  • Tamaño promedio: {stats['comunidades']['tamaño_promedio']:.1f} usuarios")
        print(f"  • Mayor comunidad: {stats['comunidades']['mayor_comunidad']} usuarios")
        
        print(f"\n⏰ Última actualización: {stats['ultima_actualizacion']}")
        print("=" * 70)
    
    def generar_reporte_recomendaciones(self, usuario_id):
        """
        Genera un reporte completo de recomendaciones para un usuario.
        
        Args:
            usuario_id: ID del usuario
            
        Returns:
            Diccionario con todas las recomendaciones y análisis
        """
        usuario = self.biblioteca.obtener_usuario_por_id(usuario_id)
        if not usuario:
            return None
        
        # Recomendaciones de libros
        recomendaciones = self.recomendar_libros_usuario(usuario_id, top_n=5)
        
        # Usuarios similares
        similares = self.usuarios_similares(usuario_id, top_n=5)
        
        # Libros leídos
        libros_leidos = self.grafo_interacciones.obtener_libros_de_usuario(usuario_id)
        
        # Estadísticas personales
        num_conexiones = self.grafo_usuarios.obtener_grado(usuario_id)
        
        return {
            'usuario': usuario,
            'libros_leidos': len(libros_leidos),
            'total_prestamos': sum(peso for _, peso in libros_leidos),
            'conexiones_sociales': num_conexiones,
            'recomendaciones': recomendaciones,
            'usuarios_similares': similares
        }
