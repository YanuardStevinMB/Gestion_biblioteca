"""
Estructuras de Datos Lineales para Sistema de Gestión de Biblioteca
================================================================

Este módulo contiene las implementaciones de las estructuras de datos lineales
utilizadas en el sistema de gestión de biblioteca:
- Lista enlazada
- Pila (Stack)
- Cola (Queue)
- Arreglo dinámico

Autor: [Tu nombre]
Fecha: 2024
Curso: Estructuras de Datos - Unidad 1
"""

class Nodo:
    """
    Clase que representa un nodo para estructuras enlazadas.
    
    Atributos:
        dato: Información almacenada en el nodo
        siguiente: Referencia al siguiente nodo
    """
    def __init__(self, dato):
        self.dato = dato
        self.siguiente = None

class ListaEnlazada:
    """
    Implementación de una lista enlazada simple.
    
    Esta estructura se utiliza para almacenar la información de libros
    permitiendo inserciones y eliminaciones eficientes.
    """
    
    def __init__(self):
        self.cabeza = None
        self.tamaño = 0
    
    def insertar_al_inicio(self, dato):
        """Inserta un elemento al inicio de la lista."""
        nuevo_nodo = Nodo(dato)
        nuevo_nodo.siguiente = self.cabeza
        self.cabeza = nuevo_nodo
        self.tamaño += 1
    
    def insertar_al_final(self, dato):
        """Inserta un elemento al final de la lista."""
        nuevo_nodo = Nodo(dato)
        if not self.cabeza:
            self.cabeza = nuevo_nodo
        else:
            actual = self.cabeza
            while actual.siguiente:
                actual = actual.siguiente
            actual.siguiente = nuevo_nodo
        self.tamaño += 1
    
    def buscar(self, criterio_busqueda):
        """
        Busca elementos en la lista basado en un criterio.
        
        Args:
            criterio_busqueda: Función que evalúa si un elemento cumple la condición
            
        Returns:
            Lista de elementos que cumplen el criterio
        """
        resultados = []
        actual = self.cabeza
        while actual:
            if criterio_busqueda(actual.dato):
                resultados.append(actual.dato)
            actual = actual.siguiente
        return resultados
    
    def eliminar(self, criterio_eliminacion):
        """Elimina elementos que cumplan con el criterio especificado."""
        if not self.cabeza:
            return False
        
        # Si el primer elemento cumple el criterio
        if criterio_eliminacion(self.cabeza.dato):
            self.cabeza = self.cabeza.siguiente
            self.tamaño -= 1
            return True
        
        # Buscar en el resto de la lista
        actual = self.cabeza
        while actual.siguiente:
            if criterio_eliminacion(actual.siguiente.dato):
                actual.siguiente = actual.siguiente.siguiente
                self.tamaño -= 1
                return True
            actual = actual.siguiente
        return False
    
    def obtener_todos(self):
        """Retorna todos los elementos de la lista."""
        elementos = []
        actual = self.cabeza
        while actual:
            elementos.append(actual.dato)
            actual = actual.siguiente
        return elementos
    
    def esta_vacia(self):
        """Verifica si la lista está vacía."""
        return self.cabeza is None
    
    def obtener_tamaño(self):
        """Retorna el tamaño de la lista."""
        return self.tamaño

class Pila:
    """
    Implementación de una pila (LIFO - Last In, First Out).
    
    Se utiliza para manejar el historial de préstamos recientes,
    permitiendo acceder rápidamente a las últimas operaciones.
    """
    
    def __init__(self):
        self.tope = None
        self.tamaño = 0
    
    def apilar(self, dato):
        """Agrega un elemento al tope de la pila."""
        nuevo_nodo = Nodo(dato)
        nuevo_nodo.siguiente = self.tope
        self.tope = nuevo_nodo
        self.tamaño += 1
    
    def desapilar(self):
        """
        Remueve y retorna el elemento del tope de la pila.
        
        Returns:
            Elemento del tope o None si la pila está vacía
        """
        if self.esta_vacia():
            return None
        dato = self.tope.dato
        self.tope = self.tope.siguiente
        self.tamaño -= 1
        return dato
    
    def ver_tope(self):
        """Retorna el elemento del tope sin removerlo."""
        if self.esta_vacia():
            return None
        return self.tope.dato
    
    def esta_vacia(self):
        """Verifica si la pila está vacía."""
        return self.tope is None
    
    def obtener_tamaño(self):
        """Retorna el tamaño de la pila."""
        return self.tamaño
    
    def obtener_todos(self):
        """Retorna todos los elementos de la pila (del tope hacia abajo)."""
        elementos = []
        actual = self.tope
        while actual:
            elementos.append(actual.dato)
            actual = actual.siguiente
        return elementos

class Cola:
    """
    Implementación de una cola (FIFO - First In, First Out).
    
    Se utiliza para manejar las solicitudes de préstamos pendientes,
    garantizando que se procesen en orden de llegada.
    """
    
    def __init__(self):
        self.frente = None
        self.final = None
        self.tamaño = 0
    
    def encolar(self, dato):
        """Agrega un elemento al final de la cola."""
        nuevo_nodo = Nodo(dato)
        if self.esta_vacia():
            self.frente = self.final = nuevo_nodo
        else:
            self.final.siguiente = nuevo_nodo
            self.final = nuevo_nodo
        self.tamaño += 1
    
    def desencolar(self):
        """
        Remueve y retorna el elemento del frente de la cola.
        
        Returns:
            Elemento del frente o None si la cola está vacía
        """
        if self.esta_vacia():
            return None
        dato = self.frente.dato
        self.frente = self.frente.siguiente
        if self.frente is None:  # Si la cola queda vacía
            self.final = None
        self.tamaño -= 1
        return dato
    
    def ver_frente(self):
        """Retorna el elemento del frente sin removerlo."""
        if self.esta_vacia():
            return None
        return self.frente.dato
    
    def esta_vacia(self):
        """Verifica si la cola está vacía."""
        return self.frente is None
    
    def obtener_tamaño(self):
        """Retorna el tamaño de la cola."""
        return self.tamaño
    
    def obtener_todos(self):
        """Retorna todos los elementos de la cola (del frente al final)."""
        elementos = []
        actual = self.frente
        while actual:
            elementos.append(actual.dato)
            actual = actual.siguiente
        return elementos

class ArregloDinamico:
    """
    Implementación de un arreglo dinámico.
    
    Se utiliza para almacenar información de usuarios con acceso
    indexado rápido y capacidad de crecimiento automático.
    """
    
    def __init__(self, capacidad_inicial=10):
        self.capacidad = capacidad_inicial
        self.tamaño = 0
        self.datos = [None] * self.capacidad
    
    def _redimensionar(self):
        """Duplica la capacidad del arreglo cuando es necesario."""
        nueva_capacidad = self.capacidad * 2
        nuevo_arreglo = [None] * nueva_capacidad
        for i in range(self.tamaño):
            nuevo_arreglo[i] = self.datos[i]
        self.datos = nuevo_arreglo
        self.capacidad = nueva_capacidad
    
    def agregar(self, elemento):
        """Agrega un elemento al final del arreglo."""
        if self.tamaño >= self.capacidad:
            self._redimensionar()
        self.datos[self.tamaño] = elemento
        self.tamaño += 1
    
    def obtener(self, indice):
        """
        Obtiene el elemento en la posición especificada.
        
        Args:
            indice: Posición del elemento (0-indexado)
            
        Returns:
            Elemento en la posición especificada
            
        Raises:
            IndexError: Si el índice está fuera de rango
        """
        if 0 <= indice < self.tamaño:
            return self.datos[indice]
        raise IndexError("Índice fuera de rango")
    
    def establecer(self, indice, elemento):
        """
        Establece el valor en la posición especificada.
        
        Args:
            indice: Posición donde establecer el elemento
            elemento: Nuevo elemento
            
        Raises:
            IndexError: Si el índice está fuera de rango
        """
        if 0 <= indice < self.tamaño:
            self.datos[indice] = elemento
        else:
            raise IndexError("Índice fuera de rango")
    
    def buscar(self, criterio_busqueda):
        """
        Busca elementos que cumplan con el criterio especificado.
        
        Args:
            criterio_busqueda: Función que evalúa si un elemento cumple la condición
            
        Returns:
            Lista de elementos que cumplen el criterio
        """
        resultados = []
        for i in range(self.tamaño):
            if criterio_busqueda(self.datos[i]):
                resultados.append(self.datos[i])
        return resultados
    
    def eliminar(self, indice):
        """
        Elimina el elemento en la posición especificada.
        
        Args:
            indice: Posición del elemento a eliminar
            
        Returns:
            Elemento eliminado
            
        Raises:
            IndexError: Si el índice está fuera de rango
        """
        if not (0 <= indice < self.tamaño):
            raise IndexError("Índice fuera de rango")
        
        elemento_eliminado = self.datos[indice]
        # Desplazar elementos hacia la izquierda
        for i in range(indice, self.tamaño - 1):
            self.datos[i] = self.datos[i + 1]
        self.tamaño -= 1
        return elemento_eliminado
    
    def obtener_todos(self):
        """Retorna todos los elementos del arreglo."""
        return [self.datos[i] for i in range(self.tamaño)]
    
    def esta_vacio(self):
        """Verifica si el arreglo está vacío."""
        return self.tamaño == 0
    
    def obtener_tamaño(self):
        """Retorna el tamaño actual del arreglo."""
        return self.tamaño