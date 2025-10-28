# Invitación de Boda - Aplicación Web

Aplicación web elegante para invitaciones de boda con registro de asistencia.

## Tecnologías Utilizadas
- **Flask**: Framework web de Python
- **SQLite**: Base de datos para almacenar invitados
- **Jinja2**: Motor de plantillas (incluido con Flask)

## Instalación

1. Instala las dependencias:
```bash
pip install -r requirements.txt
```

## Uso

1. Ejecuta la aplicación:
```bash
python app.py
```

2. Abre tu navegador en: `http://127.0.0.1:5000`

3. Para ver la lista de invitados registrados, accede a: `http://127.0.0.1:5000/lista-invitados`

## Estructura del Proyecto

```
├── app.py                 # Aplicación principal de Flask
├── invitados.db          # Base de datos SQLite (se crea automáticamente)
├── requirements.txt      # Dependencias del proyecto
├── templates/
│   ├── base.html        # Plantilla base
│   ├── index.html       # Página principal de invitación
│   └── lista.html       # Página de lista de invitados
└── README.md            # Este archivo
```

## Características

- ✨ Diseño elegante y responsivo
- 💝 Formulario de confirmación de asistencia
- 📋 Panel administrativo para ver la lista de invitados
- 🎨 Animaciones suaves y efectos visuales
- 📱 Compatible con dispositivos móviles

## Personalización

Puedes editar los siguientes aspectos en `templates/index.html`:
- Fecha, hora y lugar de la boda
- Colores y estilos (en la sección `{% block styles %}`)
- Textos y mensajes

## Seguridad

**Importante**: Antes de desplegar en producción, cambia la `secret_key` en `app.py` por una clave segura y única.
