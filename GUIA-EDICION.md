# Guía para editar «Scratch en el aula»

La web se construye sola a partir de la carpeta **`generador/`**. Tú cambias un texto o una imagen desde el navegador, guardas, y en 2-3 minutos GitHub vuelve a crear toda la web: páginas, archivos .sb3, plantillas y tarjetas PDF.

---

## 1. Puesta en marcha (solo la primera vez)

1. En GitHub, crea un repositorio público llamado **`scratch-en-el-aula`**.
2. Pulsa **Add file › Upload files** y arrastra **todo el contenido** de este ZIP (las carpetas `generador` y `.github`, y estos archivos .md). Pulsa **Commit changes**.
   - Si la carpeta `.github` no se sube al arrastrar (algunos sistemas la ocultan), créala a mano: **Add file › Create new file**, escribe como nombre `.github/workflows/publicar.yml` y pega dentro el contenido de ese archivo.
3. Ve a **Settings › Pages** y, en **Source**, elige **GitHub Actions**.
4. Ve a la pestaña **Actions**, pulsa **Construir y publicar la web** y luego **Run workflow**.
5. Cuando aparezca el ✓ verde, la web estará en: `https://pablomoraga.github.io/scratch-en-el-aula/`

## 2. Cambiar el texto de un reto

Cada apartado tiene su archivo:

| Archivo | Contiene |
|---|---|
| `generador/c_empezar.py` | Para empezar |
| `generador/c_conoce.py` | Conoce Scratch 3.0 (categorías y ejemplos) |
| `generador/c_comenzamos.py` | Los 20 retos de Comenzamos |
| `generador/c_errores.py` | Encuentra el error |
| `generador/c_experto.py` | Modo experto |
| `generador/c_talleres.py` | Talleres |
| `generador/c_saber.py` | Para saber más (recursos, glosario, evaluación, enlaces) |

Pasos:

1. Abre el archivo y pulsa el **lápiz** (Edit this file).
2. Busca el reto con **Ctrl+F** (por ejemplo, escribe `Robit camina`).
3. Cambia solo el texto que está **entre comillas**. Así es un reto por dentro:

```python
R('Robit camina', 1, '15 min', ['bucles', 'animación'],          # título, dificultad (1-3), tiempo, conceptos
  'Hacer que Robit cruce el escenario moviendo las piernas.',     # objetivo
  ['Al pulsar la bandera, coloca a Robit a la izquierda.',        # pasos (uno por línea)
   'Repite 30 veces: mover 10 pasos y siguiente disfraz.'],
  ['El bloque <i>repetir</i> está en Control.'],                  # pistas
  ...                                                             # la solución en bloques (mejor no tocar)
  ['Haz que al llegar diga «¡Llegué!».'])                         # ideas de «¿Y si…?»
```

4. Pulsa **Commit changes**. En la pestaña **Actions** verás la construcción en marcha; con el ✓ verde, el cambio ya está publicado.

### Reglas de oro para no romper nada

- Escribe **dentro** de las comillas `'...'` y no borres las comas que separan los textos.
- **No uses el apóstrofo `'`** dentro de un texto: usa `’` o las comillas españolas `« »`.
- Para añadir un paso o una pista, copia una línea entera (con su coma final) y cambia el texto.
- Puedes usar negrita `<b>texto</b>`, cursiva `<i>texto</i>` y enlaces `<a href="https://...">texto</a>`.
- Si algo sale mal, **la web publicada no se estropea**: la construcción se para (aparece una ✗ roja en Actions) y sigue visible la versión anterior. Abre la ✗, mira las últimas líneas (indican el archivo y la línea del error), corrígelo o pulsa **History** en el archivo para volver a la versión anterior.

## 3. Cambiar una imagen de Scratch (personajes y fondos)

Puedes sustituir cualquier disfraz o fondo por uno tuyo **sin tocar código**:

1. Prepara tu imagen en **SVG** o **PNG** (fondo transparente para personajes).
2. Ponle **exactamente el nombre** del disfraz que quieres cambiar, por ejemplo `pelota.png` o `cielo.svg`.
3. Súbela a la carpeta **`generador/personalizado/imagenes/`** (Add file › Upload files).

Al construir, la web usará tu imagen en todos los proyectos, plantillas y fichas.

**Personajes:** `robit1` `robit2` `robit3` (Robit), `pelota`, `balon`, `estrella`, `nave`, `nave2`, `roca`, `pez`, `manzana`, `cesta`, `pala`, `ladrillo`, `coche`, `punto` (lápiz), `boton`, `boton_rojo`, `meta`, `burbuja`, `tambor`, `tecla`, `tecla_on`, `sol`, `planeta`, `luna`, `moneda`, `fantasma`, `mascota_feliz`, `mascota_normal`, `mascota_triste`, `comida`, `juguete`, `cama`.

**Fondos (480 × 360):** `blanco`, `cuadricula`, `laberinto`, `cielo`, `espacio`, `mar`, `noche`, `teatro`, `campo`, `porteria`, `fin`.

Consejos:
- Mantén un **tamaño parecido** al original: algunos juegos dependen de él (la pala, la cesta, los ladrillos de 60 px de ancho).
- En el **laberinto**, las paredes deben seguir siendo del color `#2e3a87`, porque el reto detecta ese color.

## 4. Cambiar un sonido

Sube un archivo **WAV** con el nombre del sonido a **`generador/personalizado/sonidos/`**: `pop.wav`, `ding.wav`, `boing.wav`, `error.wav`, `victoria.wav` o `golpe.wav`.

## 5. Añadir tus propias fotos o documentos a una página

1. Sube el archivo a **`generador/estaticos/img/`** (por ejemplo, `foto-club.jpg`).
2. En el texto de la página, escribe:

```html
<img src="../img/foto-club.jpg" alt="Descripción de la foto" width="400">
```

Todo lo que pongas en `generador/estaticos/` se copia tal cual a la web (sirve también para PDF u otros documentos).

## 6. Cambios grandes

Para crear retos nuevos, nuevos apartados o cambiar la solución en bloques, lo más cómodo es pedírselo a Claude: genera los archivos de `generador/` actualizados y solo tienes que subirlos al repositorio.
