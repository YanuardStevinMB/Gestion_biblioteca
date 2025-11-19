# INFORME DE PROYECTO
## SISTEMA DE GESTIÓN DE BIBLIOTECA IMPLEMENTANDO ESTRUCTURAS DE DATOS LINEALES

---

## PORTADA

**UNIVERSIDAD:** [Nombre de la Universidad]  
**FACULTAD:** [Facultad correspondiente]  
**PROGRAMA:** [Programa académico]  
**ASIGNATURA:** Estructuras de Datos  
**UNIDAD:** Unidad 1 - Estructuras de Datos Lineales  

**TÍTULO DEL PROYECTO:**  
Sistema de Gestión de Biblioteca Implementando Estructuras de Datos Lineales

**ESTUDIANTE(S):**  
[Tu nombre completo]  
[Código estudiantil]

**DOCENTE:**  
[Nombre del docente]

**FECHA:**  
[Fecha de entrega]

---

## TABLA DE CONTENIDO

1. [INTRODUCCIÓN](#introducción)
2. [DESARROLLO DEL TEMA](#desarrollo-del-tema)
   - 2.1 [Marco Teórico](#marco-teórico)
   - 2.2 [Diseño del Sistema](#diseño-del-sistema)
   - 2.3 [Implementación](#implementación)
   - 2.4 [Explicación del Código](#explicación-del-código)
3. [PROTOTIPO FUNCIONAL](#prototipo-funcional)
4. [USO Y RELACIÓN DE CONCEPTOS](#uso-y-relación-de-conceptos)
5. [CONCLUSIONES](#conclusiones)
6. [REFERENCIAS](#referencias)

---

## INTRODUCCIÓN

Las estructuras de datos lineales constituyen uno de los fundamentos más importantes en la programación y el desarrollo de software. Su comprensión y aplicación práctica es esencial para la formación de profesionales en el área de tecnología e informática. El presente proyecto implementa un **Sistema de Gestión de Biblioteca** que demuestra el uso práctico de cuatro estructuras de datos lineales fundamentales: lista enlazada, arreglo dinámico, pila y cola.

### Objetivos

#### Objetivo General
Desarrollar un sistema funcional de gestión de biblioteca que implemente estructuras de datos lineales para demostrar su aplicación práctica en la resolución de problemas reales.

#### Objetivos Específicos
- Implementar desde cero las estructuras de datos lineales: lista enlazada, pila, cola y arreglo dinámico
- Diseñar un sistema que aproveche las ventajas específicas de cada estructura
- Crear una interfaz gráfica intuitiva para la interacción con el usuario
- Validar el funcionamiento correcto mediante un sistema de pruebas exhaustivas
- Documentar las decisiones de diseño y su justificación técnica

### Alcance
El proyecto abarca la implementación completa de un sistema de gestión bibliotecaria con funcionalidades de registro, búsqueda, préstamo y devolución de libros, gestión de usuarios, y generación de estadísticas en tiempo real.

### Metodología
Se utilizó un enfoque de desarrollo incremental, implementando primero las estructuras de datos fundamentales, luego las clases del dominio del problema, seguido de la lógica de negocio, la interfaz gráfica, y finalmente el sistema de pruebas y validaciones.

---

## DESARROLLO DEL TEMA

### 2.1 Marco Teórico

#### 2.1.1 Estructuras de Datos Lineales

Las estructuras de datos lineales son aquellas en las que los elementos se organizan de manera secuencial, donde cada elemento tiene un predecesor y un sucesor únicos, excepto el primer y último elemento (Ayala San Martín, 2020).

##### Lista Enlazada
Una lista enlazada es una estructura de datos dinámica donde cada elemento (nodo) contiene datos y una referencia al siguiente elemento. Según Fritelli et al. (2020), las listas enlazadas ofrecen ventajas en operaciones de inserción y eliminación, especialmente cuando estas operaciones se realizan frecuentemente al inicio de la estructura.

**Características principales:**
- Tamaño dinámico
- Inserción O(1) al inicio
- Eliminación eficiente
- Mayor uso de memoria por referencias

##### Arreglo Dinámico
Un arreglo dinámico es una estructura que combina las ventajas del acceso aleatorio de los arreglos tradicionales con la capacidad de crecimiento dinámico. Permite redimensionamiento automático cuando se alcanza la capacidad máxima (Fritelli et al., 2020).

**Características principales:**
- Acceso aleatorio O(1)
- Redimensionamiento automático
- Localidad de referencia
- Operaciones de inserción O(1) amortizado

##### Pila (Stack)
Una pila es una estructura LIFO (Last In, First Out) donde los elementos se insertan y eliminan por el mismo extremo, llamado tope. Es fundamental para el manejo de llamadas a funciones, evaluación de expresiones y algoritmos de backtracking (Ayala San Martín, 2020).

**Operaciones principales:**
- `push()`: Insertar elemento en el tope
- `pop()`: Eliminar elemento del tope
- `top()`: Ver elemento del tope sin eliminarlo
- `isEmpty()`: Verificar si está vacía

##### Cola (Queue)
Una cola implementa la política FIFO (First In, First Out), donde los elementos se insertan por un extremo (final) y se eliminan por el otro (frente). Es esencial en sistemas de procesamiento por turnos y algoritmos de recorrido de grafos (Fritelli et al., 2020).

**Operaciones principales:**
- `enqueue()`: Insertar elemento al final
- `dequeue()`: Eliminar elemento del frente
- `front()`: Ver elemento del frente
- `isEmpty()`: Verificar si está vacía

#### 2.1.2 Análisis de Complejidad Computacional

La eficiencia de las operaciones en cada estructura es crucial para la toma de decisiones de diseño:

| Estructura | Inserción | Búsqueda | Eliminación | Acceso |
|------------|-----------|----------|-------------|---------|
| Lista Enlazada | O(1)* | O(n) | O(n) | O(n) |
| Arreglo Dinámico | O(1)** | O(n) | O(n) | O(1) |
| Pila | O(1) | O(n) | O(1) | O(1) |
| Cola | O(1) | O(n) | O(1) | O(1) |

*Al inicio de la lista  
**Amortizado

### 2.2 Diseño del Sistema

#### 2.2.1 Arquitectura General

El sistema sigue un patrón de arquitectura en capas:

1. **Capa de Estructuras de Datos**: Implementaciones personalizadas de las estructuras lineales
2. **Capa de Modelos**: Clases que representan las entidades del dominio
3. **Capa de Lógica de Negocio**: Gestor principal que coordina las operaciones
4. **Capa de Presentación**: Interfaz gráfica de usuario
5. **Capa de Pruebas**: Sistema de validación y testing

#### 2.2.2 Justificación del Uso de Estructuras

La selección de cada estructura de datos se basó en el análisis de los patrones de uso específicos:

**Lista Enlazada para Libros:**
- Razón: El catálogo de libros requiere inserción y eliminación frecuente
- Ventaja: Operaciones de modificación eficientes sin necesidad de reubicación
- Uso: Almacenamiento del inventario completo de libros

**Arreglo Dinámico para Usuarios:**
- Razón: Los usuarios requieren acceso frecuente por índice
- Ventaja: Acceso O(1) y redimensionamiento automático
- Uso: Base de datos de usuarios con consultas rápidas

**Pila para Historial de Préstamos:**
- Razón: Importancia de los préstamos más recientes para auditoría
- Ventaja: Acceso inmediato a la última transacción
- Uso: Seguimiento de actividad reciente del sistema

**Cola para Solicitudes Pendientes:**
- Razón: Procesamiento justo por orden de llegada
- Ventaja: Garantiza equidad en el sistema de reservas
- Uso: Lista de espera para libros no disponibles

### 2.3 Implementación

#### 2.3.1 Módulos del Sistema

El sistema se compone de cinco módulos principales:

1. **estructuras_datos.py**: Implementaciones de las estructuras lineales
2. **modelos.py**: Clases Libro, Usuario, Préstamo y gestor principal
3. **interfaz_grafica.py**: Interfaz de usuario con Tkinter
4. **pruebas_sistema.py**: Sistema completo de testing
5. **main.py**: Punto de entrada y coordinación general

#### 2.3.2 Patrón de Diseño Utilizado

Se implementó el patrón **Manager** (Gestor) donde la clase `BibliotecaManager` centraliza todas las operaciones y mantiene la consistencia del estado del sistema.

### 2.4 Explicación del Código

#### 2.4.1 Implementación de Lista Enlazada

```python
class ListaEnlazada:
    def __init__(self):
        self.cabeza = None
        self.tamaño = 0
    
    def insertar_al_inicio(self, dato):
        """Inserta un elemento al inicio de la lista en O(1)"""
        nuevo_nodo = Nodo(dato)
        nuevo_nodo.siguiente = self.cabeza
        self.cabeza = nuevo_nodo
        self.tamaño += 1
```

**Explicación:** La inserción al inicio es O(1) porque no requiere recorrer la lista. Se crea un nuevo nodo, se establece su referencia al nodo actual de la cabeza, y se actualiza la cabeza al nuevo nodo.

#### 2.4.2 Implementación de Arreglo Dinámico

```python
class ArregloDinamico:
    def __init__(self, capacidad_inicial=10):
        self.capacidad = capacidad_inicial
        self.tamaño = 0
        self.datos = [None] * self.capacidad
    
    def _redimensionar(self):
        """Duplica la capacidad cuando es necesario"""
        nueva_capacidad = self.capacidad * 2
        nuevo_arreglo = [None] * nueva_capacidad
        for i in range(self.tamaño):
            nuevo_arreglo[i] = self.datos[i]
        self.datos = nuevo_arreglo
        self.capacidad = nueva_capacidad
```

**Explicación:** El redimensionamiento dinámico permite crecimiento automático. Se duplica la capacidad para amortizar el costo de las operaciones futuras, manteniendo un factor de carga eficiente.

#### 2.4.3 Implementación de Pila

```python
class Pila:
    def apilar(self, dato):
        """Agrega un elemento al tope de la pila"""
        nuevo_nodo = Nodo(dato)
        nuevo_nodo.siguiente = self.tope
        self.tope = nuevo_nodo
        self.tamaño += 1
    
    def desapilar(self):
        """Remueve y retorna el elemento del tope"""
        if self.esta_vacia():
            return None
        dato = self.tope.dato
        self.tope = self.tope.siguiente
        self.tamaño -= 1
        return dato
```

**Explicación:** La pila mantiene el principio LIFO utilizando una lista enlazada donde el tope apunta al primer nodo. Las operaciones son O(1) al trabajar solo con el primer elemento.

#### 2.4.4 Implementación de Cola

```python
class Cola:
    def encolar(self, dato):
        """Agrega un elemento al final de la cola"""
        nuevo_nodo = Nodo(dato)
        if self.esta_vacia():
            self.frente = self.final = nuevo_nodo
        else:
            self.final.siguiente = nuevo_nodo
            self.final = nuevo_nodo
        self.tamaño += 1
```

**Explicación:** La cola mantiene referencias tanto al frente como al final para permitir operaciones O(1) en ambos extremos, cumpliendo el principio FIFO.

#### 2.4.5 Sistema de Gestión Principal

```python
class BibliotecaManager:
    def __init__(self):
        self.libros = ListaEnlazada()          # Para catálogo dinámico
        self.usuarios = ArregloDinamico()      # Para acceso indexado
        self.historial_prestamos = Pila()     # Para auditoría LIFO
        self.cola_solicitudes = Cola()        # Para procesamiento FIFO
```

**Explicación:** El gestor principal integra todas las estructuras, cada una optimizada para su uso específico en el contexto del sistema bibliotecario.

---

## PROTOTIPO FUNCIONAL

### 3.1 Descripción del Prototipo

El prototipo desarrollado es un sistema completamente funcional que demuestra la aplicación práctica de las estructuras de datos lineales en un contexto real. El sistema incluye:

### 3.2 Funcionalidades Implementadas

#### 3.2.1 Gestión de Libros
- **Registro de libros**: Permite agregar nuevos libros con ISBN, título, autor, categoría y año
- **Búsqueda multicriterio**: Búsqueda por título, autor, categoría o ISBN
- **Control de disponibilidad**: Seguimiento automático del estado de préstamo
- **Eliminación controlada**: Remoción de libros del catálogo con validaciones

#### 3.2.2 Gestión de Usuarios
- **Registro de usuarios**: Creación de perfiles con validación de email único
- **Consultas eficientes**: Búsqueda por nombre, email o ID de usuario
- **Historial personal**: Seguimiento de préstamos por usuario
- **Estadísticas individuales**: Contadores de préstamos activos

#### 3.2.3 Sistema de Préstamos
- **Procesamiento automático**: Validaciones de disponibilidad y existencia
- **Control temporal**: Gestión de fechas de vencimiento (14 días configurables)
- **Estados dinámicos**: Seguimiento de préstamos activos, devueltos y vencidos
- **Historial LIFO**: Acceso rápido a transacciones recientes

#### 3.2.4 Cola de Solicitudes
- **Procesamiento FIFO**: Manejo justo de solicitudes por orden de llegada
- **Lista de espera**: Sistema de reservas para libros no disponibles
- **Procesamiento automático**: Asignación automática cuando el libro esté disponible

### 3.3 Interfaz de Usuario

#### 3.3.1 Interfaz Gráfica
- **Panel de estadísticas**: Métricas en tiempo real del sistema
- **Navegación por pestañas**: Organización intuitiva de funcionalidades
- **Tablas interactivas**: Visualización de datos con scroll y ordenamiento
- **Formularios validados**: Entrada de datos con verificación automática

#### 3.3.2 Interfaz de Consola
- **Menú interactivo**: Navegación textual para usuarios avanzados
- **Comandos directos**: Ejecución de operaciones específicas
- **Feedback inmediato**: Respuestas claras sobre el resultado de operaciones

### 3.4 Sistema de Validación

#### 3.4.1 Pruebas Unitarias
El sistema incluye 11 pruebas automatizadas que validan:
- Operaciones básicas de cada estructura de datos
- Comportamientos LIFO y FIFO correctos
- Funcionalidad de redimensionamiento automático
- Integridad de los modelos de datos
- Flujos completos de préstamo y devolución

#### 3.4.2 Validaciones de Integridad
- **Unicidad de ISBNs**: Prevención de duplicados en el catálogo
- **Emails únicos**: Validación de usuarios sin duplicación
- **Estados consistentes**: Verificación de disponibilidad de libros
- **Fechas válidas**: Control de vencimientos y cálculos temporales

### 3.5 Datos de Demostración

El sistema incluye datos precargados para facilitar la evaluación:
- **5 libros clásicos** de diferentes géneros y épocas
- **3 usuarios de ejemplo** con diferentes perfiles
- **Estadísticas iniciales** que demuestran el estado del sistema

---

## USO Y RELACIÓN DE CONCEPTOS

### 4.1 Aplicación de Conceptos Teóricos

#### 4.1.1 Selección Basada en Patrones de Uso

La selección de estructuras de datos se fundamentó en el análisis de patrones de acceso específicos del dominio bibliotecario:

**Análisis de Frecuencia de Operaciones:**
- Libros: Alta frecuencia de inserción/eliminación → Lista Enlazada
- Usuarios: Alta frecuencia de acceso aleatorio → Arreglo Dinámico  
- Historial: Necesidad de acceso a elementos recientes → Pila
- Solicitudes: Procesamiento por orden de llegada → Cola

#### 4.1.2 Trade-offs Considerados

**Memoria vs Velocidad:**
- Lista enlazada: Mayor uso de memoria por punteros, pero inserción O(1)
- Arreglo dinámico: Desperdicio de espacio por capacidad extra, pero acceso O(1)

**Simplicidad vs Eficiencia:**
- Implementaciones propias vs bibliotecas estándar
- Control total sobre comportamiento vs desarrollo más rápido

#### 4.1.3 Principios de Diseño Aplicados

**Encapsulación:**
Cada estructura de datos encapsula su implementación, exponiendo solo las operaciones necesarias.

**Separación de Responsabilidades:**
- Estructuras de datos: Gestión de almacenamiento
- Modelos: Representación del dominio
- Gestor: Lógica de negocio
- Interfaz: Presentación

**Reutilización:**
Las estructuras implementadas son genéricas y reutilizables en otros contextos.

### 4.2 Demostración de Conceptos Clave

#### 4.2.1 Complejidad Computacional
El proyecto demuestra prácticamente las diferencias de rendimiento:
- Acceso O(1) en arreglos vs O(n) en listas
- Inserción O(1) en pilas/colas vs estructuras más complejas
- Redimensionamiento amortizado en arreglos dinámicos

#### 4.2.2 Gestión de Memoria
- Asignación dinámica en listas enlazadas
- Reutilización de espacio en arreglos
- Liberación automática por garbage collection

#### 4.2.3 Invariantes de Estructura
- LIFO mantenido consistentemente en pilas
- FIFO preservado en colas
- Integridad de enlaces en listas
- Factores de carga en arreglos dinámicos

### 4.3 Parametrización de Datos

#### 4.3.1 Configurabilidad del Sistema
```python
# Ejemplos de parametrización implementada
prestamo = Prestamo(id_prestamo, isbn, usuario, dias_prestamo=14)
arreglo = ArregloDinamico(capacidad_inicial=10)
```

#### 4.3.2 Flexibilidad de Criterios
```python
# Búsquedas parametrizadas por función lambda
libros.buscar(lambda libro: "García Márquez" in libro.autor)
usuarios.buscar(lambda usuario: usuario.prestamos_activos > 0)
```

---

## CONCLUSIONES

### 5.1 Aprendizajes Obtenidos

#### 5.1.1 Comprensión Profunda de Estructuras Lineales
El desarrollo del proyecto permitió una comprensión práctica de cómo las estructuras de datos teóricas se aplican en problemas reales. La implementación desde cero reveló la importancia de cada detalle en el diseño de estas estructuras fundamentales.

#### 5.1.2 Importancia de la Selección Apropiada
Se evidenció que la elección de la estructura de datos correcta puede impactar significativamente el rendimiento y la mantenibilidad del sistema. Cada estructura tiene su nicho específico donde ofrece ventajas únicas.

#### 5.1.3 Integración de Múltiples Estructuras
El proyecto demostró cómo diferentes estructuras pueden trabajar en conjunto dentro de un mismo sistema, cada una optimizada para su caso de uso específico, creando una solución completa y eficiente.

#### 5.1.4 Desarrollo de Habilidades de Diseño
Se adquirió experiencia práctica en:
- Análisis de requisitos y patrones de uso
- Diseño de arquitectura modular
- Implementación de interfaces consistentes
- Validación mediante pruebas automatizadas

### 5.2 Dificultades Encontradas

#### 5.2.1 Gestión de Referencias en Listas Enlazadas
La implementación de operaciones de eliminación en listas enlazadas requirió cuidado especial para mantener la integridad de los enlaces y evitar referencias perdidas.

**Solución aplicada:** Implementación de métodos auxiliares que manejan casos especiales como eliminación del primer elemento y actualización correcta de referencias.

#### 5.2.2 Redimensionamiento Eficiente de Arreglos
El balance entre uso de memoria y rendimiento en arreglos dinámicos presentó desafíos en la estrategia de crecimiento.

**Solución aplicada:** Implementación de duplicación de capacidad que amortiza el costo de redimensionamiento manteniendo eficiencia en operaciones frecuentes.

#### 5.2.3 Sincronización de Estados
Mantener la consistencia entre diferentes estructuras que almacenan información relacionada requirió diseño cuidadoso.

**Solución aplicada:** Centralización de operaciones en la clase BibliotecaManager que garantiza actualizaciones consistentes en todas las estructuras afectadas.

#### 5.2.4 Diseño de Interfaz Intuitiva
Crear una interfaz que sea tanto funcional como educativa para demostrar el uso de las estructuras presentó desafíos de diseño de UX.

**Solución aplicada:** Implementación de múltiples modos de interacción (gráfico, consola, pruebas) que se adaptan a diferentes necesidades de uso.

### 5.3 Mejoras Posibles

#### 5.3.1 Optimizaciones de Rendimiento
- **Índices de búsqueda**: Implementación de estructuras auxiliares para búsquedas más rápidas
- **Cache de consultas**: Almacenamiento temporal de resultados de búsquedas frecuentes
- **Paginación**: Manejo eficiente de grandes volúmenes de datos

#### 5.3.2 Funcionalidades Adicionales
- **Persistencia de datos**: Integración con base de datos para almacenamiento permanente
- **Sistema de notificaciones**: Alertas automáticas para vencimientos y reservas
- **Reportes avanzados**: Generación de estadísticas y reportes exportables
- **API REST**: Interfaz programática para integración con otros sistemas

#### 5.3.3 Estructuras de Datos Avanzadas
- **Árboles de búsqueda**: Para optimización de consultas complejas
- **Tablas hash**: Para acceso O(1) a elementos por clave
- **Heap**: Para manejo de prioridades en solicitudes
- **Grafo**: Para sistemas de recomendaciones

#### 5.3.4 Aspectos de Producción
- **Manejo de concurrencia**: Soporte para múltiples usuarios simultáneos
- **Seguridad**: Autenticación y autorización de usuarios
- **Logging**: Sistema de auditoría completo
- **Configuración**: Parámetros ajustables sin modificar código

### 5.4 Impacto Académico

#### 5.4.1 Consolidación de Conocimientos
El proyecto sirvió como puente entre la teoría vista en clase y la aplicación práctica, consolidando conceptos fundamentales de estructuras de datos.

#### 5.4.2 Desarrollo de Competencias
- **Programación**: Implementación de algoritmos complejos
- **Diseño**: Arquitectura de software modular
- **Testing**: Desarrollo orientado por pruebas
- **Documentación**: Comunicación técnica efectiva

#### 5.4.3 Preparación Profesional
El proyecto proporcionó experiencia práctica en el tipo de decisiones de diseño y implementación que enfrentan los desarrolladores profesionales.

### 5.5 Reflexiones Finales

La implementación de este sistema de gestión de biblioteca ha demostrado que las estructuras de datos lineales, aunque conceptualmente simples, son herramientas poderosas cuando se aplican apropiadamente. El proyecto evidencia la importancia del análisis cuidadoso de requisitos y patrones de uso para la selección de estructuras de datos.

La experiencia obtenida trasciende el ámbito académico, proporcionando habilidades prácticas en diseño de software, implementación de algoritmos y desarrollo de interfaces de usuario que serán valiosas en el desarrollo profesional futuro.

El éxito del proyecto radica no solo en su funcionamiento correcto, sino en la comprensión profunda adquirida sobre cómo las decisiones de diseño impactan el rendimiento, mantenibilidad y escalabilidad de los sistemas de software.

---

## REFERENCIAS

Ayala San Martín, G. (2020). *Algoritmos y programación: mejores prácticas*. Fundación Universidad de las Américas Puebla (UDLAP).

Fritelli, V., Guzmán, A., & Tymoschuk, J. (2020). *Algoritmos y estructuras de datos* (2a. ed.). Jorge Sarmiento Editor - Universitas.

Knuth, D. E. (2011). *The Art of Computer Programming, Volume 1: Fundamental Algorithms* (3rd ed.). Addison-Wesley Professional.

Ruiz Rodríguez, R. (2009). *Fundamentos de la programación orientada a objetos: una aplicación a las estructuras de datos en Java*. El Cid Editor.

Sedgewick, R., & Wayne, K. (2011). *Algorithms* (4th ed.). Addison-Wesley Professional.

Weiss, M. A. (2012). *Data Structures and Algorithm Analysis in Java* (3rd ed.). Pearson Education.

Zohenero Martínez, I., & Joyanes Aguilar, L. (2008). *Estructuras de datos en Java*. McGraw-Hill España.

---

## ANEXOS

### Anexo A: Código Fuente Completo
[El código fuente completo se encuentra en los archivos adjuntos del proyecto]

### Anexo B: Resultados de Pruebas
```
============================================================
RESUMEN DE PRUEBAS DEL SISTEMA
============================================================
Pruebas ejecutadas: 11
Exitosas: 11
Fallidas: 0
Errores: 0

🎉 TODAS LAS PRUEBAS PASARON EXITOSAMENTE
```

### Anexo C: Manual de Usuario
[Documentación detallada de uso disponible en README.md]

### Anexo D: Diagramas de Arquitectura
[Diagramas UML y de arquitectura del sistema]

---

*Este documento constituye el informe final del proyecto de implementación de estructuras de datos lineales, desarrollado como parte de los requisitos académicos de la Unidad 1 del curso de Estructuras de Datos.*