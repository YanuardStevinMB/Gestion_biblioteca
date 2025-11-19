"""
Estructuras de Datos No Lineales (Árboles) para Sistema de Gestión de Biblioteca
================================================================================

Este módulo contiene las implementaciones de estructuras de árboles utilizadas
para optimizar las operaciones del sistema de gestión de biblioteca:
- Árbol AVL (autobalance ado)
- Min-Heap (cola de prioridad)
- Trie (árbol de prefijos)
- Árbol N-ario (jerarquía de categorías)

Autor: Equipo de Desarrollo Biblioteca Virtual
Fecha: 2025
Curso: Estructuras de Datos - Unidad 2
"""

from datetime import datetime


# ============================================================================
# ÁRBOL AVL (Adelson-Velsky y Landis)
# ============================================================================

class NodoAVL:
    """
    Nodo de un árbol AVL.
    
    Atributos:
        dato: Información almacenada en el nodo
        clave: Valor utilizado para comparaciones y ordenamiento
        izquierdo: Referencia al hijo izquierdo
        derecho: Referencia al hijo derecho
        altura: Altura del subárbol con raíz en este nodo
    """
    
    def __init__(self, dato, clave):
        self.dato = dato
        self.clave = clave
        self.izquierdo = None
        self.derecho = None
        self.altura = 1


class ArbolAVL:
    """
    Implementación de un Árbol AVL (Árbol Binario de Búsqueda Autobalanceado).
    
    El árbol AVL mantiene la propiedad de que para cada nodo, la diferencia
    de alturas entre sus subárboles izquierdo y derecho es como máximo 1.
    
    Garantiza operaciones de búsqueda, inserción y eliminación en O(log n).
    """
    
    def __init__(self, funcion_clave=None):
        """
        Inicializa un árbol AVL vacío.
        
        Args:
            funcion_clave: Función para extraer la clave de comparación del dato.
                          Si es None, se usa el dato directamente.
        """
        self.raiz = None
        self.tamaño = 0
        self.funcion_clave = funcion_clave if funcion_clave else lambda x: x
    
    def obtener_altura(self, nodo):
        """Retorna la altura de un nodo (0 si el nodo es None)."""
        if not nodo:
            return 0
        return nodo.altura
    
    def obtener_altura_arbol(self):
        """Retorna la altura del árbol completo."""
        return self.obtener_altura(self.raiz)
    
    def obtener_factor_balance(self, nodo):
        """
        Calcula el factor de balance de un nodo.
        Factor de balance = altura(izquierdo) - altura(derecho)
        """
        if not nodo:
            return 0
        return self.obtener_altura(nodo.izquierdo) - self.obtener_altura(nodo.derecho)
    
    def actualizar_altura(self, nodo):
        """Actualiza la altura de un nodo basándose en las alturas de sus hijos."""
        if not nodo:
            return
        nodo.altura = 1 + max(self.obtener_altura(nodo.izquierdo),
                              self.obtener_altura(nodo.derecho))
    
    # ========== Rotaciones para Mantener el Balance ==========
    
    def rotar_derecha(self, y):
        """
        Realiza una rotación simple a la derecha.
        
            y                x
           / \              / \
          x   C    -->     A   y
         / \                  / \
        A   B                B   C
        
        Args:
            y: Nodo desbalanceado
            
        Returns:
            Nueva raíz del subárbol (x)
        """
        x = y.izquierdo
        B = x.derecho
        
        # Realizar rotación
        x.derecho = y
        y.izquierdo = B
        
        # Actualizar alturas
        self.actualizar_altura(y)
        self.actualizar_altura(x)
        
        return x
    
    def rotar_izquierda(self, x):
        """
        Realiza una rotación simple a la izquierda.
        
          x                  y
         / \                / \
        A   y      -->     x   C
           / \            / \
          B   C          A   B
        
        Args:
            x: Nodo desbalanceado
            
        Returns:
            Nueva raíz del subárbol (y)
        """
        y = x.derecho
        B = y.izquierdo
        
        # Realizar rotación
        y.izquierdo = x
        x.derecho = B
        
        # Actualizar alturas
        self.actualizar_altura(x)
        self.actualizar_altura(y)
        
        return y
    
    # ========== Operaciones Principales ==========
    
    def insertar(self, dato, clave=None):
        """
        Inserta un nuevo dato en el árbol AVL.
        
        Args:
            dato: Elemento a insertar
            clave: Clave de comparación (si None, se usa funcion_clave)
            
        Returns:
            True si se insertó correctamente, False si ya existe
        """
        if clave is None:
            clave = self.funcion_clave(dato)
        
        resultado = {"insertado": False}
        self.raiz = self._insertar_recursivo(self.raiz, dato, clave, resultado)
        
        if resultado["insertado"]:
            self.tamaño += 1
        
        return resultado["insertado"]
    
    def _insertar_recursivo(self, nodo, dato, clave, resultado):
        """Función auxiliar recursiva para insertar en el árbol AVL."""
        # 1. Realizar inserción estándar de BST
        if not nodo:
            resultado["insertado"] = True
            return NodoAVL(dato, clave)
        
        if clave < nodo.clave:
            nodo.izquierdo = self._insertar_recursivo(nodo.izquierdo, dato, clave, resultado)
        elif clave > nodo.clave:
            nodo.derecho = self._insertar_recursivo(nodo.derecho, dato, clave, resultado)
        else:
            # Clave duplicada, no se inserta
            return nodo
        
        # 2. Actualizar altura del nodo ancestro
        self.actualizar_altura(nodo)
        
        # 3. Obtener factor de balance
        balance = self.obtener_factor_balance(nodo)
        
        # 4. Si el nodo está desbalanceado, aplicar rotaciones
        
        # Caso Izquierda-Izquierda (LL)
        if balance > 1 and clave < nodo.izquierdo.clave:
            return self.rotar_derecha(nodo)
        
        # Caso Derecha-Derecha (RR)
        if balance < -1 and clave > nodo.derecho.clave:
            return self.rotar_izquierda(nodo)
        
        # Caso Izquierda-Derecha (LR)
        if balance > 1 and clave > nodo.izquierdo.clave:
            nodo.izquierdo = self.rotar_izquierda(nodo.izquierdo)
            return self.rotar_derecha(nodo)
        
        # Caso Derecha-Izquierda (RL)
        if balance < -1 and clave < nodo.derecho.clave:
            nodo.derecho = self.rotar_derecha(nodo.derecho)
            return self.rotar_izquierda(nodo)
        
        return nodo
    
    def buscar(self, clave):
        """
        Busca un elemento por su clave.
        
        Args:
            clave: Clave a buscar
            
        Returns:
            El dato asociado a la clave, o None si no se encuentra
        """
        nodo = self._buscar_nodo(self.raiz, clave)
        return nodo.dato if nodo else None
    
    def _buscar_nodo(self, nodo, clave):
        """Función auxiliar recursiva para buscar un nodo."""
        if not nodo or nodo.clave == clave:
            return nodo
        
        if clave < nodo.clave:
            return self._buscar_nodo(nodo.izquierdo, clave)
        else:
            return self._buscar_nodo(nodo.derecho, clave)
    
    def buscar_por_prefijo(self, prefijo):
        """
        Busca todos los elementos cuyas claves comienzan con el prefijo dado.
        
        Args:
            prefijo: Prefijo a buscar (debe ser string)
            
        Returns:
            Lista de datos que coinciden con el prefijo
        """
        resultados = []
        self._buscar_prefijo_recursivo(self.raiz, str(prefijo).lower(), resultados)
        return resultados
    
    def _buscar_prefijo_recursivo(self, nodo, prefijo, resultados):
        """Función auxiliar para búsqueda por prefijo."""
        if not nodo:
            return
        
        clave_str = str(nodo.clave).lower()
        
        # Explorar izquierdo si el prefijo puede estar ahí
        if prefijo <= clave_str:
            self._buscar_prefijo_recursivo(nodo.izquierdo, prefijo, resultados)
        
        # Verificar nodo actual
        if clave_str.startswith(prefijo):
            resultados.append(nodo.dato)
        
        # Explorar derecho si el prefijo puede estar ahí
        if prefijo >= clave_str[:len(prefijo)]:
            self._buscar_prefijo_recursivo(nodo.derecho, prefijo, resultados)
    
    def eliminar(self, clave):
        """
        Elimina un elemento del árbol por su clave.
        
        Args:
            clave: Clave del elemento a eliminar
            
        Returns:
            True si se eliminó correctamente, False si no se encontró
        """
        resultado = {"eliminado": False}
        self.raiz = self._eliminar_recursivo(self.raiz, clave, resultado)
        
        if resultado["eliminado"]:
            self.tamaño -= 1
        
        return resultado["eliminado"]
    
    def _eliminar_recursivo(self, nodo, clave, resultado):
        """Función auxiliar recursiva para eliminar en el árbol AVL."""
        # 1. Realizar eliminación estándar de BST
        if not nodo:
            return nodo
        
        if clave < nodo.clave:
            nodo.izquierdo = self._eliminar_recursivo(nodo.izquierdo, clave, resultado)
        elif clave > nodo.clave:
            nodo.derecho = self._eliminar_recursivo(nodo.derecho, clave, resultado)
        else:
            # Nodo encontrado, proceder a eliminar
            resultado["eliminado"] = True
            
            # Nodo con un solo hijo o sin hijos
            if not nodo.izquierdo:
                return nodo.derecho
            elif not nodo.derecho:
                return nodo.izquierdo
            
            # Nodo con dos hijos: obtener sucesor inorden (mínimo del subárbol derecho)
            sucesor = self._obtener_minimo(nodo.derecho)
            nodo.dato = sucesor.dato
            nodo.clave = sucesor.clave
            
            # Eliminar el sucesor
            nodo.derecho = self._eliminar_recursivo(nodo.derecho, sucesor.clave, {"eliminado": False})
        
        # Si el árbol tenía solo un nodo, retornar
        if not nodo:
            return nodo
        
        # 2. Actualizar altura
        self.actualizar_altura(nodo)
        
        # 3. Obtener factor de balance
        balance = self.obtener_factor_balance(nodo)
        
        # 4. Si el nodo está desbalanceado, aplicar rotaciones
        
        # Caso Izquierda-Izquierda
        if balance > 1 and self.obtener_factor_balance(nodo.izquierdo) >= 0:
            return self.rotar_derecha(nodo)
        
        # Caso Izquierda-Derecha
        if balance > 1 and self.obtener_factor_balance(nodo.izquierdo) < 0:
            nodo.izquierdo = self.rotar_izquierda(nodo.izquierdo)
            return self.rotar_derecha(nodo)
        
        # Caso Derecha-Derecha
        if balance < -1 and self.obtener_factor_balance(nodo.derecho) <= 0:
            return self.rotar_izquierda(nodo)
        
        # Caso Derecha-Izquierda
        if balance < -1 and self.obtener_factor_balance(nodo.derecho) > 0:
            nodo.derecho = self.rotar_derecha(nodo.derecho)
            return self.rotar_izquierda(nodo)
        
        return nodo
    
    def _obtener_minimo(self, nodo):
        """Obtiene el nodo con el valor mínimo en un subárbol."""
        actual = nodo
        while actual.izquierdo:
            actual = actual.izquierdo
        return actual
    
    # ========== Recorridos ==========
    
    def recorrido_inorden(self):
        """
        Realiza un recorrido inorden del árbol (izquierdo-raíz-derecho).
        
        Returns:
            Lista de datos en orden ascendente por clave
        """
        resultado = []
        self._inorden_recursivo(self.raiz, resultado)
        return resultado
    
    def _inorden_recursivo(self, nodo, resultado):
        """Función auxiliar para recorrido inorden."""
        if nodo:
            self._inorden_recursivo(nodo.izquierdo, resultado)
            resultado.append(nodo.dato)
            self._inorden_recursivo(nodo.derecho, resultado)
    
    def recorrido_preorden(self):
        """Realiza un recorrido preorden del árbol (raíz-izquierdo-derecho)."""
        resultado = []
        self._preorden_recursivo(self.raiz, resultado)
        return resultado
    
    def _preorden_recursivo(self, nodo, resultado):
        """Función auxiliar para recorrido preorden."""
        if nodo:
            resultado.append(nodo.dato)
            self._preorden_recursivo(nodo.izquierdo, resultado)
            self._preorden_recursivo(nodo.derecho, resultado)
    
    def recorrido_postorden(self):
        """Realiza un recorrido postorden del árbol (izquierdo-derecho-raíz)."""
        resultado = []
        self._postorden_recursivo(self.raiz, resultado)
        return resultado
    
    def _postorden_recursivo(self, nodo, resultado):
        """Función auxiliar para recorrido postorden."""
        if nodo:
            self._postorden_recursivo(nodo.izquierdo, resultado)
            self._postorden_recursivo(nodo.derecho, resultado)
            resultado.append(nodo.dato)
    
    # ========== Métodos de Utilidad ==========
    
    def esta_vacio(self):
        """Verifica si el árbol está vacío."""
        return self.raiz is None
    
    def obtener_tamaño(self):
        """Retorna el número de elementos en el árbol."""
        return self.tamaño
    
    def obtener_todos(self):
        """Retorna todos los elementos del árbol en orden."""
        return self.recorrido_inorden()
    
    def verificar_balance(self):
        """
        Verifica si el árbol está balanceado correctamente.
        
        Returns:
            True si el árbol es un AVL válido, False en caso contrario
        """
        return self._verificar_balance_recursivo(self.raiz)[0]
    
    def _verificar_balance_recursivo(self, nodo):
        """
        Función auxiliar para verificar el balance del árbol.
        
        Returns:
            Tupla (es_balanceado, altura)
        """
        if not nodo:
            return (True, 0)
        
        # Verificar subárboles
        izq_balanceado, altura_izq = self._verificar_balance_recursivo(nodo.izquierdo)
        der_balanceado, altura_der = self._verificar_balance_recursivo(nodo.derecho)
        
        # Verificar factor de balance
        balance = abs(altura_izq - altura_der) <= 1
        
        es_balanceado = izq_balanceado and der_balanceado and balance
        altura = 1 + max(altura_izq, altura_der)
        
        return (es_balanceado, altura)


# ============================================================================
# MIN-HEAP (Montículo Mínimo)
# ============================================================================

class MinHeap:
    """
    Implementación de un Min-Heap (montículo mínimo) usando un arreglo.
    
    En un min-heap, el elemento padre es siempre menor o igual que sus hijos,
    y el elemento mínimo está siempre en la raíz.
    
    Útil para colas de prioridad donde se necesita acceso rápido al mínimo.
    """
    
    def __init__(self, funcion_comparacion=None):
        """
        Inicializa un min-heap vacío.
        
        Args:
            funcion_comparacion: Función que toma dos elementos y retorna True
                               si el primero debe ir antes que el segundo.
                               Por defecto usa operador <
        """
        self.heap = []
        self.tamaño = 0
        self.comparar = funcion_comparacion if funcion_comparacion else lambda a, b: a < b
    
    def _padre(self, i):
        """Retorna el índice del padre del nodo i."""
        return (i - 1) // 2
    
    def _hijo_izquierdo(self, i):
        """Retorna el índice del hijo izquierdo del nodo i."""
        return 2 * i + 1
    
    def _hijo_derecho(self, i):
        """Retorna el índice del hijo derecho del nodo i."""
        return 2 * i + 2
    
    def _intercambiar(self, i, j):
        """Intercambia dos elementos en el heap."""
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]
    
    def _heapify_arriba(self, i):
        """
        Restaura la propiedad del heap moviendo el elemento hacia arriba.
        
        Se usa después de insertar un nuevo elemento.
        """
        padre = self._padre(i)
        
        if i > 0 and self.comparar(self.heap[i], self.heap[padre]):
            self._intercambiar(i, padre)
            self._heapify_arriba(padre)
    
    def _heapify_abajo(self, i):
        """
        Restaura la propiedad del heap moviendo el elemento hacia abajo.
        
        Se usa después de extraer el elemento mínimo.
        """
        minimo = i
        izq = self._hijo_izquierdo(i)
        der = self._hijo_derecho(i)
        
        # Encontrar el menor entre nodo, hijo izquierdo e hijo derecho
        if izq < self.tamaño and self.comparar(self.heap[izq], self.heap[minimo]):
            minimo = izq
        
        if der < self.tamaño and self.comparar(self.heap[der], self.heap[minimo]):
            minimo = der
        
        # Si el mínimo no es el nodo actual, intercambiar y continuar
        if minimo != i:
            self._intercambiar(i, minimo)
            self._heapify_abajo(minimo)
    
    def insertar(self, elemento):
        """
        Inserta un nuevo elemento en el heap.
        
        Complejidad: O(log n)
        
        Args:
            elemento: Elemento a insertar
        """
        self.heap.append(elemento)
        self.tamaño += 1
        self._heapify_arriba(self.tamaño - 1)
    
    def extraer_minimo(self):
        """
        Extrae y retorna el elemento mínimo del heap.
        
        Complejidad: O(log n)
        
        Returns:
            El elemento mínimo, o None si el heap está vacío
        """
        if self.tamaño == 0:
            return None
        
        if self.tamaño == 1:
            self.tamaño -= 1
            return self.heap.pop()
        
        # Guardar el mínimo
        minimo = self.heap[0]
        
        # Mover el último elemento a la raíz y restaurar la propiedad del heap
        self.heap[0] = self.heap.pop()
        self.tamaño -= 1
        self._heapify_abajo(0)
        
        return minimo
    
    def obtener_minimo(self):
        """
        Retorna el elemento mínimo sin extraerlo.
        
        Complejidad: O(1)
        
        Returns:
            El elemento mínimo, o None si el heap está vacío
        """
        return self.heap[0] if self.tamaño > 0 else None
    
    def esta_vacio(self):
        """Verifica si el heap está vacío."""
        return self.tamaño == 0
    
    def obtener_tamaño(self):
        """Retorna el número de elementos en el heap."""
        return self.tamaño
    
    def obtener_todos(self):
        """Retorna todos los elementos del heap (no necesariamente ordenados)."""
        return list(self.heap[:self.tamaño])


# ============================================================================
# TRIE (Árbol de Prefijos)
# ============================================================================

class NodoTrie:
    """
    Nodo de un Trie (árbol de prefijos).
    
    Atributos:
        hijos: Diccionario que mapea caracteres a nodos hijos
        es_fin_palabra: Indica si este nodo marca el final de una palabra
        dato: Dato completo asociado (si es fin de palabra)
        frecuencia: Contador de frecuencia (útil para ranking)
    """
    
    def __init__(self):
        self.hijos = {}
        self.es_fin_palabra = False
        self.dato = None
        self.frecuencia = 0


class Trie:
    """
    Implementación de un Trie (árbol de prefijos).
    
    Estructura de datos especializada para cadenas de texto,
    ideal para autocompletado y búsqueda de prefijos.
    
    Cada nodo representa un carácter, y los caminos desde la raíz
    hasta nodos marcados como "fin de palabra" representan palabras completas.
    """
    
    def __init__(self, case_sensitive=False):
        """
        Inicializa un Trie vacío.
        
        Args:
            case_sensitive: Si es True, distingue mayúsculas de minúsculas
        """
        self.raiz = NodoTrie()
        self.tamaño = 0
        self.case_sensitive = case_sensitive
    
    def _normalizar(self, texto):
        """Normaliza el texto según la configuración de case_sensitive."""
        return texto if self.case_sensitive else texto.lower()
    
    def insertar(self, palabra, dato=None):
        """
        Inserta una palabra en el Trie.
        
        Complejidad: O(m) donde m es la longitud de la palabra
        
        Args:
            palabra: Palabra a insertar
            dato: Dato asociado a la palabra (opcional)
            
        Returns:
            True si se insertó una nueva palabra, False si ya existía
        """
        if not palabra:
            return False
        
        palabra = self._normalizar(str(palabra))
        nodo = self.raiz
        
        # Navegar/crear el camino para la palabra
        for caracter in palabra:
            if caracter not in nodo.hijos:
                nodo.hijos[caracter] = NodoTrie()
            nodo = nodo.hijos[caracter]
        
        # Marcar como fin de palabra
        if not nodo.es_fin_palabra:
            nodo.es_fin_palabra = True
            nodo.dato = dato if dato is not None else palabra
            self.tamaño += 1
            nodo.frecuencia = 1
            return True
        else:
            # Palabra ya existe, incrementar frecuencia
            nodo.frecuencia += 1
            return False
    
    def buscar(self, palabra):
        """
        Busca una palabra exacta en el Trie.
        
        Complejidad: O(m) donde m es la longitud de la palabra
        
        Args:
            palabra: Palabra a buscar
            
        Returns:
            El dato asociado si la palabra existe, None en caso contrario
        """
        if not palabra:
            return None
        
        palabra = self._normalizar(str(palabra))
        nodo = self.raiz
        
        # Navegar el camino de la palabra
        for caracter in palabra:
            if caracter not in nodo.hijos:
                return None
            nodo = nodo.hijos[caracter]
        
        # Verificar si es una palabra completa
        return nodo.dato if nodo.es_fin_palabra else None
    
    def comienza_con(self, prefijo):
        """
        Verifica si existe alguna palabra con el prefijo dado.
        
        Args:
            prefijo: Prefijo a verificar
            
        Returns:
            True si existe al menos una palabra con ese prefijo
        """
        if not prefijo:
            return True
        
        prefijo = self._normalizar(str(prefijo))
        nodo = self.raiz
        
        for caracter in prefijo:
            if caracter not in nodo.hijos:
                return False
            nodo = nodo.hijos[caracter]
        
        return True
    
    def autocompletar(self, prefijo, limite=10):
        """
        Retorna sugerencias de autocompletado para un prefijo dado.
        
        Complejidad: O(m + k) donde m es la longitud del prefijo
                     y k es el número de resultados
        
        Args:
            prefijo: Prefijo para buscar sugerencias
            limite: Número máximo de sugerencias a retornar
            
        Returns:
            Lista de tuplas (palabra, dato, frecuencia) ordenadas por frecuencia
        """
        if prefijo is None:
            return []
        
        prefijo = self._normalizar(str(prefijo))
        nodo = self.raiz
        
        # Si el prefijo está vacío, empezar desde la raíz
        if prefijo:
            # Navegar hasta el nodo del prefijo
            for caracter in prefijo:
                if caracter not in nodo.hijos:
                    return []
                nodo = nodo.hijos[caracter]
        
        # Recolectar todas las palabras que comienzan con el prefijo
        resultados = []
        self._recolectar_palabras(nodo, prefijo, resultados)
        
        # Ordenar por frecuencia (descendente) y limitar
        resultados.sort(key=lambda x: x[2], reverse=True)
        return resultados[:limite]
    
    def _recolectar_palabras(self, nodo, prefijo_actual, resultados):
        """
        Función auxiliar recursiva para recolectar palabras desde un nodo.
        
        Args:
            nodo: Nodo actual
            prefijo_actual: Prefijo construido hasta el momento
            resultados: Lista donde se almacenan los resultados
        """
        if nodo.es_fin_palabra:
            resultados.append((prefijo_actual, nodo.dato, nodo.frecuencia))
        
        for caracter, hijo in nodo.hijos.items():
            self._recolectar_palabras(hijo, prefijo_actual + caracter, resultados)
    
    def eliminar(self, palabra):
        """
        Elimina una palabra del Trie.
        
        Args:
            palabra: Palabra a eliminar
            
        Returns:
            True si se eliminó correctamente, False si no existía
        """
        if not palabra:
            return False
        
        palabra = self._normalizar(str(palabra))
        
        resultado = {"eliminado": False}
        self.raiz = self._eliminar_recursivo(self.raiz, palabra, 0, resultado)
        
        if resultado["eliminado"]:
            self.tamaño -= 1
        
        return resultado["eliminado"]
    
    def _eliminar_recursivo(self, nodo, palabra, profundidad, resultado):
        """Función auxiliar recursiva para eliminar una palabra."""
        if not nodo:
            return None
        
        # Caso base: hemos llegado al final de la palabra
        if profundidad == len(palabra):
            if nodo.es_fin_palabra:
                nodo.es_fin_palabra = False
                nodo.dato = None
                resultado["eliminado"] = True
            
            # Si el nodo no tiene hijos, puede ser eliminado
            if not nodo.hijos:
                return None
            
            return nodo
        
        # Recursión
        caracter = palabra[profundidad]
        if caracter in nodo.hijos:
            nodo.hijos[caracter] = self._eliminar_recursivo(
                nodo.hijos[caracter], palabra, profundidad + 1, resultado
            )
            
            # Si el hijo fue eliminado, remover la entrada
            if nodo.hijos[caracter] is None:
                del nodo.hijos[caracter]
        
        # Si el nodo actual no es fin de palabra y no tiene hijos, puede ser eliminado
        if not nodo.es_fin_palabra and not nodo.hijos:
            return None
        
        return nodo
    
    def esta_vacio(self):
        """Verifica si el Trie está vacío."""
        return self.tamaño == 0
    
    def obtener_tamaño(self):
        """Retorna el número de palabras en el Trie."""
        return self.tamaño
    
    def obtener_todas_palabras(self):
        """Retorna todas las palabras almacenadas en el Trie."""
        resultados = []
        self._recolectar_palabras(self.raiz, "", resultados)
        return [palabra for palabra, _, _ in resultados]


# ============================================================================
# ÁRBOL N-ARIO (Jerarquía de Categorías)
# ============================================================================

class NodoCategoria:
    """
    Nodo de un árbol N-ario para representar categorías jerárquicas.
    
    Atributos:
        nombre: Nombre de la categoría
        padre: Referencia al nodo padre (None para la raíz)
        hijos: Lista de nodos hijos (subcategorías)
        datos: Lista de datos asociados a esta categoría
    """
    
    def __init__(self, nombre, padre=None):
        self.nombre = nombre
        self.padre = padre
        self.hijos = []
        self.datos = []
    
    def agregar_hijo(self, hijo):
        """Agrega un hijo (subcategoría) a este nodo."""
        hijo.padre = self
        self.hijos.append(hijo)
    
    def agregar_dato(self, dato):
        """Agrega un dato a esta categoría."""
        self.datos.append(dato)
    
    def es_raiz(self):
        """Verifica si este nodo es la raíz."""
        return self.padre is None
    
    def es_hoja(self):
        """Verifica si este nodo es una hoja (no tiene hijos)."""
        return len(self.hijos) == 0
    
    def obtener_nivel(self):
        """Retorna el nivel del nodo (la raíz está en el nivel 0)."""
        nivel = 0
        nodo = self
        while nodo.padre:
            nivel += 1
            nodo = nodo.padre
        return nivel
    
    def obtener_ruta(self):
        """Retorna la ruta desde la raíz hasta este nodo."""
        ruta = []
        nodo = self
        while nodo:
            ruta.insert(0, nodo.nombre)
            nodo = nodo.padre
        return ruta


class ArbolCategorias:
    """
    Árbol N-ario para representar jerarquías de categorías.
    
    Cada nodo puede tener cualquier número de hijos, permitiendo
    representar estructuras jerárquicas complejas como categorías
    y subcategorías de productos, sistemas de archivos, etc.
    """
    
    def __init__(self, nombre_raiz="Raíz"):
        """
        Inicializa el árbol con un nodo raíz.
        
        Args:
            nombre_raiz: Nombre del nodo raíz
        """
        self.raiz = NodoCategoria(nombre_raiz)
        self.tamaño = 1  # Contando la raíz
    
    def agregar_categoria(self, nombre_categoria, nombre_padre=None):
        """
        Agrega una nueva categoría al árbol.
        
        Args:
            nombre_categoria: Nombre de la nueva categoría
            nombre_padre: Nombre de la categoría padre (None para agregar a la raíz)
            
        Returns:
            True si se agregó correctamente, False si el padre no existe
        """
        # Buscar el nodo padre
        if nombre_padre is None:
            padre = self.raiz
        else:
            padre = self.buscar_categoria(nombre_padre)
            if not padre:
                return False
        
        # Crear y agregar la nueva categoría
        nueva_categoria = NodoCategoria(nombre_categoria, padre)
        padre.agregar_hijo(nueva_categoria)
        self.tamaño += 1
        
        return True
    
    def buscar_categoria(self, nombre):
        """
        Busca una categoría por su nombre.
        
        Usa búsqueda en amplitud (BFS) para recorrer el árbol.
        
        Args:
            nombre: Nombre de la categoría a buscar
            
        Returns:
            El nodo de la categoría si se encuentra, None en caso contrario
        """
        cola = [self.raiz]
        
        while cola:
            nodo = cola.pop(0)
            
            if nodo.nombre.lower() == nombre.lower():
                return nodo
            
            cola.extend(nodo.hijos)
        
        return None
    
    def agregar_dato_a_categoria(self, nombre_categoria, dato):
        """
        Agrega un dato a una categoría específica.
        
        Args:
            nombre_categoria: Nombre de la categoría
            dato: Dato a agregar
            
        Returns:
            True si se agregó correctamente, False si la categoría no existe
        """
        categoria = self.buscar_categoria(nombre_categoria)
        if not categoria:
            return False
        
        categoria.agregar_dato(dato)
        return True
    
    def obtener_datos_categoria(self, nombre_categoria, incluir_subcategorias=False):
        """
        Obtiene los datos de una categoría.
        
        Args:
            nombre_categoria: Nombre de la categoría
            incluir_subcategorias: Si es True, incluye datos de subcategorías
            
        Returns:
            Lista de datos, o None si la categoría no existe
        """
        categoria = self.buscar_categoria(nombre_categoria)
        if not categoria:
            return None
        
        if not incluir_subcategorias:
            return list(categoria.datos)
        
        # Recolectar datos de esta categoría y todas sus subcategorías
        datos = []
        self._recolectar_datos_recursivo(categoria, datos)
        return datos
    
    def _recolectar_datos_recursivo(self, nodo, datos):
        """Función auxiliar recursiva para recolectar datos."""
        datos.extend(nodo.datos)
        for hijo in nodo.hijos:
            self._recolectar_datos_recursivo(hijo, datos)
    
    def obtener_subcategorias(self, nombre_categoria):
        """
        Obtiene las subcategorías directas de una categoría.
        
        Args:
            nombre_categoria: Nombre de la categoría
            
        Returns:
            Lista de nombres de subcategorías, o None si la categoría no existe
        """
        categoria = self.buscar_categoria(nombre_categoria)
        if not categoria:
            return None
        
        return [hijo.nombre for hijo in categoria.hijos]
    
    def obtener_jerarquia_completa(self):
        """
        Retorna la jerarquía completa del árbol como una estructura de diccionarios.
        
        Returns:
            Diccionario anidado representando la jerarquía
        """
        return self._construir_jerarquia_recursiva(self.raiz)
    
    def _construir_jerarquia_recursiva(self, nodo):
        """Función auxiliar para construir la jerarquía."""
        jerarquia = {
            "nombre": nodo.nombre,
            "nivel": nodo.obtener_nivel(),
            "cantidad_datos": len(nodo.datos),
            "subcategorias": []
        }
        
        for hijo in nodo.hijos:
            jerarquia["subcategorias"].append(self._construir_jerarquia_recursiva(hijo))
        
        return jerarquia
    
    def imprimir_jerarquia(self, nodo=None, prefijo="", es_ultimo=True):
        """
        Imprime la jerarquía del árbol de forma visual.
        
        Args:
            nodo: Nodo desde donde imprimir (None para empezar desde la raíz)
            prefijo: Prefijo para la indentación (uso interno)
            es_ultimo: Indica si es el último hijo (uso interno)
        """
        if nodo is None:
            nodo = self.raiz
        
        # Imprimir el nodo actual
        conector = "└── " if es_ultimo else "├── "
        print(f"{prefijo}{conector}{nodo.nombre} ({len(nodo.datos)} elementos)")
        
        # Actualizar prefijo para los hijos
        if es_ultimo:
            nuevo_prefijo = prefijo + "    "
        else:
            nuevo_prefijo = prefijo + "│   "
        
        # Imprimir hijos
        for i, hijo in enumerate(nodo.hijos):
            es_ultimo_hijo = (i == len(nodo.hijos) - 1)
            self.imprimir_jerarquia(hijo, nuevo_prefijo, es_ultimo_hijo)
    
    def obtener_tamaño(self):
        """Retorna el número total de categorías en el árbol."""
        return self.tamaño
    
    def obtener_altura(self):
        """Retorna la altura del árbol (máximo nivel de profundidad)."""
        return self._obtener_altura_recursiva(self.raiz)
    
    def _obtener_altura_recursiva(self, nodo):
        """Función auxiliar recursiva para obtener la altura."""
        if nodo.es_hoja():
            return 0
        
        altura_maxima = 0
        for hijo in nodo.hijos:
            altura = self._obtener_altura_recursiva(hijo)
            altura_maxima = max(altura_maxima, altura)
        
        return 1 + altura_maxima
