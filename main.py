"""
Sistema de Gestión de Biblioteca - Archivo Principal
===================================================

Este es el archivo principal para ejecutar el Sistema de Gestión de Biblioteca
que implementa estructuras de datos lineales (Lista, Pila, Cola, Arreglo).

Uso:
    python main.py [opción]

Opciones:
    --gui     : Ejecutar con interfaz gráfica (por defecto)
    --tests   : Ejecutar pruebas del sistema
    --console : Ejecutar en modo consola
    --help    : Mostrar esta ayuda

Autor: [Tu nombre]
Fecha: 2024
Curso: Estructuras de Datos - Unidad 1
"""

import sys
import argparse
from datetime import datetime

def mostrar_banner():
    """Muestra el banner de bienvenida del sistema."""
    print("="*70)
    print("     SISTEMA DE GESTIÓN DE BIBLIOTECA")
    print("     Implementación de Estructuras de Datos Lineales")
    print("="*70)
    print("Curso: Estructuras de Datos - Unidad 1")
    print(f"Fecha de ejecución: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print("="*70)

def ejecutar_interfaz_grafica():
    """Ejecuta el sistema con interfaz gráfica."""
    try:
        from interfaz_grafica import main as gui_main
        print("Iniciando interfaz gráfica...")
        print("Nota: Cierre la ventana para terminar la aplicación.")
        gui_main()
    except ImportError as e:
        print(f"Error al importar la interfaz gráfica: {e}")
        print("Asegúrese de que tkinter esté instalado correctamente.")
        return False
    except Exception as e:
        print(f"Error inesperado en la interfaz gráfica: {e}")
        return False
    return True

def ejecutar_pruebas():
    """Ejecuta las pruebas del sistema."""
    try:
        from pruebas_sistema import ejecutar_pruebas_completas
        print("Ejecutando pruebas del sistema...")
        exito = ejecutar_pruebas_completas()
        return exito
    except ImportError as e:
        print(f"Error al importar el módulo de pruebas: {e}")
        return False
    except Exception as e:
        print(f"Error inesperado durante las pruebas: {e}")
        return False

def ejecutar_modo_consola():
    """Ejecuta el sistema en modo consola interactivo."""
    try:
        from modelos import BibliotecaManager
        
        print("Iniciando modo consola...")
        biblioteca = BibliotecaManager()
        
        while True:
            print("\n" + "-"*50)
            print("MENÚ PRINCIPAL")
            print("-"*50)
            print("1. Mostrar estadísticas")
            print("2. Listar todos los libros")
            print("3. Listar todos los usuarios")
            print("4. Buscar libro")
            print("5. Realizar préstamo")
            print("6. Devolver libro")
            print("7. Mostrar préstamos activos")
            print("0. Salir")
            
            try:
                opcion = input("\nSeleccione una opción: ").strip()
                
                if opcion == "0":
                    print("¡Gracias por usar el Sistema de Gestión de Biblioteca!")
                    break
                
                elif opcion == "1":
                    mostrar_estadisticas(biblioteca)
                
                elif opcion == "2":
                    listar_libros(biblioteca)
                
                elif opcion == "3":
                    listar_usuarios(biblioteca)
                
                elif opcion == "4":
                    buscar_libro_consola(biblioteca)
                
                elif opcion == "5":
                    realizar_prestamo_consola(biblioteca)
                
                elif opcion == "6":
                    devolver_libro_consola(biblioteca)
                
                elif opcion == "7":
                    mostrar_prestamos_activos(biblioteca)
                
                else:
                    print("Opción inválida. Por favor, intente nuevamente.")
                    
            except KeyboardInterrupt:
                print("\n\nSaliendo del sistema...")
                break
            except Exception as e:
                print(f"Error: {e}")
                
    except ImportError as e:
        print(f"Error al importar módulos necesarios: {e}")
        return False
    except Exception as e:
        print(f"Error inesperado en modo consola: {e}")
        return False
    
    return True

def mostrar_estadisticas(biblioteca):
    """Muestra las estadísticas del sistema."""
    print("\n" + "="*40)
    print("ESTADÍSTICAS DEL SISTEMA")
    print("="*40)
    
    stats = biblioteca.obtener_estadisticas()
    for clave, valor in stats.items():
        nombre = clave.replace('_', ' ').title()
        print(f"{nombre:.<30} {valor}")

def listar_libros(biblioteca):
    """Lista todos los libros."""
    print("\n" + "="*60)
    print("LISTA DE LIBROS")
    print("="*60)
    
    libros = biblioteca.obtener_todos_los_libros()
    if not libros:
        print("No hay libros registrados.")
        return
    
    for i, libro in enumerate(libros, 1):
        estado = "Disponible" if libro.disponible else "Prestado"
        print(f"{i:2d}. {libro.titulo}")
        print(f"    Autor: {libro.autor}")
        print(f"    ISBN: {libro.isbn}")
        print(f"    Estado: {estado}")
        print()

def listar_usuarios(biblioteca):
    """Lista todos los usuarios."""
    print("\n" + "="*60)
    print("LISTA DE USUARIOS")
    print("="*60)
    
    usuarios = biblioteca.obtener_todos_los_usuarios()
    if not usuarios:
        print("No hay usuarios registrados.")
        return
    
    for i, usuario in enumerate(usuarios, 1):
        print(f"{i:2d}. {usuario.nombre} ({usuario.id_usuario})")
        print(f"    Email: {usuario.email}")
        print(f"    Préstamos activos: {usuario.prestamos_activos}")
        print()

def buscar_libro_consola(biblioteca):
    """Permite buscar libros por diferentes criterios."""
    print("\n" + "="*40)
    print("BÚSQUEDA DE LIBROS")
    print("="*40)
    
    print("Criterios de búsqueda:")
    print("1. Por título")
    print("2. Por autor")
    print("3. Por categoría")
    print("4. Por ISBN")
    
    try:
        criterio_num = input("Seleccione criterio (1-4): ").strip()
        criterios = {"1": "titulo", "2": "autor", "3": "categoria", "4": "isbn"}
        
        if criterio_num not in criterios:
            print("Criterio inválido.")
            return
        
        criterio = criterios[criterio_num]
        valor = input(f"Ingrese valor de búsqueda para {criterio}: ").strip()
        
        if not valor:
            print("Debe ingresar un valor de búsqueda.")
            return
        
        libros = biblioteca.buscar_libros(criterio, valor)
        
        if not libros:
            print(f"No se encontraron libros con {criterio} que contenga '{valor}'.")
            return
        
        print(f"\nSe encontraron {len(libros)} libro(s):")
        print("-" * 50)
        
        for i, libro in enumerate(libros, 1):
            estado = "Disponible" if libro.disponible else "Prestado"
            print(f"{i}. {libro.titulo} - {libro.autor}")
            print(f"   ISBN: {libro.isbn} | Estado: {estado}")
            
    except Exception as e:
        print(f"Error durante la búsqueda: {e}")

def realizar_prestamo_consola(biblioteca):
    """Permite realizar un préstamo."""
    print("\n" + "="*40)
    print("REALIZAR PRÉSTAMO")
    print("="*40)
    
    try:
        isbn = input("ISBN del libro: ").strip()
        id_usuario = input("ID del usuario: ").strip()
        
        if not isbn or not id_usuario:
            print("Debe proporcionar ISBN y ID de usuario.")
            return
        
        # Verificar que el libro existe y está disponible
        libro = biblioteca.obtener_libro_por_isbn(isbn)
        if not libro:
            print("El libro no existe en el sistema.")
            return
        
        if not libro.disponible:
            print("El libro no está disponible para préstamo.")
            return
        
        # Verificar que el usuario existe
        usuario = biblioteca.obtener_usuario_por_id(id_usuario)
        if not usuario:
            print("El usuario no existe en el sistema.")
            return
        
        # Realizar préstamo
        loan_id = biblioteca.realizar_prestamo(isbn, id_usuario)
        if loan_id:
            print(f"✓ Préstamo realizado exitosamente.")
            print(f"  ID del préstamo: {loan_id}")
            print(f"  Libro: {libro.titulo}")
            print(f"  Usuario: {usuario.nombre}")
        else:
            print("No se pudo realizar el préstamo.")
            
    except Exception as e:
        print(f"Error al realizar préstamo: {e}")

def devolver_libro_consola(biblioteca):
    """Permite devolver un libro."""
    print("\n" + "="*40)
    print("DEVOLVER LIBRO")
    print("="*40)
    
    try:
        loan_id = input("ID del préstamo: ").strip()
        
        if not loan_id:
            print("Debe proporcionar el ID del préstamo.")
            return
        
        if biblioteca.devolver_libro(loan_id):
            print(f"✓ Libro devuelto exitosamente (Préstamo: {loan_id})")
        else:
            print("No se encontró el préstamo especificado.")
            
    except Exception as e:
        print(f"Error al devolver libro: {e}")

def mostrar_prestamos_activos(biblioteca):
    """Muestra todos los préstamos activos."""
    print("\n" + "="*60)
    print("PRÉSTAMOS ACTIVOS")
    print("="*60)
    
    prestamos = biblioteca.obtener_prestamos_activos()
    if not prestamos:
        print("No hay préstamos activos.")
        return
    
    for i, prestamo in enumerate(prestamos, 1):
        libro = biblioteca.obtener_libro_por_isbn(prestamo.isbn_libro)
        usuario = biblioteca.obtener_usuario_por_id(prestamo.id_usuario)
        
        print(f"{i:2d}. Préstamo {prestamo.id_prestamo}")
        print(f"    Libro: {libro.titulo if libro else 'Desconocido'}")
        print(f"    Usuario: {usuario.nombre if usuario else 'Desconocido'}")
        print(f"    Fecha préstamo: {prestamo.fecha_prestamo.strftime('%d/%m/%Y %H:%M')}")
        print(f"    Vencimiento: {prestamo.fecha_vencimiento.strftime('%d/%m/%Y')}")
        print(f"    Días restantes: {prestamo.dias_restantes()}")
        print()

def mostrar_ayuda():
    """Muestra la ayuda del programa."""
    print(__doc__)

def main():
    """Función principal del programa."""
    parser = argparse.ArgumentParser(
        description="Sistema de Gestión de Biblioteca con Estructuras de Datos Lineales",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos de uso:
    python main.py                    # Ejecutar con interfaz gráfica
    python main.py --gui              # Ejecutar con interfaz gráfica
    python main.py --tests            # Ejecutar pruebas del sistema
    python main.py --console          # Ejecutar en modo consola
        """
    )
    
    parser.add_argument('--gui', action='store_true', 
                       help='Ejecutar con interfaz gráfica (por defecto)')
    parser.add_argument('--tests', action='store_true', 
                       help='Ejecutar pruebas del sistema')
    parser.add_argument('--console', action='store_true', 
                       help='Ejecutar en modo consola')
    
    args = parser.parse_args()
    
    mostrar_banner()
    
    # Si no se especifica ninguna opción, usar GUI por defecto
    if not any([args.gui, args.tests, args.console]):
        args.gui = True
    
    exito = True
    
    if args.tests:
        exito = ejecutar_pruebas()
        
    elif args.console:
        exito = ejecutar_modo_consola()
        
    elif args.gui:
        exito = ejecutar_interfaz_grafica()
    
    if not exito:
        sys.exit(1)
    
    print("\nPrograma terminado.")

if __name__ == "__main__":
    main()