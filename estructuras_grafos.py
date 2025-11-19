"""
Estructuras de Grafos para Sistema de Gestión de Biblioteca
===========================================================

Este módulo contiene las implementaciones de grafos utilizadas para modelar
y optimizar las interacciones entre usuarios y libros en el sistema bibliotecario.

Implementaciones:
- Grafo (dirigido y no dirigido)
- Grafo Ponderado
- Algoritmos de recorrido (BFS, DFS)
- Algoritmos de caminos (Dijkstra, Floyd-Warshall)
- Detección de comunidades

Autor: Sistema de Biblioteca Virtual
Fecha: 2024
Curso: Estructuras de Datos - Unidad 2 (Grafos)
"""

from collections import deque, defaultdict
import heapq
from typing import List, Dict, Set, Tuple, Optional, Any


# ============================================================================
# GRAFO GENERAL (BASE)
# ============================================================================

class Grafo:
    """
    Implementación de un Grafo general.
    
    Características:
    - Soporta grafos dirigidos y no dirigidos
    - Soporta grafos ponderados y no ponderados
    - Usa lista de adyacencia para representación eficiente
    
    Atributos:
        dirigido: Si el grafo es dirigido o no
        ponderado: Si las aristas tienen peso
        vertices: Conjunto de todos los vértices
        adyacencias: Diccionario de listas de adyacencia
    """
    
    def __init__(self, dirigido=False, ponderado=False):
        """
        Inicializa un grafo vacío.
        
        Args:
            dirigido: True para grafo dirigido, False para no dirigido
            ponderado: True si las aristas tienen peso
        """
        self.dirigido = dirigido
        self.ponderado = ponderado
        self.vertices = set()
        # adyacencias[u] = [(v, peso), ...] si es ponderado
        # adyacencias[u] = [v, ...] si no es ponderado
        self.adyacencias = defaultdict(list)
        self.num_aristas = 0
    
    def agregar_vertice(self, vertice):
        """
        Agrega un vértice al grafo.
        
        Args:
            vertice: Identificador del vértice (puede ser cualquier tipo hashable)
        """
        if vertice not in self.vertices:
            self.vertices.add(vertice)
            if vertice not in self.adyacencias:
                self.adyacencias[vertice] = []
    
    def agregar_arista(self, origen, destino, peso=1):
        """
        Agrega una arista entre dos vértices.
        
        Args:
            origen: Vértice de origen
            destino: Vértice de destino
            peso: Peso de la arista (solo para grafos ponderados)
        """
        # Agregar vértices si no existen
        self.agregar_vertice(origen)
        self.agregar_vertice(destino)
        
        if self.ponderado:
            # Evitar duplicados
            if not any(v == destino for v, _ in self.adyacencias[origen]):
                self.adyacencias[origen].append((destino, peso))
                self.num_aristas += 1
                
            # Si no es dirigido, agregar arista inversa
            if not self.dirigido:
                if not any(v == origen for v, _ in self.adyacencias[destino]):
                    self.adyacencias[destino].append((origen, peso))
        else:
            # Grafo no ponderado
            if destino not in self.adyacencias[origen]:
                self.adyacencias[origen].append(destino)
                self.num_aristas += 1
                
            if not self.dirigido and origen not in self.adyacencias[destino]:
                self.adyacencias[destino].append(origen)
    
    def eliminar_arista(self, origen, destino):
        """
        Elimina una arista entre dos vértices.
        
        Args:
            origen: Vértice de origen
            destino: Vértice de destino
            
        Returns:
            True si se eliminó la arista, False si no existía
        """
        if origen not in self.vertices or destino not in self.vertices:
            return False
        
        eliminado = False
        
        if self.ponderado:
            # Grafo ponderado
            self.adyacencias[origen] = [(v, p) for v, p in self.adyacencias[origen] if v != destino]
            if not self.dirigido:
                self.adyacencias[destino] = [(v, p) for v, p in self.adyacencias[destino] if v != origen]
            eliminado = True
        else:
            # Grafo no ponderado
            if destino in self.adyacencias[origen]:
                self.adyacencias[origen].remove(destino)
                eliminado = True
            if not self.dirigido and origen in self.adyacencias[destino]:
                self.adyacencias[destino].remove(origen)
        
        if eliminado:
            self.num_aristas -= 1
        
        return eliminado
    
    def obtener_vecinos(self, vertice):
        """
        Obtiene los vecinos de un vértice.
        
        Args:
            vertice: Vértice del cual obtener vecinos
            
        Returns:
            Lista de vecinos (o tuplas (vecino, peso) si es ponderado)
        """
        if vertice not in self.vertices:
            return []
        return self.adyacencias[vertice]
    
    def tiene_arista(self, origen, destino):
        """
        Verifica si existe una arista entre dos vértices.
        
        Args:
            origen: Vértice de origen
            destino: Vértice de destino
            
        Returns:
            True si existe la arista, False en caso contrario
        """
        if origen not in self.vertices or destino not in self.vertices:
            return False
        
        if self.ponderado:
            return any(v == destino for v, _ in self.adyacencias[origen])
        else:
            return destino in self.adyacencias[origen]
    
    def obtener_peso_arista(self, origen, destino):
        """
        Obtiene el peso de una arista (solo para grafos ponderados).
        
        Args:
            origen: Vértice de origen
            destino: Vértice de destino
            
        Returns:
            Peso de la arista o None si no existe
        """
        if not self.ponderado:
            return 1 if self.tiene_arista(origen, destino) else None
        
        for v, peso in self.adyacencias[origen]:
            if v == destino:
                return peso
        return None
    
    def obtener_grado(self, vertice):
        """
        Obtiene el grado de un vértice.
        
        Args:
            vertice: Vértice del cual calcular el grado
            
        Returns:
            Grado del vértice (número de aristas conectadas)
        """
        if vertice not in self.vertices:
            return 0
        return len(self.adyacencias[vertice])
    
    def es_conexo(self):
        """
        Verifica si el grafo es conexo (todos los vértices son alcanzables).
        
        Returns:
            True si el grafo es conexo, False en caso contrario
        """
        if not self.vertices:
            return True
        
        # Realizar BFS desde un vértice arbitrario
        inicio = next(iter(self.vertices))
        visitados = self.bfs(inicio)
        
        return len(visitados) == len(self.vertices)
    
    # ========================================================================
    # ALGORITMOS DE RECORRIDO
    # ========================================================================
    
    def bfs(self, inicio):
        """
        Recorrido en Anchura (Breadth-First Search).
        
        Complejidad: O(V + E)
        
        Args:
            inicio: Vértice inicial
            
        Returns:
            Lista de vértices visitados en orden BFS
        """
        if inicio not in self.vertices:
            return []
        
        visitados = []
        cola = deque([inicio])
        visitados_set = {inicio}
        
        while cola:
            vertice = cola.popleft()
            visitados.append(vertice)
            
            # Obtener vecinos
            if self.ponderado:
                vecinos = [v for v, _ in self.adyacencias[vertice]]
            else:
                vecinos = self.adyacencias[vertice]
            
            for vecino in vecinos:
                if vecino not in visitados_set:
                    visitados_set.add(vecino)
                    cola.append(vecino)
        
        return visitados
    
    def dfs(self, inicio):
        """
        Recorrido en Profundidad (Depth-First Search).
        
        Complejidad: O(V + E)
        
        Args:
            inicio: Vértice inicial
            
        Returns:
            Lista de vértices visitados en orden DFS
        """
        if inicio not in self.vertices:
            return []
        
        visitados = []
        visitados_set = set()
        
        def dfs_recursivo(vertice):
            visitados_set.add(vertice)
            visitados.append(vertice)
            
            # Obtener vecinos
            if self.ponderado:
                vecinos = [v for v, _ in self.adyacencias[vertice]]
            else:
                vecinos = self.adyacencias[vertice]
            
            for vecino in vecinos:
                if vecino not in visitados_set:
                    dfs_recursivo(vecino)
        
        dfs_recursivo(inicio)
        return visitados
    
    def camino_mas_corto_bfs(self, origen, destino):
        """
        Encuentra el camino más corto entre dos vértices usando BFS.
        Solo para grafos no ponderados o con pesos iguales.
        
        Complejidad: O(V + E)
        
        Args:
            origen: Vértice de origen
            destino: Vértice de destino
            
        Returns:
            Lista con el camino más corto, o None si no existe camino
        """
        if origen not in self.vertices or destino not in self.vertices:
            return None
        
        if origen == destino:
            return [origen]
        
        # BFS con seguimiento de padres
        visitados = {origen}
        cola = deque([origen])
        padres = {origen: None}
        
        while cola:
            vertice = cola.popleft()
            
            # Obtener vecinos
            if self.ponderado:
                vecinos = [v for v, _ in self.adyacencias[vertice]]
            else:
                vecinos = self.adyacencias[vertice]
            
            for vecino in vecinos:
                if vecino not in visitados:
                    visitados.add(vecino)
                    padres[vecino] = vertice
                    cola.append(vecino)
                    
                    # Si encontramos el destino, reconstruir camino
                    if vecino == destino:
                        camino = []
                        actual = destino
                        while actual is not None:
                            camino.append(actual)
                            actual = padres[actual]
                        return camino[::-1]  # Invertir
        
        return None  # No hay camino
    
    def dijkstra(self, origen):
        """
        Algoritmo de Dijkstra para encontrar caminos más cortos desde un origen.
        Solo para grafos ponderados con pesos no negativos.
        
        Complejidad: O((V + E) log V) con heap
        
        Args:
            origen: Vértice de origen
            
        Returns:
            Diccionario con distancias mínimas y diccionario de padres
        """
        if not self.ponderado:
            raise ValueError("Dijkstra requiere un grafo ponderado")
        
        if origen not in self.vertices:
            return {}, {}
        
        # Inicializar distancias
        distancias = {v: float('inf') for v in self.vertices}
        distancias[origen] = 0
        padres = {origen: None}
        
        # Heap de prioridad: (distancia, vértice)
        heap = [(0, origen)]
        visitados = set()
        
        while heap:
            dist_actual, vertice_actual = heapq.heappop(heap)
            
            if vertice_actual in visitados:
                continue
            
            visitados.add(vertice_actual)
            
            # Relajar aristas
            for vecino, peso in self.adyacencias[vertice_actual]:
                if vecino in visitados:
                    continue
                
                nueva_distancia = dist_actual + peso
                
                if nueva_distancia < distancias[vecino]:
                    distancias[vecino] = nueva_distancia
                    padres[vecino] = vertice_actual
                    heapq.heappush(heap, (nueva_distancia, vecino))
        
        return distancias, padres
    
    def reconstruir_camino_dijkstra(self, origen, destino, padres):
        """
        Reconstruye el camino más corto encontrado por Dijkstra.
        
        Args:
            origen: Vértice de origen
            destino: Vértice de destino
            padres: Diccionario de padres retornado por Dijkstra
            
        Returns:
            Lista con el camino, o None si no existe
        """
        if destino not in padres:
            return None
        
        camino = []
        actual = destino
        
        while actual is not None:
            camino.append(actual)
            actual = padres.get(actual)
        
        camino.reverse()
        
        if camino[0] == origen:
            return camino
        return None
    
    # ========================================================================
    # ANÁLISIS Y MÉTRICAS
    # ========================================================================
    
    def obtener_componentes_conexas(self):
        """
        Encuentra todas las componentes conexas del grafo.
        
        Returns:
            Lista de listas, cada una representa una componente conexa
        """
        visitados = set()
        componentes = []
        
        for vertice in self.vertices:
            if vertice not in visitados:
                # BFS para encontrar la componente
                componente = self.bfs(vertice)
                componentes.append(componente)
                visitados.update(componente)
        
        return componentes
    
    def obtener_vertices_mas_conectados(self, top_n=10):
        """
        Obtiene los vértices con mayor grado (más conexiones).
        
        Args:
            top_n: Número de vértices a retornar
            
        Returns:
            Lista de tuplas (vertice, grado) ordenadas por grado descendente
        """
        grados = [(v, self.obtener_grado(v)) for v in self.vertices]
        grados.sort(key=lambda x: x[1], reverse=True)
        return grados[:top_n]
    
    def calcular_densidad(self):
        """
        Calcula la densidad del grafo.
        Densidad = aristas / aristas_posibles
        
        Returns:
            Densidad del grafo (0 a 1)
        """
        n = len(self.vertices)
        if n <= 1:
            return 0.0
        
        if self.dirigido:
            aristas_posibles = n * (n - 1)
        else:
            aristas_posibles = n * (n - 1) / 2
        
        return self.num_aristas / aristas_posibles if aristas_posibles > 0 else 0.0
    
    def obtener_estadisticas(self):
        """
        Obtiene estadísticas generales del grafo.
        
        Returns:
            Diccionario con estadísticas
        """
        grados = [self.obtener_grado(v) for v in self.vertices]
        
        return {
            'num_vertices': len(self.vertices),
            'num_aristas': self.num_aristas,
            'grado_promedio': sum(grados) / len(grados) if grados else 0,
            'grado_maximo': max(grados) if grados else 0,
            'grado_minimo': min(grados) if grados else 0,
            'densidad': self.calcular_densidad(),
            'es_conexo': self.es_conexo(),
            'num_componentes': len(self.obtener_componentes_conexas())
        }
    
    def __str__(self):
        """Representación en string del grafo."""
        tipo = "Dirigido" if self.dirigido else "No dirigido"
        peso = "Ponderado" if self.ponderado else "No ponderado"
        return f"Grafo {tipo}, {peso} ({len(self.vertices)} vértices, {self.num_aristas} aristas)"
    
    def __repr__(self):
        return self.__str__()


# ============================================================================
# GRAFO BIPARTITO (USUARIO-LIBRO)
# ============================================================================

class GrafoBipartito(Grafo):
    """
    Grafo Bipartito especializado para modelar relaciones Usuario-Libro.
    
    Los vértices se dividen en dos conjuntos:
    - Conjunto A: Usuarios
    - Conjunto B: Libros
    
    Las aristas solo conectan vértices de diferentes conjuntos.
    """
    
    def __init__(self, ponderado=True):
        """
        Inicializa un grafo bipartito.
        
        Args:
            ponderado: Si las aristas tienen peso (ej: frecuencia de préstamos)
        """
        super().__init__(dirigido=False, ponderado=ponderado)
        self.conjunto_a = set()  # Usuarios
        self.conjunto_b = set()  # Libros
    
    def agregar_usuario(self, usuario_id):
        """Agrega un usuario al conjunto A."""
        self.agregar_vertice(usuario_id)
        self.conjunto_a.add(usuario_id)
    
    def agregar_libro(self, libro_id):
        """Agrega un libro al conjunto B."""
        self.agregar_vertice(libro_id)
        self.conjunto_b.add(libro_id)
    
    def agregar_interaccion(self, usuario_id, libro_id, peso=1):
        """
        Agrega una interacción entre usuario y libro.
        
        Args:
            usuario_id: ID del usuario
            libro_id: ID del libro
            peso: Peso de la interacción (ej: número de veces prestado)
        """
        self.agregar_usuario(usuario_id)
        self.agregar_libro(libro_id)
        
        # Incrementar peso si ya existe la arista
        peso_actual = self.obtener_peso_arista(usuario_id, libro_id)
        if peso_actual is not None:
            self.eliminar_arista(usuario_id, libro_id)
            peso += peso_actual
        
        self.agregar_arista(usuario_id, libro_id, peso)
    
    def obtener_libros_de_usuario(self, usuario_id):
        """
        Obtiene los libros que un usuario ha tomado prestados.
        
        Returns:
            Lista de tuplas (libro_id, peso)
        """
        if usuario_id not in self.conjunto_a:
            return []
        return self.obtener_vecinos(usuario_id)
    
    def obtener_usuarios_de_libro(self, libro_id):
        """
        Obtiene los usuarios que han tomado prestado un libro.
        
        Returns:
            Lista de tuplas (usuario_id, peso)
        """
        if libro_id not in self.conjunto_b:
            return []
        return self.obtener_vecinos(libro_id)
    
    def recomendar_libros(self, usuario_id, top_n=5):
        """
        Recomienda libros a un usuario basado en usuarios similares.
        
        Algoritmo:
        1. Encontrar usuarios que leyeron libros similares
        2. Obtener libros que esos usuarios leyeron
        3. Rankear por popularidad entre usuarios similares
        
        Args:
            usuario_id: ID del usuario
            top_n: Número de recomendaciones
            
        Returns:
            Lista de tuplas (libro_id, score)
        """
        if usuario_id not in self.conjunto_a:
            return []
        
        # Libros que el usuario ya tiene
        libros_usuario = {libro for libro, _ in self.obtener_libros_de_usuario(usuario_id)}
        
        # Encontrar usuarios similares (que leyeron al menos un libro en común)
        usuarios_similares = set()
        for libro_id in libros_usuario:
            for usuario, _ in self.obtener_usuarios_de_libro(libro_id):
                if usuario != usuario_id:
                    usuarios_similares.add(usuario)
        
        # Contar libros recomendados
        recomendaciones = defaultdict(float)
        
        for usuario_similar in usuarios_similares:
            for libro_id, peso in self.obtener_libros_de_usuario(usuario_similar):
                if libro_id not in libros_usuario:
                    # Peso ponderado por interacciones
                    recomendaciones[libro_id] += peso
        
        # Ordenar y retornar top N
        ranked = sorted(recomendaciones.items(), key=lambda x: x[1], reverse=True)
        return ranked[:top_n]
    
    def obtener_libros_populares(self, top_n=10):
        """
        Obtiene los libros más populares (más préstamos).
        
        Returns:
            Lista de tuplas (libro_id, num_prestamos)
        """
        popularidad = []
        
        for libro_id in self.conjunto_b:
            usuarios = self.obtener_usuarios_de_libro(libro_id)
            total_prestamos = sum(peso for _, peso in usuarios)
            popularidad.append((libro_id, total_prestamos))
        
        popularidad.sort(key=lambda x: x[1], reverse=True)
        return popularidad[:top_n]
    
    def detectar_comunidades_usuarios(self):
        """
        Detecta comunidades de usuarios con intereses similares.
        
        Returns:
            Lista de conjuntos de usuarios agrupados por similitud
        """
        # Crear grafo de usuarios basado en libros compartidos
        grafo_usuarios = Grafo(dirigido=False, ponderado=True)
        
        for libro_id in self.conjunto_b:
            usuarios = [u for u, _ in self.obtener_usuarios_de_libro(libro_id)]
            # Conectar todos los usuarios que leyeron este libro
            for i in range(len(usuarios)):
                for j in range(i + 1, len(usuarios)):
                    u1, u2 = usuarios[i], usuarios[j]
                    peso_actual = grafo_usuarios.obtener_peso_arista(u1, u2) or 0
                    if peso_actual > 0:
                        grafo_usuarios.eliminar_arista(u1, u2)
                    grafo_usuarios.agregar_arista(u1, u2, peso_actual + 1)
        
        # Las componentes conexas son las comunidades
        return grafo_usuarios.obtener_componentes_conexas()
