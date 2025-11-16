#!/usr/bin/env python3
"""
x2y CLI
Convierte archivos de audio y video entre diferentes formatos usando FFmpeg.
"""

import argparse
import os
import subprocess
import sys
from pathlib import Path


def check_ffmpeg():
    """Verifica si FFmpeg está instalado en el sistema."""
    try:
        result = subprocess.run(['ffmpeg', '-version'],
                              capture_output=True, text=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def get_supported_audio_formats():
    """Retorna los formatos de audio soportados."""
    return ['mp3', 'wav', 'flac', 'aac', 'm4a', 'ogg', 'wma']


def get_supported_video_formats():
    """Retorna los formatos de video soportados."""
    return ['mp4', 'mkv', 'avi', 'mov', 'webm', 'flv', 'wmv', 'm4v']


def get_all_supported_formats():
    """Retorna todos los formatos soportados (audio + video)."""
    return get_supported_audio_formats() + get_supported_video_formats()


def is_video_format(file_path):
    """Determina si un archivo es de video basándose en su extensión."""
    video_extensions = get_supported_video_formats() + ['3gp', 'asf', 'divx', 'f4v', 'm2v', 'mpg', 'mpeg', 'ogv', 'rmvb']
    extension = Path(file_path).suffix.lower().lstrip('.')
    return extension in video_extensions


def detect_media_type(file_path):
    """Detecta si un archivo es de audio o video usando FFprobe."""
    try:
        cmd = ['ffprobe', '-v', 'quiet', '-print_format', 'json', '-show_streams', file_path]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)

        import json
        data = json.loads(result.stdout)

        has_video = any(stream.get('codec_type') == 'video' for stream in data.get('streams', []))
        has_audio = any(stream.get('codec_type') == 'audio' for stream in data.get('streams', []))

        if has_video:
            return 'video'
        elif has_audio:
            return 'audio'
        else:
            return 'unknown'
    except (subprocess.CalledProcessError, json.JSONDecodeError, FileNotFoundError):
        # Fallback a detección por extensión
        if is_video_format(file_path):
            return 'video'
        else:
            return 'audio'


def convert_media(input_file, output_file, output_format, quality='192k'):
    """
    Convierte un archivo de audio o video al formato especificado.

    Args:
        input_file (str): Ruta del archivo de entrada
        output_file (str): Ruta del archivo de salida
        output_format (str): Formato de salida
        quality (str): Calidad del audio/video
    """
    if not os.path.exists(input_file):
        print(f"❌ Error: El archivo '{input_file}' no existe.")
        return False

    # Detectar tipo de media
    media_type = detect_media_type(input_file)

    # Determinar si el formato de salida es de video o audio
    output_is_video = output_format.lower() in get_supported_video_formats()

    print(f"🔍 Detectado: {media_type}")
    print(f"🎯 Convirtiendo a: {'video' if output_is_video else 'audio'}")

    # Construir el comando FFmpeg
    cmd = ['ffmpeg', '-i', input_file]

    if output_is_video:
        # Configuración para video
        if output_format.lower() == 'mp4':
            cmd.extend(['-codec:v', 'libx264', '-codec:a', 'aac'])
            if quality != '192k':  # Para video, quality puede ser resolución
                if quality.endswith('p'):
                    height = quality.rstrip('p')
                    cmd.extend(['-vf', f'scale=-2:{height}'])
        elif output_format.lower() == 'mkv':
            cmd.extend(['-codec:v', 'libx264', '-codec:a', 'aac'])
            if quality != '192k' and quality.endswith('p'):
                height = quality.rstrip('p')
                cmd.extend(['-vf', f'scale=-2:{height}'])
        elif output_format.lower() == 'avi':
            cmd.extend(['-codec:v', 'libxvid', '-codec:a', 'libmp3lame'])
        elif output_format.lower() == 'mov':
            cmd.extend(['-codec:v', 'libx264', '-codec:a', 'aac'])
        elif output_format.lower() == 'webm':
            cmd.extend(['-codec:v', 'libvpx-vp9', '-codec:a', 'libopus'])
        elif output_format.lower() == 'flv':
            cmd.extend(['-codec:v', 'libx264', '-codec:a', 'aac'])
        elif output_format.lower() == 'wmv':
            cmd.extend(['-codec:v', 'wmv2', '-codec:a', 'wmav2'])
        elif output_format.lower() == 'm4v':
            cmd.extend(['-codec:v', 'libx264', '-codec:a', 'aac'])

        # Agregar bitrate de audio para video
        cmd.extend(['-b:a', '128k'])

    else:
        # Configuración para audio (código original)
        if output_format.lower() == 'mp3':
            cmd.extend(['-codec:a', 'libmp3lame', '-b:a', quality])
        elif output_format.lower() == 'wav':
            cmd.extend(['-codec:a', 'pcm_s16le'])
        elif output_format.lower() == 'flac':
            cmd.extend(['-codec:a', 'flac'])
        elif output_format.lower() == 'aac':
            cmd.extend(['-codec:a', 'aac', '-b:a', quality])
        elif output_format.lower() == 'm4a':
            cmd.extend(['-codec:a', 'aac', '-b:a', quality])
        elif output_format.lower() == 'ogg':
            cmd.extend(['-codec:a', 'libvorbis', '-b:a', quality])
        elif output_format.lower() == 'wma':
            cmd.extend(['-codec:a', 'wmav2', '-b:a', quality])

    # Sobrescribir archivo si existe
    cmd.extend(['-y', output_file])

    try:
        print(f"🔄 Convirtiendo '{input_file}' a '{output_file}'...")
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        print(f"✅ Conversión completada exitosamente!")
        print(f"📁 Archivo guardado en: {output_file}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error durante la conversión:")
        print(f"   {e.stderr}")
        return False


def main():
    parser = argparse.ArgumentParser(
        description="🎵🎬 x2y - Convierte archivos de audio y video usando FFmpeg",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos de uso:
  # Audio
  python run.py -i audio.wav -o audio.mp3
  python run.py -i song.flac -o song.mp3 -q 320k
  python run.py -i music.m4a -f wav

  # Video
  python run.py -i video.avi -f mp4
  python run.py -i movie.mkv -o movie.mp4 -q 720p
  python run.py -i clip.mov -f webm
        """
    )

    parser.add_argument('-i', '--input',
                       help='Archivo de audio o video de entrada')

    parser.add_argument('-o', '--output',
                       help='Archivo de salida (opcional)')

    parser.add_argument('-f', '--format',
                       choices=get_all_supported_formats(),
                       default='mp3',
                       help='Formato de salida (default: mp3)')

    parser.add_argument('-q', '--quality',
                       default='192k',
                       help='Calidad - bitrate para audio (192k) o resolución para video (720p)')

    parser.add_argument('--list-formats', action='store_true',
                       help='Mostrar formatos soportados')

    args = parser.parse_args()

    # Mostrar formatos soportados
    if args.list_formats:
        print("🎵 Formatos de audio soportados:")
        for fmt in get_supported_audio_formats():
            print(f"   • {fmt.upper()}")
        print("\n🎥 Formatos de video soportados:")
        for fmt in get_supported_video_formats():
            print(f"   • {fmt.upper()}")
        return

    # Verificar que se especifique archivo de entrada
    if not args.input:
        parser.error("Se requiere especificar un archivo de entrada (-i/--input)")
        return

    # Verificar que FFmpeg esté instalado
    if not check_ffmpeg():
        print("❌ Error: FFmpeg no está instalado o no está en el PATH.")
        print("💡 Instala FFmpeg con:")
        print("   Ubuntu/Debian: sudo apt install ffmpeg")
        print("   Fedora: sudo dnf install ffmpeg")
        print("   Arch: sudo pacman -S ffmpeg")
        print("   macOS: brew install ffmpeg")
        sys.exit(1)

    input_file = args.input
    output_format = args.format.lower()

    # Generar nombre de archivo de salida si no se especifica
    if args.output:
        output_file = args.output
    else:
        input_path = Path(input_file)
        output_file = str(input_path.with_suffix(f'.{output_format}'))

    # Realizar la conversión
    success = convert_media(input_file, output_file, output_format, args.quality)

    if success:
        # Mostrar información del archivo resultante
        if os.path.exists(output_file):
            size = os.path.getsize(output_file)
            size_mb = size / (1024 * 1024)
            print(f"📊 Tamaño del archivo: {size_mb:.2f} MB")
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
