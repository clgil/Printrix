# TallerPrint - Sistema de Gestión de Talleres de Impresoras

Sistema profesional para la gestión integral de talleres de reparación de impresoras, con arquitectura limpia, interfaz moderna Mobile First y preparado para convertirse posteriormente en una aplicación Android.

## Características

- **100% Offline**: No requiere conexión a Internet
- **Mobile First**: Diseñado primero para móviles, luego tablets y escritorio
- **Arquitectura Modular**: Blueprints independientes por módulo
- **Bootstrap 5.3 Local**: Sin dependencias CDN
- **SQLite**: Base de datos ligera y portable
- **Preparado para Android**: Compatible con Capacitor/WebView

## Tecnologías

- Python 3.12+
- Flask 3.0
- SQLAlchemy
- SQLite
- Bootstrap 5.3
- Bootstrap Icons
- Jinja2
- JavaScript Vanilla

## Instalación

```bash
# Instalar dependencias
pip install -r requirements.txt

# Ejecutar aplicación
python run.py
```

## Acceso

- URL: http://localhost:5000
- Usuario: admin
- Contraseña: admin123

## Estructura del Proyecto

```
/workspace
├── app/                      # Paquete principal
│   ├── auth/                 # Autenticación
│   ├── dashboard/            # Panel principal
│   ├── clientes/             # Gestión de clientes
│   ├── equipos/              # Gestión de equipos
│   ├── ordenes/              # Órdenes de trabajo
│   ├── tecnicos/             # Gestión de técnicos
│   ├── inventario/           # Control de inventario
│   ├── proveedores/          # Gestión de proveedores
│   ├── usuarios/             # Administración de usuarios
│   ├── reportes/             # Reportes e informes
│   ├── configuracion/        # Configuración del sistema
│   ├── backup/               # Copias de seguridad
│   ├── helpers/              # Utilidades
│   ├── models/               # Modelos de datos
│   └── services/             # Servicios
├── static/                   # Archivos estáticos
│   ├── css/                  # Hojas de estilo
│   ├── js/                   # JavaScript
│   ├── images/               # Imágenes
│   └── fonts/                # Fuentes
├── templates/                # Plantillas Jinja2
├── instance/                 # Base de datos SQLite
├── run.py                    # Punto de entrada
└── requirements.txt          # Dependencias
```

## Módulos Implementados

### Autenticación
- Login/Logout
- Recuperación de contraseña
- Cambio de contraseña
- Roles y permisos

### Dashboard
- Estadísticas en tiempo real
- Acciones rápidas
- Últimas órdenes
- Stock crítico

### Clientes
- CRUD completo
- Historial de equipos
- Búsqueda avanzada
- Observaciones

### Equipos
- Registro de impresoras
- Marcas y modelos
- Número de serie
- Accesorios
- Estado físico
- Fotos (pendiente)

### Órdenes de Trabajo
- Recepción
- Diagnóstico
- Presupuesto
- Reparación
- Entrega
- Historial completo
- Estados personalizables

### Técnicos
- CRUD completo
- Especialidad
- Estado (disponible/ocupado)
- Asignaciones

### Inventario
- Productos
- Categorías
- Entradas/Salidas
- Stock mínimo
- Movimientos

### Proveedores
- CRUD completo
- Historial de compras
- Datos de contacto

### Usuarios
- CRUD completo
- Roles (Administrador, Recepcionista, Técnico, Consulta)
- Permisos
- Actividad

### Reportes
- Ingresos
- Equipos reparados
- Clientes
- Inventario
- Técnicos
- Ganancias
- Exportación PDF (pendiente)

### Configuración
- Datos de empresa
- Moneda
- Parámetros del sistema

### Backup
- Crear respaldo
- Restaurar
- Exportar/Importar

## Diseño UI/UX

### Componentes
- Cards modernas
- Badges de estado
- Offcanvas para menús
- Bottom Navigation (mobile)
- Sidebar (desktop)
- Botones grandes táctiles
- Iconografía consistente

### Responsive
- Móvil: Bottom Navigation + Offcanvas
- Tablet: Sidebar colapsable
- Escritorio: Sidebar fijo

### Colores Profesionales
- Primary: #2563eb (Azul)
- Success: #22c55e (Verde)
- Warning: #f59e0b (Ámbar)
- Danger: #ef4444 (Rojo)
- Info: #0ea5e9 (Celeste)

## Seguridad

- Hash de contraseñas (Werkzeug)
- Protección CSRF (Flask-WTF)
- Validaciones en servidor
- Control de permisos por roles
- Registro de actividad de usuarios

## Base de Datos

Modelos normalizados con relaciones mediante claves foráneas:
- Usuarios
- Clientes
- Equipos
- Órdenes
- Técnicos
- Productos
- Categorías
- Movimientos
- Proveedores
- Compras
- Configuración

## Preparado para Android

La interfaz está diseñada para empaquetarse fácilmente con:
- **Capacitor**: Para convertir la web app en nativa
- **WebView**: Para incrustar en una app Android

No se requieren modificaciones de la experiencia de usuario.

## Próximas Mejoras

- [ ] Descarga de Bootstrap localmente
- [ ] Descarga de Bootstrap Icons localmente
- [ ] Completar todos los formularios CRUD
- [ ] Implementar subida de fotos
- [ ] Generación de PDF para reportes
- [ ] Dark Mode completo
- [ ] Notificaciones push
- [ ] Código de barras/QR
- [ ] Firmas digitales
- [ ] WhatsApp integration

## Licencia

MIT License

## Autor

Desarrollado como sistema profesional para talleres de impresión.
