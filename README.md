# 🎵🎬 Free Media Converter

**Free Media Converter** es una herramienta de línea de comandos ligera y fácil de usar que convierte archivos de **audio y video** con la potencia de FFmpeg, pero sin tener que instalar nada más en tu equipo: todo el entorno se levanta dentro de Docker.

Diseñado para creadores de contenido, podcasters y desarrolladores que necesitan una solución rápida, el CLI ofrece:

* 🎧 Conversión entre formatos de audio populares
* 🎥 Soporte para formatos de video comunes
* ⚙️ Control de calidad con bitrate (audio) y resolución (video)
* 🔄 Detección automática del tipo de media
* 🐳 Dockerizado: Python + FFmpeg en contenedores listos para usar

## 📋 Requisitos

- Docker 24 o superior (el plugin de Compose entra como parte de Docker Desktop o Docker Engine moderno).
- Permisos para ejecutar `docker` y `docker compose` desde tu terminal.
- El repositorio con `run.sh`, `docker/Dockerfile` y `docker/docker-compose.yml` intactos.

## 🐳 Entorno Docker

El proyecto incluye `docker/Dockerfile` que instala Python 3.11 y FFmpeg, y expone `ENTRYPOINT ["python", "run.py"]` para que cada contenedor arranque con la herramienta. El archivo `docker/docker-compose.yml` construye esa imagen, monta la raíz del repositorio en `/app` y mantiene el servicio listo para uso interactivo.

## 🚀 Uso

### Ejecutar el CLI dentro del contenedor

Desde la raíz del proyecto ejecuta `./run.sh` seguido de los flags de la herramienta. El script reconstruye la imagen cuando hace falta y hace `docker compose run --rm free-media-converter` pasando exactamente los argumentos que le diste:

```bash
./run.sh -i audio.wav -o audio.mp3
./run.sh -i song.flac -o song.mp3 -q 320k
./run.sh -i video.mkv -f mp4 -q 720p
```

Si quieres ver los formatos soportados usa `./run.sh --list-formats` y el CLI los listará por pantalla.

### Opciones de CLI

```
-i, --input       Archivo de audio o video de entrada (requerido)
-o, --output      Archivo de salida (opcional)
-f, --format      Formato de salida (default: mp3)
-q, --quality     Calidad - bitrate para audio (192k) o resolución para video (720p)
--list-formats    Mostrar formatos soportados
-h, --help        Mostrar ayuda
```

### Formatos soportados

- **Audio**: MP3, WAV, FLAC, AAC, M4A, OGG, WMA
- **Video**: MP4, MKV, AVI, MOV, WebM, FLV, WMV, M4V

### Verificación automática

El script se encarga de verificar:

- ✅ FFmpeg disponible dentro del contenedor (ya viene instalado).
- ✅ Que el archivo de entrada exista en la ruta desde donde ejecutas `./run.sh`.
- ✅ Que la conversión termine sin errores (se imprime el stderr de FFmpeg en caso de fallo).
- 📊 Tamaño final del archivo convertido cuando todo sale bien.

### Solución de problemas rápida

- **FFmpeg no encontrado**: ejecuta `./run.sh`; evita lanzar `python run.py` fuera de Docker.
- **Archivo no encontrado**: pasa rutas relativas al directorio actual donde se lanza `./run.sh`.
- **Error de conversión**: revisa el mensaje que FFmpeg imprime para entender el problema.

## 🎯 Características

- 🎧 Conversión completa entre formatos de audio y video populares.
- 🎯 Control de calidad por bitrate/resolución.
- 🔍 Detección inteligente de audio vs. video.
- 🐳 Todo encapsulado en Docker: no necesitas FFmpeg ni Python en tu host.
