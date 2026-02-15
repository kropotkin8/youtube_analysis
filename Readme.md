Proyecto: Análisis de YouTube (Data Extraction & Storage)

Descripción breve
Esta iniciativa tiene por objetivo extraer, almacenar y analizar datos públicos de YouTube con fines de investigación: crear un repositorio histórico de métricas, metadatos y texto (comentarios, títulos, descripciones), que sirva como base para análisis de tendencias, experimentos ML y generación de contenido. El proyecto incluye un Dockerfile para levantar un contenedor PostgreSQL donde guardar los datos y ejemplos de pipelines que se pueden orquestar vía GitHub Actions. Tambien contendrá los modelos de sqlalchemy para las tablas que contendrán los datos obtenidos.

Finalidad de los datos (qué y por qué)

El objetivo es disponer de un dataset reproducible y versionado que permita investigar y responder preguntas del tipo:

¿Qué formatos, tags y títulos están asociados a mayor engagement?

¿Cómo evolucionan tendencias temáticas en el tiempo?

¿Qué fragmentos de vídeo son más propensos a volverse “shorts” virales?

Entrenar y validar modelos que predigan CTR, retención o crecimiento de un canal.

Para ello se pretende recolectar datos que cubran las siguientes dimensiones (detalladas a continuación):

Datos deseados (lista y justificación)
1) Metadatos de contenido (por vídeo / item)

videoId, title, description, publishedAt, duration, categoryId, tags, thumbnails, language.
Por qué: análisis SEO/temático, clasificación por tipo, filtros por duración/idioma.

2) Métricas de rendimiento

viewCount, likeCount, dislikeCount (si aplica), commentCount, favoriteCount.
Por qué: cuantificar impacto, base para series temporales.

3) Métricas temporales y de retención

averageViewDuration, watchTime, retención por segmento (si disponible para canal propio).
Por qué: modelado de retención y calidad de contenido.

4) Datos de interacción textual

Comentarios (commentId, author, text, publishedAt, likeCount), hilos y respuestas.
Por qué: análisis de sentimiento, topic modelling y detección de comunidad.

5) Datos de audiencia (cuando sea accesible)

Demografía, país, idioma, dispositivos (normalmente sólo disponibles para canales propios).
Por qué: segmentación y validación de hipótesis sobre público objetivo.

6) Históricos de crecimiento

Series temporales de subscriberCount, viewCount por fecha.
Por qué: análisis de crecimiento y detección de anomalías o viralidad.

7) Metadatos técnicos y enriquecidos

Timestamps de capítulos, subtítulos (SRT), embeddings generados localmente (texto, audio, visual).
Por qué: necesario para análisis multimodal y extracción automática de clips.

Qué datos suelen ser accesibles y cuáles no

Accesibles fácilmente (API pública + API key): metadatos públicos (title, description, tags), videos.list (estadísticas básicas), search.list, playlistItems.list, channels.list (estadísticas globales).

Accesibles con limitaciones / OAuth: métricas internas (retención detallada, demografía) y YouTube Analytics (solo para el propietario del canal con OAuth).

No accesibles sin acuerdos comerciales o permisos especiales: datos privados de usuarios, historiales completos de visualizaciones a nivel usuario, datos demográficos de terceros.

Estructura de almacenamiento propuesta (esquema de ejemplo)

Nota: no es un diseño final; es un esquema orientativo para comenzar.

Tablas principales (ejemplos)

videos

video_id (PK), title, description, published_at, duration, category_id, channel_id, raw_snippet (JSON), inserted_at

video_stats_timeseries

id, video_id (FK), snapshot_time (timestamp), view_count, like_count, comment_count, favorite_count

channels

channel_id (PK), title, description, subscriber_count, raw_snippet

comments

comment_id (PK), video_id (FK), author, text, published_at, like_count, parent_id (nullable)

trends_market

id, source (youtube/social), topic, score, captured_at, raw_payload

embeddings

id, object_type (video/segment/text), object_id, vector (opcional en Chroma), created_at

Docker: levantar PostgreSQL

El repositorio contiene un Dockerfile o (preferible) un docker-compose.yml para levantar PostgreSQL localmente.

Ejemplo rápido (docker-compose):

version: '3.8'
services:
  db:
    image: postgres:15
    environment:
      POSTGRES_USER: yt_user
      POSTGRES_PASSWORD: yt_password
      POSTGRES_DB: youtube_analysis
    ports:
      - "5432:5432"
    volumes:
      - db_data:/var/lib/postgresql/data
volumes:
  db_data:


Instrucciones:

docker compose up -d

Conectar con psql o un cliente (usar variables de env).

Ejecutar scripts de creación de tablas (migrations SQL incluidos en /migrations).

Periodicidad recomendada (scheduling / GitHub Actions)

Se propone orquestar las llamadas a los endpoints de la API mediante workflows en GitHub Actions (cron). IMPORTANTE: GitHub Actions usa tiempos en UTC.

A continuación una tabla con la periodicidad recomendada y por qué:

Pipeline / Endpoint	Frecuencia sugerida (cron)	Justificación
videos.list (trending / top N)	Cada 1 hora (0 * * * *)	Métricas dinámicas; detectar viralidad temprana.
search.list (keywords/monitor)	Cada 4 horas (0 */4 * * *)	Descubrimiento de nuevo contenido por keyword.
commentThreads.list (videos monitorizados)	Diario (0 2 * * *)	Comentarios no cambian tan rápido; reduce cuota.
playlistItems.list (uploads de canal)	Diario (0 3 * * *)	Nuevos uploads normalmente diarios.
channels.list (suscriptores snapshot)	Diario (0 4 * * *)	Serie histórica de suscriptores.
activities.list / videoCategories.list	Semanal (0 5 * * 0)	Cambios menos frecuentes.
Snapshots completos (backup DB)	Mensual (0 0 1 * *)	Backup y almacenamiento histórico.

Ejemplo de workflow GitHub Actions (simplificado):

name: YouTube Data hourly
on:
  schedule:
    - cron: '0 * * * *'  # cada hora (UTC)
jobs:
  fetch_videos:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      - name: Run video fetcher
        env:
          YT_API_KEY: ${{ secrets.YT_API_KEY }}
          DATABASE_URL: ${{ secrets.DATABASE_URL }}
        run: |
          pip install -r requirements.txt
          python scripts/fetch_trending_videos.py --limit 50


Consejo: dividir workflows por frecuencia para optimizar cuota y facilitar trazabilidad.

Autenticación y credenciales

Variables de entorno recomendadas:

YT_API_KEY — API Key (YouTube Data API v3)

DATABASE_URL — URL de Postgres (ej. postgresql://yt_user:yt_password@db:5432/youtube_analysis)

En GitHub Actions: guardar como secrets (Repository Settings → Secrets).

Precauciones: no subir nunca credenciales a git.

Gestión de límites y cuotas

YouTube Data API usa un sistema de “units”. Cada endpoint consume unidades distintas.

Ejemplo: search.list suele costar 100 units; videos.list (por id) puede costar 1 unit por recurso pero depende de part.

Estrategias:

Cachear resultados y evitar solicitudes redundantes.

Respetar pageToken y paginación.

Priorizar llamadas (hourly vs daily) según criticidad.

Registrar consumo y alarmas (logs + métricas).

Ejemplos de uso (curl)

Obtener detalles de un vídeo:

curl -s "https://youtube.googleapis.com/youtube/v3/videos?part=snippet,contentDetails,statistics&id=VIDEO_ID&key=${YT_API_KEY}"


Buscar por palabra clave:

curl -s "https://youtube.googleapis.com/youtube/v3/search?part=snippet&q=machine+learning&type=video&maxResults=25&key=${YT_API_KEY}"


Obtener comentarios:

curl -s "https://youtube.googleapis.com/youtube/v3/commentThreads?part=snippet,replies&videoId=VIDEO_ID&maxResults=100&key=${YT_API_KEY}"

Monitoreo, logs y reintentos

Registrar cada job con:

timestamp

endpoint llamado y parámetros

payload/response size

latency y HTTP code

Implementar reintentos exponenciales ante errores 5xx o rate-limit (429).

Guardar last-run time por job para facilitar incrementales.

Ética, legales y buenas prácticas

Cumplir los Términos de Servicio de YouTube y políticas de uso de API.

No almacenar información personal innecesaria; anonimizar cuando sea posible.

Respetar GDPR: si recoges información que pueda ser personal (p. ej. comentarios identificables), trata con cuidado y define un propósito legítimo.

Documentar y versionar cambios en el pipeline y en el esquema de datos.

Siguientes pasos prácticos (cómo empezar ahora)

Asegúrate de tener YT_API_KEY y acceso a un repositorio con Secrets en GitHub.

Levanta PostgreSQL local con docker compose up -d.

Ejecuta los scripts iniciales: migraciones de tablas y prueba de conexión.

Lanza el primer workflow en GitHub Actions con la cron diaria para testear inicios.

Monitoriza el consumo de cuota y ajusta frecuencias.

Recursos útiles (rápido)

YouTube Data API docs: https://developers.google.com/youtube/v3

GitHub Actions cron docs: https://docs.github.com/actions/learn-github-actions/events-that-trigger-workflows#scheduled-events

Buenas prácticas API: backoff, paginación, caché.