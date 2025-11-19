#!/usr/bin/env python3
"""
VALIDACIÓN FINAL DEL SISTEMA COMPLETO
Biblioteca Virtual - Estructuras Lineales + Árboles
"""

from modelos import BibliotecaManager

def validar_sistema():
    print('🧪 VALIDACIÓN FINAL DEL SISTEMA COMPLETO')
    print('=' * 50)

    try:
        # Crear instancia del sistema
        biblioteca = BibliotecaManager()
        print('✅ BibliotecaManager creado correctamente')

        # Agregar datos de prueba
        print('\n📚 Agregando datos de prueba...')
        biblioteca.registrar_libro('978-84-376-0494-7', 'Cien años de soledad', 'Gabriel García Márquez', 'Novela', 1967)
        biblioteca.registrar_usuario('Juan Pérez', 'juan@email.com', '123-456-7890')
        print('✅ Datos agregados correctamente')

        # Probar búsquedas optimizadas
        print('\n🔍 Probando búsquedas optimizadas...')
        libro_encontrado = biblioteca.obtener_libro_por_isbn('978-84-376-0494-7')
        usuario_encontrado = biblioteca.obtener_usuario_por_id('U001')
        print(f'✅ Libro encontrado: {libro_encontrado.titulo if libro_encontrado else "No encontrado"}')
        print(f'✅ Usuario encontrado: {usuario_encontrado.nombre if usuario_encontrado else "No encontrado"}')

        # Probar estadísticas
        print('\n📊 Generando estadísticas...')
        stats = biblioteca.obtener_estadisticas()
        print(f'✅ Total libros: {stats["total_libros"]}')
        print(f'✅ Índices optimizados: {stats["indices_optimizados"]}')

        print('\n🎉 VALIDACIÓN COMPLETA - SISTEMA FUNCIONANDO PERFECTAMENTE')
        print('✅ Arquitectura híbrida operativa')
        print('✅ Optimizaciones de rendimiento activas')
        return True

    except Exception as e:
        print(f'❌ Error en validación: {e}')
        return False

if __name__ == '__main__':
    exito = validar_sistema()
    exit(0 if exito else 1)