# FASE 1: ANÁLISIS Y EJECUCIÓN DEL PROYECTO EXISTENTE

## 📋 Información del Proyecto

**Asignatura:** Estructuras de Datos - Unidad 2  
**Tema:** Implementación de Estructuras de Datos No Lineales (Árboles)  
**Fecha de Análisis:** Octubre 2025  
**Autor:** Equipo de Desarrollo Biblioteca Virtual

---

## 🎯 Objetivo de la Fase 1

Revisar, analizar y comprender el código actual del Sistema de Gestión de Biblioteca desarrollado en la Unidad 1, que utiliza estructuras de datos lineales. Este análisis servirá como base para identificar las operaciones que pueden ser optimizadas mediante estructuras de datos no lineales (árboles).

---

## 📁 Estructura del Proyecto Actual

```
biblioteca/
├── estructuras_datos.py       # Implementaciones de estructuras lineales
├── modelos.py                 # Clases del dominio (Libro, Usuario, Préstamo)
├── interfaz_grafica.py        # Interfaz gráfica con Tkinter
├── pruebas_sistema.py         # Suite de pruebas unitarias
├── main.py                    # Punto de entrada principal
├── README.md                  # Documentación de la Unidad 1
├── INFORME_PROYECTO.md        # Informe técnico
└── INFORME_FINAL_WORD.md      # Informe final en formato Word
```

### Descripción de Archivos Principales

| Archivo | Líneas de Código | Descripción | Estructuras Utilizadas |
|---------|-----------------|-------------|----------------------|
| `estructuras_datos.py` | 345 | Implementación de estructuras lineales | Lista Enlazada, Pila, Cola, Arreglo Dinámico |
| `modelos.py` | 502 | Modelos de dominio y gestor principal | Utiliza todas las estructuras lineales |
| `interfaz_grafica.py` | ~800 | Interfaz gráfica completa | Tkinter, ttk |
| `pruebas_sistema.py` | 473 | Suite de pruebas | unittest |
| `main.py` | 361 | Punto de entrada y modos de ejecución | argparse |

---

## 🔍 Análisis del Código Actual

### 1. Estructuras de Datos Lineales Implementadas

#### **1.1 Lista Enlazada Simple** (`estructuras_datos.py`: líneas 29-114)

```python path=C:\Users\yanuard.montialegre\Documents\UNIVERCIDAD_PROJECTO\biblioteca\biblioteca\estructuras_datos.py start=29
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
```

**Uso Actual:** Gestión del catálogo de libros  
**Complejidad:**
- Inserción al inicio: O(1)
- Inserción al final: O(n)
- Búsqueda: O(n)
- Eliminación: O(n)

**Limitación Identificada:** La búsqueda lineal es ineficiente para catálogos grandes. Un árbol de búsqueda binaria (BST) podría reducir la complejidad a O(log n).

---

#### **1.2 Arreglo Dinámico** (`estructuras_datos.py`: líneas 234-345)

```python path=C:\Users\yanuard.montialegre\Documents\UNIVERCIDAD_PROJECTO\biblioteca\biblioteca\estructuras_datos.py start=234
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
```

**Uso Actual:** Gestión de usuarios registrados  
**Complejidad:**
- Acceso por índice: O(1)
- Búsqueda: O(n)
- Inserción al final: O(1) amortizado
- Eliminación: O(n)

**Limitación Identificada:** La búsqueda de usuarios por ID o email requiere O(n). Un árbol AVL o BST indexado podría mejorar esto.

---

#### **1.3 Pila (LIFO)** (`estructuras_datos.py`: líneas 116-171)

```python path=C:\Users\yanuard.montialegre\Documents\UNIVERCIDAD_PROJECTO\biblioteca\biblioteca\estructuras_datos.py start=116
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
```

**Uso Actual:** Historial de préstamos recientes  
**Complejidad:** Todas las operaciones principales son O(1)

**Observación:** Esta estructura es adecuada para su propósito. No requiere modificación inmediata.

---

#### **1.4 Cola (FIFO)** (`estructuras_datos.py`: líneas 172-232)

```python path=C:\Users\yanuard.montialegre\Documents\UNIVERCIDAD_PROJECTO\biblioteca\biblioteca\estructuras_datos.py start=172
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
```

**Uso Actual:** Gestión de solicitudes pendientes de préstamos  
**Complejidad:** Todas las operaciones principales son O(1)

**Observación:** Implementación correcta y eficiente para su propósito.

---

### 2. Modelos de Dominio

#### **2.1 Clase Libro** (`modelos.py`: líneas 20-64)

```python path=C:\Users\yanuard.montialegre\Documents\UNIVERCIDAD_PROJECTO\biblioteca\biblioteca\modelos.py start=20
class Libro:
    """
    Clase que representa un libro en el sistema de biblioteca.
    
    Atributos:
        isbn: Código ISBN único del libro
        titulo: Título del libro
        autor: Autor del libro
        categoria: Categoría o género del libro
        año_publicacion: Año de publicación
        disponible: Estado de disponibilidad (True/False)
        fecha_registro: Fecha cuando se registró en el sistema
    """
    
    def __init__(self, isbn, titulo, autor, categoria, año_publicacion):
        self.isbn = isbn
        self.titulo = titulo
        self.autor = autor
        self.categoria = categoria
        self.año_publicacion = año_publicacion
        self.disponible = True
        self.fecha_registro = datetime.now()
```

**Atributos Clave para Indexación:**
- `isbn`: Identificador único (puede ser clave primaria en árbol)
- `titulo`: Útil para búsqueda alfabética
- `autor`: Permite agrupar libros por autor
- `categoria`: Categorización jerárquica natural

---

#### **2.2 Clase Usuario** (`modelos.py`: líneas 66-108)

```python path=C:\Users\yanuard.montialegre\Documents\UNIVERCIDAD_PROJECTO\biblioteca\biblioteca\modelos.py start=66
class Usuario:
    """
    Clase que representa un usuario de la biblioteca.
    
    Atributos:
        id_usuario: Identificador único del usuario
        nombre: Nombre completo del usuario
        email: Correo electrónico del usuario
        telefono: Número de teléfono
        fecha_registro: Fecha de registro en el sistema
        prestamos_activos: Número de préstamos activos
        historial_prestamos: Lista de préstamos realizados
    """
    
    def __init__(self, id_usuario, nombre, email, telefono):
        self.id_usuario = id_usuario
        self.nombre = nombre
        self.email = email
        self.telefono = telefono
        self.fecha_registro = datetime.now()
        self.prestamos_activos = 0
        self.historial_prestamos = []
```

**Atributos Clave para Indexación:**
- `id_usuario`: Identificador secuencial (U001, U002, ...)
- `email`: Debe ser único, buena clave para BST
- `nombre`: Útil para búsqueda alfabética

---

#### **2.3 Clase Préstamo** (`modelos.py`: líneas 110-168)

```python path=C:\Users\yanuard.montialegre\Documents\UNIVERCIDAD_PROJECTO\biblioteca\biblioteca\modelos.py start=110
class Prestamo:
    """
    Clase que representa un préstamo de libro.
    
    Atributos:
        id_prestamo: Identificador único del préstamo
        isbn_libro: ISBN del libro prestado
        id_usuario: ID del usuario que realiza el préstamo
        fecha_prestamo: Fecha del préstamo
        fecha_vencimiento: Fecha límite de devolución
        fecha_devolucion: Fecha real de devolución (None si está activo)
        estado: Estado del préstamo (activo, devuelto, vencido)
    """
    
    def __init__(self, id_prestamo, isbn_libro, id_usuario, dias_prestamo=14):
        self.id_prestamo = id_prestamo
        self.isbn_libro = isbn_libro
        self.id_usuario = id_usuario
        self.fecha_prestamo = datetime.now()
        self.fecha_vencimiento = self.fecha_prestamo + timedelta(days=dias_prestamo)
        self.fecha_devolucion = None
        self.estado = "activo"
```

**Atributos Clave:**
- `fecha_vencimiento`: Útil para heap o árbol de prioridad
- `id_prestamo`: Identificador único
- `estado`: Para filtrado y búsqueda

---

### 3. Gestor Principal: BibliotecaManager

#### **3.1 Inicialización** (`modelos.py`: líneas 170-196)

```python path=C:\Users\yanuard.montialegre\Documents\UNIVERCIDAD_PROJECTO\biblioteca\biblioteca\modelos.py start=181
def __init__(self):
    # Estructuras de datos principales
    self.libros = ListaEnlazada()          # Lista enlazada para libros
    self.usuarios = ArregloDinamico()      # Arreglo dinámico para usuarios
    self.historial_prestamos = Pila()     # Pila para historial reciente
    self.cola_solicitudes = Cola()        # Cola para solicitudes pendientes
    
    # Contadores para IDs únicos
    self.siguiente_id_usuario = 1
    self.siguiente_id_prestamo = 1
    
    # Préstamos activos (diccionario para búsqueda rápida)
    self.prestamos_activos = {}
    
    # Inicializar con datos de ejemplo
    self._inicializar_datos_ejemplo()
```

**Estructuras Utilizadas:**
1. `ListaEnlazada` → Para libros (buscar O(n))
2. `ArregloDinamico` → Para usuarios (buscar O(n))
3. `Pila` → Para historial (eficiente)
4. `Cola` → Para solicitudes (eficiente)
5. `dict` (Python nativo) → Para préstamos activos (buscar O(1))

---

#### **3.2 Operación de Búsqueda de Libros** (`modelos.py`: líneas 251-278)

```python path=C:\Users\yanuard.montialegre\Documents\UNIVERCIDAD_PROJECTO\biblioteca\biblioteca\modelos.py start=251
def buscar_libros(self, criterio="", valor=""):
    """
    Busca libros por diferentes criterios.
    
    Args:
        criterio: Tipo de búsqueda (titulo, autor, categoria, isbn)
        valor: Valor a buscar
        
    Returns:
        Lista de libros que coinciden con el criterio
    """
    if not criterio or not valor:
        return self.libros.obtener_todos()
    
    valor_lower = valor.lower()
    
    def buscar_por_criterio(libro):
        if criterio == "titulo":
            return valor_lower in libro.titulo.lower()
        elif criterio == "autor":
            return valor_lower in libro.autor.lower()
        elif criterio == "categoria":
            return valor_lower in libro.categoria.lower()
        elif criterio == "isbn":
            return valor_lower in libro.isbn.lower()
        return False
    
    return self.libros.buscar(buscar_por_criterio)
```

**Complejidad Actual:** O(n) - Búsqueda lineal en toda la lista

**Oportunidad de Mejora:** 
- Implementar un BST indexado por ISBN → O(log n)
- Implementar un árbol de búsqueda por título → O(log n)
- Usar un Trie para autocompletado de títulos

---

## 🧪 Resultados de las Pruebas del Sistema

### Ejecución de Pruebas

```bash
python main.py --tests
```

### Resultados

```
====================================================================
SISTEMA DE GESTIÓN DE BIBLIOTECA
     Implementación de Estructuras de Datos Lineales
====================================================================
Curso: Estructuras de Datos - Unidad 1
Fecha de ejecución: 27/10/2025 03:20:00
====================================================================

Ejecutando pruebas del sistema...
INICIANDO PRUEBAS DEL SISTEMA DE GESTIÓN DE BIBLIOTECA
============================================================

Ran 11 tests in 0.003s

============================================================
RESUMEN DE PRUEBAS
============================================================
Pruebas ejecutadas: 11
Exitosas: 11
Fallidas: 0
Errores: 0

🎉 TODAS LAS PRUEBAS PASARON EXITOSAMENTE
```

### Desglose de Pruebas

| Categoría | Pruebas | Estado | Tiempo |
|-----------|---------|--------|--------|
| Estructuras de Datos | 4 | ✅ Todas exitosas | 0.001s |
| Modelos de Dominio | 3 | ✅ Todas exitosas | 0.001s |
| Sistema Integrado | 4 | ✅ Todas exitosas | 0.001s |

#### Pruebas de Estructuras de Datos
1. ✅ `test_lista_enlazada_operaciones_basicas` - Inserción, búsqueda, eliminación
2. ✅ `test_pila_operaciones_lifo` - Comportamiento LIFO verificado
3. ✅ `test_cola_operaciones_fifo` - Comportamiento FIFO verificado
4. ✅ `test_arreglo_dinamico_operaciones` - Redimensionamiento y acceso indexado

#### Pruebas de Modelos
5. ✅ `test_libro_creacion_y_propiedades` - Creación y atributos de Libro
6. ✅ `test_usuario_creacion_y_propiedades` - Creación y atributos de Usuario
7. ✅ `test_prestamo_creacion_y_estados` - Estados y transiciones de Préstamo

#### Pruebas de Sistema
8. ✅ `test_registro_y_busqueda_libros` - Registro y búsqueda de libros
9. ✅ `test_registro_y_busqueda_usuarios` - Registro y búsqueda de usuarios
10. ✅ `test_sistema_prestamos_completo` - Préstamo y devolución completa
11. ✅ `test_estadisticas_sistema` - Cálculo de estadísticas

---

## 📊 Estado Actual del Sistema

### Datos Precargados

**Libros (5 libros):**
```
1. Cien años de soledad - Gabriel García Márquez (1967)
2. Don Quijote de la Mancha - Miguel de Cervantes (1605)
3. 1984 - George Orwell (1949)
4. El principito - Antoine de Saint-Exupéry (1943)
5. Crónica de una muerte anunciada - Gabriel García Márquez (1981)
```

**Usuarios (3 usuarios):**
```
1. Juan Pérez (U001) - juan.perez@email.com
2. María García (U002) - maria.garcia@email.com
3. Carlos López (U003) - carlos.lopez@email.com
```

### Estadísticas Actuales

```
Total de Libros................. 5
Libros Disponibles.............. 5
Libros Prestados................ 0
Total de Usuarios............... 3
Préstamos Activos............... 0
Solicitudes Pendientes.......... 0
```

---

## 🔍 Identificación de Operaciones para Optimizar con Árboles

### Operaciones Críticas Identificadas

| # | Operación | Estructura Actual | Complejidad Actual | Estructura Propuesta | Complejidad Esperada |
|---|-----------|-------------------|-------------------|---------------------|---------------------|
| 1 | Búsqueda de libros por ISBN | Lista Enlazada | O(n) | BST por ISBN | O(log n) |
| 2 | Búsqueda de libros por título | Lista Enlazada | O(n) | BST alfabético | O(log n) |
| 3 | Búsqueda de usuarios por ID | Arreglo Dinámico | O(n) | BST por ID | O(log n) |
| 4 | Búsqueda de usuarios por email | Arreglo Dinámico | O(n) | BST por email | O(log n) |
| 5 | Organización de libros por categoría | Lista Enlazada | O(n) | Árbol de categorías | O(log n) |
| 6 | Préstamos por fecha de vencimiento | Diccionario | O(n) para ordenar | Heap / Árbol de prioridad | O(log n) |
| 7 | Autocompletado de títulos | Lista Enlazada | O(n) | Trie | O(m) donde m = longitud |
| 8 | Rango de años de publicación | Lista Enlazada | O(n) | Árbol de intervalo | O(log n + k) |

---

## 🎯 Conclusiones de la Fase 1

### Hallazgos Principales

1. **Sistema Funcional:** El proyecto actual funciona correctamente con estructuras lineales. Todas las pruebas pasan exitosamente.

2. **Limitaciones de Rendimiento:** Las operaciones de búsqueda son O(n) en las estructuras principales (libros y usuarios), lo que puede ser ineficiente con grandes volúmenes de datos.

3. **Arquitectura Sólida:** La separación entre estructuras de datos, modelos de dominio y lógica de negocio facilita la integración de nuevas estructuras.

4. **Oportunidades de Optimización:** Múltiples operaciones pueden beneficiarse de estructuras de árbol:
   - Búsquedas más rápidas
   - Ordenamiento eficiente
   - Consultas por rango
   - Autocompletado

### Métricas del Código Actual

```
Total de líneas de código: ~2,481
- estructuras_datos.py: 345 líneas
- modelos.py: 502 líneas
- interfaz_grafica.py: ~800 líneas
- pruebas_sistema.py: 473 líneas
- main.py: 361 líneas

Cobertura de pruebas: 11 pruebas (100% exitosas)
Tiempo de ejecución de pruebas: 0.003 segundos
```

### Preparación para Fase 2

El análisis de la Fase 1 ha identificado claramente las áreas donde las estructuras de árbol pueden mejorar significativamente el rendimiento del sistema. En la siguiente fase, procederemos a:

1. Diseñar las estructuras de árbol apropiadas
2. Definir las interfaces y operaciones
3. Planificar la integración con el código existente

---

## 📝 Recomendaciones

### Compatibilidad con Código Existente

Para mantener la funcionalidad actual mientras agregamos árboles:

1. **Enfoque de Adaptador:** Crear clases wrapper que implementen las mismas interfaces que las estructuras lineales
2. **Pruebas de Regresión:** Mantener todas las pruebas existentes funcionando
3. **Migración Gradual:** Implementar árboles en paralelo antes de reemplazar estructuras lineales

### Próximos Pasos

1. ✅ **Fase 1 Completada:** Análisis y comprensión del código existente
2. ⏭️ **Fase 2:** Selección y diseño de estructuras de árbol
3. ⏭️ **Fase 3:** Implementación de las estructuras de árbol
4. ⏭️ **Fase 4:** Integración y pruebas
5. ⏭️ **Fase 5:** Documentación final y comparación de rendimiento

---

**Fecha de Finalización de Fase 1:** Octubre 27, 2025  
**Estado:** ✅ COMPLETADO  
**Siguiente Fase:** Comprensión del Modelo Actual e Identificación de Operaciones con Árboles

---

*Documentación generada para el proyecto de Estructuras de Datos - Unidad 2*  
*Sistema de Gestión de Biblioteca Virtual*
