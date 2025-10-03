# 📚 Sistema de Gestión de Biblioteca

## Implementación de Estructuras de Datos Lineales en Python

---

## 📋 Descripción del Proyecto

Este proyecto implementa un **Sistema de Gestión de Biblioteca** completo utilizando estructuras de datos lineales personalizadas (Lista Enlazada, Pila, Cola y Arreglo Dinámico). El sistema permite gestionar libros, usuarios y préstamos a través de una interfaz gráfica intuitiva desarrollada con Python y Tkinter.

### 🎯 Objetivos Académicos
- **Implementar** estructuras de datos lineales desde cero
- **Aplicar** conceptos teóricos en un proyecto real
- **Desarrollar** una interfaz de usuario funcional
- **Validar** el funcionamiento mediante pruebas exhaustivas

---

## 🛠️ Requisitos del Sistema

### Software Necesario
- **Python 3.7 o superior** (Recomendado: Python 3.9+)
- **Tkinter** (Incluido con Python en Windows)
- **Sistema Operativo**: Windows, macOS o Linux

### Verificar Instalación de Python
```bash
python --version
```
Debe mostrar algo como: `Python 3.x.x`

### Verificar Tkinter (Para la interfaz gráfica)
```bash
python -c "import tkinter; print('Tkinter está disponible')"
```

---

## 📁 Estructura del Proyecto

```
biblioteca/
├── estructuras_datos.py    # Implementaciones de Lista, Pila, Cola, Arreglo
├── modelos.py             # Clases Libro, Usuario, Préstamo, BibliotecaManager
├── interfaz_grafica.py    # Interfaz gráfica con Tkinter
├── pruebas_sistema.py     # Pruebas unitarias y de integración
├── main.py               # Archivo principal para ejecutar el sistema
└── README.md             # Esta documentación
```

### Descripción de Archivos

| Archivo | Descripción |
|---------|-------------|
| `estructuras_datos.py` | Implementaciones personalizadas de estructuras lineales |
| `modelos.py` | Clases del dominio: Libro, Usuario, Préstamo y gestor principal |
| `interfaz_grafica.py` | Interfaz gráfica completa con pestañas y tablas |
| `pruebas_sistema.py` | Sistema de pruebas para validar funcionamiento |
| `main.py` | Punto de entrada principal con múltiples modos de ejecución |

---

## 🚀 Instalación y Configuración

### 1. Descargar el Proyecto
Asegúrese de tener todos los archivos Python en el mismo directorio.

### 2. Verificar Dependencias
```bash
# Abrir terminal en el directorio del proyecto
cd "ruta\a\tu\proyecto\biblioteca"

# Verificar Python
python --version

# Verificar que puede importar los módulos
python -c "import tkinter; print('✅ Tkinter OK')"
```

### 3. Ejecutar Pruebas Iniciales
```bash
python main.py --tests
```
**Resultado esperado**: Todas las pruebas deben pasar (11/11 exitosas)

---

## 🎮 Cómo Usar el Sistema

### Opción 1: Interfaz Gráfica (Recomendada)
```bash
python main.py
```
o
```bash
python main.py --gui
```

**Características de la Interfaz:**
- Panel de estadísticas en tiempo real
- Pestañas organizadas por funcionalidad
- Tablas interactivas con scroll
- Formularios intuitivos para entrada de datos

### Opción 2: Modo Consola
```bash
python main.py --console
```

**Funciones disponibles:**
1. Mostrar estadísticas del sistema
2. Listar todos los libros
3. Listar todos los usuarios
4. Buscar libros por criterio
5. Realizar préstamos
6. Devolver libros
7. Ver préstamos activos

### Opción 3: Ejecutar Pruebas
```bash
python main.py --tests
```

### Opción 4: Ver Ayuda
```bash
python main.py --help
```

---

## 🏗️ Arquitectura y Estructuras de Datos

### 1. **Lista Enlazada** - Gestión de Libros
```python
# Usado para almacenar libros
# Permite inserción/eliminación eficiente
libros = ListaEnlazada()
libros.insertar_al_final(libro)
libros.buscar(criterio_busqueda)
```

**Ventajas:**
- Inserción O(1) al inicio
- Eliminación eficiente
- Memoria dinámica

### 2. **Arreglo Dinámico** - Gestión de Usuarios
```python
# Usado para usuarios con acceso indexado
usuarios = ArregloDinamico()
usuarios.agregar(usuario)
usuarios.obtener(indice)  # Acceso O(1)
```

**Ventajas:**
- Acceso aleatorio O(1)
- Redimensionamiento automático
- Búsquedas eficientes

### 3. **Pila (LIFO)** - Historial de Préstamos
```python
# Guarda los préstamos más recientes arriba
historial = Pila()
historial.apilar(prestamo_nuevo)
ultimo_prestamo = historial.ver_tope()
```

**Ventajas:**
- Acceso rápido a operaciones recientes
- Ideal para auditoría
- Implementación simple

### 4. **Cola (FIFO)** - Solicitudes Pendientes
```python
# Procesa solicitudes por orden de llegada
solicitudes = Cola()
solicitudes.encolar(nueva_solicitud)
siguiente = solicitudes.desencolar()
```

**Ventajas:**
- Procesamiento justo (primero en llegar, primero en ser atendido)
- Ideal para sistemas de reservas
- Mantiene orden temporal

---

## 💻 Funcionalidades Implementadas

### ✅ Gestión de Libros
- Registrar nuevos libros (ISBN, título, autor, categoría, año)
- Buscar libros por múltiples criterios
- Ver estado de disponibilidad
- Eliminar libros del sistema
- Listado completo con información detallada

### ✅ Gestión de Usuarios
- Registrar usuarios (nombre, email, teléfono)
- Búsqueda por nombre, email o ID
- Seguimiento de préstamos activos por usuario
- Historial completo de préstamos
- Validación de emails únicos

### ✅ Sistema de Préstamos
- Realizar préstamos con validaciones automáticas
- Devolver libros y actualizar disponibilidad
- Control de fechas de vencimiento (14 días por defecto)
- Cálculo automático de días restantes
- Manejo de préstamos vencidos

### ✅ Estadísticas en Tiempo Real
- Total de libros en el sistema
- Libros disponibles vs prestados
- Total de usuarios registrados
- Préstamos activos
- Solicitudes pendientes

### ✅ Sistema de Historial y Reportes
- Historial de préstamos recientes (usando Pila)
- Cola de solicitudes pendientes (usando Cola)
- Reportes detallados por usuario
- Seguimiento de actividad del sistema

---

## 🧪 Sistema de Pruebas

### Pruebas Incluidas
- **Estructuras de Datos**: Validación de todas las operaciones básicas
- **Modelos de Dominio**: Creación y propiedades de objetos
- **Integración**: Flujos completos del sistema
- **Estadísticas**: Coherencia de datos y cálculos

### Ejecutar Pruebas
```bash
# Pruebas completas con demostración
python main.py --tests

# Solo pruebas unitarias
python pruebas_sistema.py
```

**Ejemplo de salida exitosa:**
```
Pruebas ejecutadas: 11
Exitosas: 11
Fallidas: 0
Errores: 0

🎉 TODAS LAS PRUEBAS PASARON EXITOSAMENTE
```

---

## 📊 Datos de Ejemplo Incluidos

### Libros Precargados
1. "Cien años de soledad" - Gabriel García Márquez
2. "Don Quijote de la Mancha" - Miguel de Cervantes  
3. "1984" - George Orwell
4. "El principito" - Antoine de Saint-Exupéry
5. "Crónica de una muerte anunciada" - Gabriel García Márquez

### Usuarios Precargados
1. Juan Pérez (U001) - juan.perez@email.com
2. María García (U002) - maria.garcia@email.com
3. Carlos López (U003) - carlos.lopez@email.com

---

## 🎨 Capturas de Pantalla de la Interfaz

### Panel Principal
- **Izquierda**: Estadísticas en tiempo real
- **Derecha**: Pestañas funcionales

### Pestañas Disponibles
1. **Gestión de Libros**: Registro, búsqueda, eliminación
2. **Gestión de Usuarios**: Registro y consultas
3. **Gestión de Préstamos**: Realizar y devolver
4. **Historial y Reportes**: Visualización de actividad

---

## 🔧 Solución de Problemas Comunes

### Problema: "python no se reconoce como comando"
**Solución**: Verificar que Python está en el PATH del sistema
```bash
# Verificar instalación
where python
# o
python --version
```

### Problema: "No module named 'tkinter'"
**Solución**: 
- **Windows**: Reinstalar Python desde python.org
- **Linux**: `sudo apt-get install python3-tk`
- **macOS**: `brew install python-tk`

### Problema: "Permission denied"
**Solución**: Verificar permisos de ejecución
```bash
# Windows: Ejecutar como administrador si es necesario
# Linux/Mac: chmod +x main.py
```

### Problema: Archivos no encontrados
**Solución**: Verificar que todos los archivos estén en el mismo directorio
```bash
# Listar archivos en el directorio
dir  # Windows
ls   # Linux/Mac
```

---

## 📈 Rendimiento y Complejidad

### Complejidades Computacionales

| Operación | Lista Enlazada | Arreglo Dinámico | Pila | Cola |
|-----------|---------------|------------------|------|------|
| **Inserción** | O(1) al inicio | O(1) amortizado | O(1) | O(1) |
| **Búsqueda** | O(n) | O(n) | O(n) | O(n) |
| **Eliminación** | O(n) | O(n) | O(1) | O(1) |
| **Acceso** | O(n) | O(1) | O(1) tope | O(1) frente |

### Uso de Memoria
- **Lista Enlazada**: O(n) + overhead de punteros
- **Arreglo Dinámico**: O(n) con capacidad de crecimiento
- **Pila/Cola**: O(n) proporcional al contenido

---

## 🚦 Estados del Sistema

### Estados de Libro
- **Disponible**: Listo para préstamo
- **Prestado**: Actualmente en préstamo

### Estados de Préstamo
- **Activo**: Préstamo vigente
- **Devuelto**: Libro ya devuelto
- **Vencido**: Préstamo que excedió la fecha límite

### Estados de Usuario
- **Activo**: Con o sin préstamos
- **Préstamos activos**: Contador automático

---

## 📚 Decisiones de Diseño

### ¿Por qué estas estructuras?

1. **Lista Enlazada para Libros**
   - Razón: Catálogo cambia frecuentemente
   - Inserción/eliminación eficiente
   - No necesita acceso aleatorio

2. **Arreglo Dinámico para Usuarios**
   - Razón: Acceso frecuente por índice
   - Usuarios cambian menos frecuentemente
   - Redimensionamiento automático

3. **Pila para Historial**
   - Razón: Importancia de eventos recientes
   - LIFO natural para auditoría
   - Acceso rápido al último elemento

4. **Cola para Solicitudes**
   - Razón: Procesamiento justo (FIFO)
   - Sistema de turnos
   - Manejo de lista de espera

---

## 🎓 Valor Académico

### Conceptos Demostrados
- **Implementación desde cero** de estructuras fundamentales
- **Aplicación práctica** en sistema real
- **Comparación de rendimiento** entre estructuras
- **Diseño orientado a objetos** con separación de responsabilidades
- **Pruebas unitarias** y validación de código
- **Interfaz de usuario** moderna y funcional

### Habilidades Desarrolladas
- Programación en Python
- Diseño de interfaces gráficas
- Testing y depuración
- Documentación técnica
- Análisis de complejidad computacional

---

## 📞 Soporte y Contacto

### Verificación Rápida del Sistema
```bash
# Diagnóstico completo
python -c "
import sys, os
print('🔍 DIAGNÓSTICO DEL SISTEMA')
print(f'Python: {sys.version}')
print(f'Directorio: {os.getcwd()}')

modules = ['tkinter', 'datetime', 'unittest']
for module in modules:
    try:
        __import__(module)
        print(f'✅ {module}: Disponible')
    except ImportError:
        print(f'❌ {module}: No disponible')

files = ['estructuras_datos.py', 'modelos.py', 'interfaz_grafica.py', 'pruebas_sistema.py', 'main.py']
print('\\n📁 ARCHIVOS DEL PROYECTO:')
for file in files:
    status = '✅' if os.path.exists(file) else '❌ FALTA'
    print(f'{status} {file}')
"
```

### Comandos de Inicio Rápido
```bash
# 1. Verificar instalación
python main.py --tests

# 2. Ejecutar interfaz gráfica
python main.py --gui

# 3. Usar modo consola
python main.py --console
```

---

## ✅ Checklist de Instalación

### Antes de Empezar
- [ ] Python 3.7+ instalado y funcionando
- [ ] Tkinter disponible para interfaz gráfica
- [ ] Todos los archivos .py descargados
- [ ] Archivos en el mismo directorio
- [ ] Terminal abierta en el directorio correcto

### Verificación de Funcionamiento  
- [ ] `python main.py --tests` pasa todas las pruebas
- [ ] `python main.py --gui` abre la interfaz gráfica
- [ ] `python main.py --console` muestra el menú interactivo
- [ ] Las estadísticas muestran datos precargados

### ¡Todo Listo! 🎉
Si todos los elementos están marcados, el sistema está listo para usar.

**Comando recomendado para comenzar:**
```bash
python main.py
```

---

## 📝 Ejemplo de Uso Completo

### 1. Verificar el Sistema
```bash
# Ejecutar diagnóstico
python -c "
import sys, os
print('Sistema:', sys.platform)
print('Python:', sys.version[:5])
files = ['estructuras_datos.py', 'modelos.py', 'interfaz_grafica.py', 'main.py']
missing = [f for f in files if not os.path.exists(f)]
print('Archivos faltantes:' if missing else 'Todos los archivos presentes:', missing or 'Ninguno')
"
```

### 2. Ejecutar Pruebas
```bash
python main.py --tests
```

### 3. Usar el Sistema
```bash
# Interfaz gráfica
python main.py

# O modo consola
python main.py --console
```

### 4. Explorar Funcionalidades
En la interfaz gráfica puedes:
- Ver estadísticas en tiempo real
- Registrar nuevos libros y usuarios
- Realizar y devolver préstamos
- Buscar por diferentes criterios
- Ver el historial de actividades

---

## 🚀 Demo Rápida (Modo Consola)

```bash
python main.py --console
```

1. Seleccionar opción `1` para ver estadísticas
2. Seleccionar opción `2` para ver libros precargados
3. Seleccionar opción `3` para ver usuarios de ejemplo
4. Seleccionar opción `5` para realizar un préstamo:
   - ISBN: `978-84-376-0494-7`
   - Usuario: `U001`
5. Ver las estadísticas actualizadas con opción `1`

---

## 📊 Resultados Esperados

### Al Ejecutar las Pruebas
```
============================================================
RESUMEN DE PRUEBAS
============================================================
Pruebas ejecutadas: 11
Exitosas: 11
Fallidas: 0
Errores: 0

🎉 TODAS LAS PRUEBAS PASARON EXITOSAMENTE
```

### Al Ver Estadísticas Iniciales
```
========================================
ESTADÍSTICAS DEL SISTEMA
========================================
Total De Libros................. 5
Libros Disponibles.............. 5
Libros Prestados................ 0
Total De Usuarios............... 3
Prestamos Activos............... 0
Solicitudes Pendientes.......... 0
```

---

**🏆 ¡Disfruta explorando las estructuras de datos lineales con este sistema completo de gestión de biblioteca!**

---

*Proyecto desarrollado para el curso de Estructuras de Datos - Unidad 1*  
*Implementación académica con fines educativos - 2024*