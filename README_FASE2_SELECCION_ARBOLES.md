# FASE 2: SELECCIÓN DE ESTRUCTURAS DE ÁRBOL APROPIADAS

## 📋 Información del Proyecto

**Asignatura:** Estructuras de Datos - Unidad 2  
**Tema:** Selección y Diseño de Árboles  
**Fecha:** Octubre 2025  
**Autor:** Equipo de Desarrollo Biblioteca Virtual

---

## 🎯 Objetivo de la Fase 2

Seleccionar y justificar las estructuras de árbol más apropiadas para optimizar las operaciones del Sistema de Gestión de Biblioteca, basándose en el análisis realizado en la Fase 1.

---

## 📊 Análisis de Requisitos

### Operaciones Críticas Identificadas en Fase 1

| Operación | Frecuencia | Complejidad Actual | Impacto |
|-----------|------------|-------------------|---------|
| Búsqueda de libros por ISBN | Alta | O(n) | Alto |
| Búsqueda de libros por título | Alta | O(n) | Alto |
| Búsqueda de usuarios por ID | Media | O(n) | Medio |
| Búsqueda de usuarios por email | Media | O(n) | Medio |
| Organización por categorías | Baja | O(n) | Bajo |
| Gestión de préstamos por fecha | Alta | O(n) | Alto |
| Autocompletado de títulos | Media | O(n) | Medio |
| Búsqueda por rango de años | Baja | O(n) | Bajo |

---

## 🌳 Tipos de Árboles Considerados

### 1. Árbol Binario de Búsqueda (BST)

**Características:**
- Cada nodo tiene como máximo 2 hijos
- Subárbol izquierdo contiene valores menores
- Subárbol derecho contiene valores mayores
- Búsqueda, inserción, eliminación: O(log n) promedio, O(n) peor caso

**Ventajas:**
- Implementación simple
- Búsqueda eficiente en promedio
- Recorrido in-order produce elementos ordenados

**Desventajas:**
- Puede degenerar en lista enlazada (peor caso)
- No balanceado automáticamente

---

### 2. Árbol AVL (Adelson-Velsky y Landis)

**Características:**
- BST autobalanceado
- Factor de balance: |altura(izq) - altura(der)| ≤ 1
- Rotaciones para mantener balance
- Búsqueda, inserción, eliminación: O(log n) garantizado

**Ventajas:**
- Búsqueda muy eficiente (mejor que Red-Black para búsquedas intensivas)
- Altura garantizada: h ≤ 1.44 * log(n)
- Ideal para sistemas con más lecturas que escrituras

**Desventajas:**
- Rotaciones frecuentes en inserciones/eliminaciones
- Overhead de almacenamiento (altura en cada nodo)

---

### 3. Árbol Rojo-Negro (Red-Black Tree)

**Características:**
- BST autobalanceado con color (rojo/negro)
- Altura máxima: 2 * log(n)
- Menos rotaciones que AVL en inserciones

**Ventajas:**
- Mejor rendimiento en inserciones/eliminaciones frecuentes
- Menos estricto en balanceo que AVL

**Desventajas:**
- Búsqueda ligeramente más lenta que AVL
- Implementación más compleja

---

### 4. Árbol B (B-Tree)

**Características:**
- Cada nodo puede tener múltiples claves
- Todos los nodos hoja están al mismo nivel
- Ideal para sistemas de almacenamiento en disco

**Ventajas:**
- Minimiza operaciones de I/O
- Excelente para grandes volúmenes de datos
- Factor de ramificación alto

**Desventajas:**
- Overhead de implementación para aplicaciones en memoria
- No necesario para datasets pequeños/medianos

---

### 5. Trie (Árbol de Prefijos)

**Características:**
- Árbol especializado para cadenas
- Cada nodo representa un carácter
- Búsqueda: O(m) donde m = longitud de la cadena

**Ventajas:**
- Excelente para autocompletado
- Búsqueda de prefijos muy eficiente
- No hay colisiones como en hash tables

**Desventajas:**
- Alto uso de memoria
- Solo para cadenas

---

### 6. Heap Binario

**Características:**
- Árbol binario completo
- Min-heap: padre ≤ hijos
- Max-heap: padre ≥ hijos
- Inserción/eliminación: O(log n)

**Ventajas:**
- Acceso O(1) al elemento mínimo/máximo
- Ideal para colas de prioridad
- Implementación eficiente con arreglos

**Desventajas:**
- Búsqueda general: O(n)
- No mantiene orden total

---

## 🎯 Selección de Estructuras para el Sistema

### DECISIÓN 1: Árbol AVL para Búsqueda de Libros por ISBN

**Justificación:**

El catálogo de libros es una operación de **lectura intensiva** con **actualizaciones poco frecuentes**:
- Búsquedas de libros: muy frecuentes
- Registro de nuevos libros: poco frecuente
- Eliminación de libros: muy poco frecuente

El **Árbol AVL** es ideal porque:
1. Garantiza O(log n) en todas las operaciones
2. Optimizado para búsquedas (mejor que Red-Black)
3. El ISBN es un identificador único y comparable
4. El overhead de balanceo se compensa con búsquedas frecuentes

**Comparación con Alternativas:**

| Criterio | AVL | BST Simple | Red-Black |
|----------|-----|------------|-----------|
| Búsqueda | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ |
| Inserción | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| Garantía de balance | ✅ | ❌ | ✅ |
| Complejidad implementación | Media | Baja | Alta |
| **Decisión** | ✅ **SELECCIONADO** | ❌ | ❌ |

**Estructura del Nodo:**

```python
class NodoAVLLibro:
    def __init__(self, libro):
        self.libro = libro              # Objeto Libro
        self.isbn = libro.isbn          # Clave de búsqueda
        self.izquierdo = None
        self.derecho = None
        self.altura = 1                 # Altura del nodo
```

**Operaciones Principales:**
- `insertar(libro)`: O(log n)
- `buscar_por_isbn(isbn)`: O(log n)
- `eliminar_por_isbn(isbn)`: O(log n)
- `recorrido_inorden()`: O(n) - Listado alfabético de ISBNs

---

### DECISIÓN 2: Árbol AVL para Búsqueda de Libros por Título

**Justificación:**

Los usuarios frecuentemente buscan libros por título. Necesitamos:
- Búsqueda exacta por título
- Búsqueda por prefijo (autocomplete)
- Orden alfabético natural

**Decisión:** Árbol AVL con clave = título (normalizado)

**Alternativa Considerada:** Trie
- ❌ Rechazada por alto uso de memoria para títulos completos
- ✅ AVL es más eficiente en memoria y suficientemente rápido

**Estructura del Nodo:**

```python
class NodoAVLTitulo:
    def __init__(self, libro):
        self.libro = libro
        self.clave_busqueda = libro.titulo.lower().strip()  # Normalizado
        self.izquierdo = None
        self.derecho = None
        self.altura = 1
```

**Características Especiales:**
- Clave normalizada (lowercase, sin espacios extras)
- Permite búsqueda case-insensitive
- Orden alfabético natural en recorrido in-order

---

### DECISIÓN 3: Árbol BST para Usuarios por ID

**Justificación:**

Los IDs de usuario son secuenciales (U001, U002, U003...). Características:
- Inserciones siempre en orden ascendente
- Búsquedas frecuentes por ID
- Dataset relativamente pequeño (cientos, no millones)

**Decisión:** BST Simple (no se requiere AVL)

**Razón:**
- Los IDs secuenciales generarían un BST desbalanceado
- **Solución:** Usar un árbol balanceado por construcción batch
- O usar Red-Black Tree para garantizar balance

**REVISIÓN DE DECISIÓN:** Usar **Árbol AVL** también aquí
- Aunque los IDs son secuenciales, el AVL manejará mejor el caso
- Costo de implementación es el mismo (ya tenemos la clase AVL genérica)

**Estructura del Nodo:**

```python
class NodoAVLUsuario:
    def __init__(self, usuario):
        self.usuario = usuario
        self.id_usuario = usuario.id_usuario
        self.izquierdo = None
        self.derecho = None
        self.altura = 1
```

---

### DECISIÓN 4: Árbol de Categorías (Árbol N-ario)

**Justificación:**

Las categorías de libros tienen una estructura jerárquica natural:
```
Ficción
├── Ciencia Ficción
│   ├── Distopía
│   └── Space Opera
├── Fantasía
│   ├── Alta Fantasía
│   └── Fantasía Urbana
└── Realismo
    └── Realismo Mágico

No Ficción
├── Historia
├── Ciencia
└── Biografía
```

**Decisión:** Árbol N-ario (cada nodo puede tener múltiples hijos)

**Estructura del Nodo:**

```python
class NodoCategoria:
    def __init__(self, nombre):
        self.nombre = nombre                    # Nombre de la categoría
        self.subcategorias = []                 # Lista de hijos
        self.libros = []                        # Libros de esta categoría
        self.padre = None                       # Referencia al padre
```

**Operaciones:**
- `agregar_subcategoria(nombre)`: O(1)
- `agregar_libro(libro)`: O(1)
- `buscar_categoria(nombre)`: O(n) con DFS/BFS
- `obtener_jerarquia()`: O(n) - Recorrido completo
- `obtener_libros_recursivo()`: Incluye subcategorías

---

### DECISIÓN 5: Min-Heap para Gestión de Préstamos por Vencimiento

**Justificación:**

Necesitamos identificar rápidamente los préstamos próximos a vencer:
- Acceder al préstamo más urgente: O(1)
- Insertar nuevo préstamo: O(log n)
- Eliminar préstamo vencido/devuelto: O(log n)

**Decisión:** Min-Heap con clave = fecha_vencimiento

**Estructura:**

```python
class HeapPrestamos:
    def __init__(self):
        self.heap = []  # Lista que representa el heap
    
    def insertar(self, prestamo):
        # Inserta y hace heapify up
        # Compara por fecha_vencimiento
    
    def extraer_minimo(self):
        # Retorna préstamo más próximo a vencer
    
    def obtener_minimo(self):
        # Solo consulta, no extrae
```

**Criterio de Comparación:**
```python
def comparar_prestamos(p1, p2):
    return p1.fecha_vencimiento < p2.fecha_vencimiento
```

---

### DECISIÓN 6: Trie para Autocompletado de Títulos de Libros

**Justificación:**

Para mejorar la experiencia del usuario con autocompletado:
- Usuario escribe "Don Q" → sugerencia "Don Quijote de la Mancha"
- Usuario escribe "Cien" → sugerencia "Cien años de soledad"

**Decisión:** Trie (Árbol de Prefijos)

**Ventajas Específicas:**
- Búsqueda de prefijos: O(m) donde m = longitud del prefijo
- Todas las palabras que empiezan con un prefijo
- Ideal para features de UI

**Estructura del Nodo:**

```python
class NodoTrie:
    def __init__(self):
        self.hijos = {}                  # Dict: caracter -> NodoTrie
        self.es_fin_palabra = False
        self.libro = None                # Libro completo si es fin
        self.frecuencia = 0              # Para ranking de sugerencias
```

**Operaciones:**
- `insertar_titulo(libro)`: O(m)
- `buscar_prefijo(prefijo)`: O(m)
- `autocompletar(prefijo, limite=10)`: O(m + k) donde k = resultados

---

## 📋 Resumen de Decisiones

| Estructura de Datos | Uso | Motivo de Selección | Complejidad Operaciones |
|-------------------|-----|---------------------|------------------------|
| **AVL Tree** | Búsqueda por ISBN | Lectura intensiva, garantía de O(log n) | Búsqueda: O(log n) |
| **AVL Tree** | Búsqueda por título | Orden alfabético, búsquedas frecuentes | Búsqueda: O(log n) |
| **AVL Tree** | Búsqueda de usuarios | Garantía de balance, inserciones secuenciales | Búsqueda: O(log n) |
| **Árbol N-ario** | Categorías jerárquicas | Estructura natural, subcategorías | DFS/BFS: O(n) |
| **Min-Heap** | Préstamos por vencimiento | Acceso rápido al mínimo, colas de prioridad | Acceso mín: O(1), Inserción: O(log n) |
| **Trie** | Autocompletado de títulos | Búsqueda de prefijos eficiente | Búsqueda: O(m) |

---

## 🔄 Compatibilidad con Sistema Actual

### Estrategia de Integración

**Patrón Adapter/Wrapper:**

```python
class GestorLibrosConArboles:
    def __init__(self):
        # Árboles paralelos indexando el mismo conjunto de libros
        self.arbol_isbn = ArbolAVL()        # Índice por ISBN
        self.arbol_titulo = ArbolAVL()       # Índice por título
        self.trie_titulos = Trie()           # Para autocompletado
        self.arbol_categorias = ArbolCategorias()
        
    def registrar_libro(self, libro):
        # Insertar en todos los índices
        self.arbol_isbn.insertar(libro, clave=libro.isbn)
        self.arbol_titulo.insertar(libro, clave=libro.titulo.lower())
        self.trie_titulos.insertar(libro.titulo, libro)
        self.arbol_categorias.agregar_libro(libro.categoria, libro)
    
    def buscar_por_isbn(self, isbn):
        return self.arbol_isbn.buscar(isbn)
    
    def buscar_por_titulo(self, titulo):
        return self.arbol_titulo.buscar(titulo.lower())
    
    def autocompletar(self, prefijo):
        return self.trie_titulos.autocompletar(prefijo)
```

### Sincronización de Estructuras

**Principio:** Un libro se mantiene en memoria una sola vez, los árboles mantienen referencias

```python
class Libro:
    def __init__(self, isbn, titulo, autor, categoria, año):
        self.isbn = isbn
        self.titulo = titulo
        self.autor = autor
        # ... otros atributos
        
# Los árboles solo almacenan referencias
arbol_isbn.insertar_referencia(libro)  # No duplica el objeto
arbol_titulo.insertar_referencia(libro)  # Misma referencia
```

---

## 🎨 Diagrama de Arquitectura Propuesta

```
┌─────────────────────────────────────────────────────────┐
│          SISTEMA DE GESTIÓN DE BIBLIOTECA               │
│                 (con Árboles - Unidad 2)                │
└─────────────────────────────────────────────────────────┘
                            │
        ┌───────────────────┴───────────────────┐
        │                                       │
┌───────▼─────────┐                    ┌───────▼────────┐
│  GESTIÓN LIBROS │                    │ GESTIÓN USUARIOS│
│   (Con Árboles) │                    │   (Con Árboles) │
└────┬──┬──┬──┬───┘                    └────┬────────────┘
     │  │  │  │                             │
     │  │  │  └─────────┐                   │
     │  │  │            │                   │
┌────▼──▼──▼──▼─────┐  │           ┌───────▼──────────┐
│  ÍNDICES LIBROS:   │  │           │ ÍNDICE USUARIOS: │
│  • AVL por ISBN    │  │           │ • AVL por ID     │
│  • AVL por Título  │  │           │ • AVL por email  │
│  • Trie (autocmpl) │  │           └──────────────────┘
└────────────────────┘  │
                        │
             ┌──────────▼─────────────┐
             │ ÁRBOL DE CATEGORÍAS    │
             │ (Árbol N-ario)         │
             │ • Ficción              │
             │   ├─ Ciencia Ficción   │
             │   └─ Fantasía          │
             │ • No Ficción           │
             │   ├─ Historia          │
             │   └─ Ciencia           │
             └────────────────────────┘

┌─────────────────────────────────────────────┐
│      GESTIÓN DE PRÉSTAMOS                   │
│      (con Min-Heap)                         │
└─────────┬───────────────────────────────────┘
          │
  ┌───────▼────────┐
  │  MIN-HEAP:     │
  │  • Por fecha   │
  │    vencimiento │
  │  • Acceso O(1) │
  │    al próximo  │
  │    a vencer    │
  └────────────────┘

┌──────────────────────────────────────────────┐
│     ESTRUCTURAS LINEALES MANTENIDAS          │
│     (de la Unidad 1)                         │
├──────────────────────────────────────────────┤
│  • Pila: Historial reciente                  │
│  • Cola: Solicitudes pendientes              │
└──────────────────────────────────────────────┘
```

---

## 📊 Comparación de Rendimiento Esperado

### Escenario: 10,000 Libros y 1,000 Usuarios

| Operación | Estructura Actual | Tiempo Actual | Estructura Nueva | Tiempo Esperado | Mejora |
|-----------|------------------|---------------|------------------|-----------------|--------|
| Buscar libro por ISBN | Lista Enlazada | O(n) = ~5,000 ops | AVL Tree | O(log n) = ~14 ops | **357x** |
| Buscar libro por título | Lista Enlazada | O(n) = ~5,000 ops | AVL Tree | O(log n) = ~14 ops | **357x** |
| Buscar usuario por ID | Arreglo | O(n) = ~500 ops | AVL Tree | O(log n) = ~10 ops | **50x** |
| Autocompletar título | Lista Enlazada | O(n) = ~5,000 ops | Trie | O(m) = ~10 ops | **500x** |
| Préstamo más urgente | Iterar todos | O(n) = ~1,000 ops | Min-Heap | O(1) = 1 op | **1,000x** |
| Libros de categoría | Filtrar todos | O(n) = ~5,000 ops | Árbol Cat. | O(k) = ~50 ops | **100x** |

**Nota:** "ops" = operaciones de comparación aproximadas

---

## 🧪 Plan de Validación

### Pruebas de Rendimiento

```python
class TestRendimientoArboles(unittest.TestCase):
    def test_comparacion_busqueda_libro(self):
        # Comparar búsqueda en Lista vs AVL
        # Medir tiempo para 1000 búsquedas
        pass
    
    def test_comparacion_insercion_masiva(self):
        # Insertar 10,000 libros
        # Comparar tiempo Lista vs AVL
        pass
    
    def test_heap_prestamos_urgentes(self):
        # Verificar que min-heap retorna préstamos en orden
        pass
```

### Pruebas de Correctitud

```python
class TestCorrecitudArboles(unittest.TestCase):
    def test_avl_balance(self):
        # Verificar que el árbol se mantiene balanceado
        pass
    
    def test_busqueda_isbn_exacta(self):
        # Verificar que la búsqueda retorna el libro correcto
        pass
    
    def test_trie_autocompletado(self):
        # Verificar sugerencias correctas
        pass
```

---

## 📝 Justificación Académica

### Aplicación de Conceptos Teóricos

1. **AVL Trees (Adelson-Velsky y Landis, 1962)**
   - Factor de balance: -1, 0, +1
   - Rotaciones: Simple (LL, RR), Doble (LR, RL)
   - Altura máxima: 1.44 * log₂(n)

2. **Heaps (Williams, 1964)**
   - Propiedad de heap: padre ≤/≥ hijos
   - Representación en array: hijo_izq = 2*i+1
   - Aplicación en colas de prioridad

3. **Tries (Fredkin, 1960)**
   - Retrieval tree
   - Búsqueda por prefijo sin comparaciones
   - Aplicación en autocompletado

### Complejidad Temporal

| Operación | Lista Enlazada | AVL | Trie | Heap |
|-----------|---------------|-----|------|------|
| Búsqueda | O(n) | O(log n) | O(m) | O(n) |
| Inserción | O(1) | O(log n) | O(m) | O(log n) |
| Eliminación | O(n) | O(log n) | O(m) | O(log n) |
| Máximo/Mínimo | O(n) | O(log n) | N/A | O(1) |

---

## 🎯 Conclusiones de la Fase 2

### Decisiones Técnicas

1. **AVL Trees:** Seleccionados para todas las búsquedas por clave única (ISBN, título, ID usuario)
2. **Min-Heap:** Seleccionado para gestión de préstamos por fecha de vencimiento
3. **Trie:** Seleccionado para autocompletado de títulos
4. **Árbol N-ario:** Seleccionado para jerarquía de categorías

### Impacto Esperado

- **Rendimiento:** Mejora de 50x a 1000x en operaciones críticas
- **Escalabilidad:** Sistema puede manejar 100x más datos con rendimiento similar
- **Experiencia de Usuario:** Autocompletado y búsquedas instantáneas

### Preparación para Fase 3

Con las estructuras de árbol seleccionadas y justificadas, la siguiente fase consistirá en:

1. Implementar las clases de árboles
2. Desarrollar operaciones básicas (insertar, buscar, eliminar)
3. Implementar operaciones especializadas (autocompletado, balance, etc.)
4. Crear pruebas unitarias para cada estructura

---

**Fecha de Finalización de Fase 2:** Octubre 27, 2025  
**Estado:** ✅ COMPLETADO  
**Siguiente Fase:** Implementación de Estructuras de Árbol

---

*Documentación generada para el proyecto de Estructuras de Datos - Unidad 2*  
*Sistema de Gestión de Biblioteca Virtual*
