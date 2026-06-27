"""
Import Engine - Google Sheet CSV → Database.
Descarga, limpia, clasifica por cargo, resuelve FKs y hace upsert.
"""

import csv
import re
import logging
import sys
from io import StringIO
from datetime import datetime, date
from unicodedata import normalize as unorm

import requests
from sqlalchemy.orm import Session

sys.path.insert(0, r'C:\xampp\htdocs\estadistica-maranatha-infantil-fastapi')
from utils.env_loader import load_app_env
load_app_env()
from models.database import SessionLocal
from models import (
    Coordinador, Capitan, Servidor, Docente, Auxiliar, Colaborador, Lider
)

logger = logging.getLogger(__name__)

MODEL_MAP = {
    'coordinadores': Coordinador,
    'capitanes': Capitan,
    'servidores': Servidor,
    'docentes': Docente,
    'auxiliares': Auxiliar,
    'colaboradores': Colaborador,
}

# ── Sheet Reader ───────────────────────────────────────────────────

def download_csv(url):
    resp = requests.get(url, timeout=120)
    resp.raise_for_status()
    raw = resp.content
    return raw.decode('utf-8')

def parse_csv(text):
    reader = csv.DictReader(StringIO(text))
    rows = []
    for i, row in enumerate(reader, start=2):
        cleaned = {}
        for k, v in row.items():
            key = k.replace('\ufeff', '').strip()
            cleaned[key] = v.strip() if v else ''
        rows.append(cleaned)
    return rows

# ── Cleaners ───────────────────────────────────────────────────────

def norm(text):
    if not text:
        return ''
    return unorm('NFKC', text).strip()

def clean_cedula(text):
    if not text or not text.strip():
        return None
    t = norm(text).replace('.', '').replace(',', '')
    t = re.sub(r'[Vv]\s*[-–—]\s*', '', t).strip()
    try:
        val = int(t)
        if val == 0:
            return None
        return val
    except ValueError:
        return None

def clean_date(text):
    if not text:
        return None
    t = norm(text)
    for fmt in ['%d/%m/%Y', '%d/%m/%y', '%d-%m-%Y', '%Y-%m-%d']:
        try:
            dt = datetime.strptime(t, fmt)
            if dt.year < 100:
                dt = dt.replace(year=dt.year + 1900)
            if dt.year > date.today().year + 1:
                logger.warning(f"Fecha futura improbable: {t}")
                return None
            return dt.strftime('%Y-%m-%d')
        except ValueError:
            continue
    return None

def clean_edad(text):
    if not text:
        return None
    m = re.search(r'\d+', norm(text))
    if m:
        try:
            return int(m.group())
        except ValueError:
            return None
    return None

def clean_sexo(text):
    if not text:
        return None
    t = norm(text).lower().replace(' ', '')
    if t in ('femenino', 'femenina', 'f', 'mujer'):
        return 'femenino'
    if t in ('masculino', 'masculina', 'm', 'hombre'):
        return 'masculino'
    return None

def clean_hijos(text):
    if not text:
        return 0
    t = norm(text).lower()
    if t in ('ninguno', 'no tengo', 'no tengo hijos', 'no', 'ningun', 'n/a', '0', '-'):
        return 0
    m = re.search(r'\d+', t)
    return int(m.group()) if m else 0

def clean_equipo(text):
    if not text:
        return None
    m = re.search(r'\d+', norm(text))
    return int(m.group()) if m else None

def clean_bool(text):
    if not text:
        return 'no'
    t = norm(text).lower().strip()
    t = re.sub(r'[^\wáéíóú]', '', t)
    if t in ('si', 'sí', 's', 'yes', '1'):
        return 'si'
    if t in ('no', 'n', '0', '-', 'ninguno'):
        return 'no'
    return 'no'

def clean_ecivil(text):
    if not text:
        return None
    t = norm(text).lower().strip()
    t = t.encode('ascii', 'ignore').decode('ascii').strip()
    first = t.split()[0] if t.split() else ''
    if first in ('soltero', 'soltera'):
        return 'soltero'
    if first in ('casado', 'casada'):
        return 'casado'
    valid = {'soltero', 'soltera', 'casado', 'casada', 'divorciado',
             'divorciada', 'viudo', 'viuda', 'concubinato'}
    if t in valid:
        return t
    for v in valid:
        if v in t:
            return v
    return None

def clean_cel(text):
    if not text:
        return None
    t = re.sub(r'[^\d+]', '', norm(text))
    return t or None

def clean_correo(text):
    if not text:
        return None
    t = norm(text).lower()
    if '@' not in t:
        return None
    return t

# ── Field dispatch ─────────────────────────────────────────────────

CLEANERS = {
    'fecha_nacimiento': clean_date,
    'edad': clean_edad,
    'sexo': clean_sexo,
    'cantidad_hijos': clean_hijos,
    'numero_equipo': clean_equipo,
    'celular': clean_cel,
    'correo': clean_correo,
    'estado_civil': clean_ecivil,
    'pertenece_evangelio_cambia': clean_bool,
    'sirve_otra_area': clean_bool,
    'bautizado': clean_bool,
    'asiste_discipulado': clean_bool,
    'usa_transporte': clean_bool,
    'levantado': clean_bool,
    'direccion': lambda v: norm(v) or None,
    'profesion': lambda v: norm(v) or None,
    'tiempo_servicio': lambda v: norm(v) or None,
    'otra_area_detalle': lambda v: norm(v) or None,
}

# ── Cargo classifier ───────────────────────────────────────────────

def classify_cargo(text, patterns, default='servidores'):
    if not text:
        return default
    t = unorm('NFKD', norm(text)).encode('ASCII', 'ignore').decode('ASCII').lower()
    for pat in patterns:
        for kw in pat['match']:
            k = unorm('NFKD', kw).encode('ASCII', 'ignore').decode('ASCII').lower()
            if k in t:
                return pat['tabla']
    return default

# ── FK resolver ────────────────────────────────────────────────────

def resolve_fk(db, table_name, nombre_search):
    if not nombre_search:
        return None
    model = MODEL_MAP.get(table_name)
    if not model:
        return None
    ns = norm(nombre_search).lower()
    records = db.query(model).filter(
        model.nombre.ilike(f'%{ns}%'),
        model.is_deleted == False
    ).all()
    if len(records) == 1:
        return records[0].id
    if len(records) > 1:
        for r in records:
            if r.nombre.lower() == ns:
                return r.id
        return records[0].id
    return None

# ── Upsert ─────────────────────────────────────────────────────────

def upsert(db, table_name, datos):
    model = MODEL_MAP.get(table_name)
    if not model:
        raise ValueError(f"Tabla desconocida: {table_name}")
    cedula = datos.get('cedula')
    existing = db.query(model).filter(
        model.cedula == cedula, model.is_deleted == False
    ).first()
    if existing:
        for k, v in datos.items():
            if k != 'id':
                setattr(existing, k, v)
        return 'updated'
    else:
        create = {k: v for k, v in datos.items() if v is not None}
        record = model(**create)
        db.add(record)
        db.flush()
        return 'created'

# ── Main ───────────────────────────────────────────────────────────

def run_import(config, dry_run=False):
    url = config['sheet']['url']
    columns = config.get('columns', {})
    composed = config.get('campos_compuestos', {})
    cargo_col = config.get('columna_cargo', 'Cargo')
    cargo_pat = config.get('cargo_patrones', [])
    cargo_def = config.get('cargo_default', 'servidores')
    jer_col = config.get('columna_jerarquia', 'Capitán o Responsable')
    fk_cfgs = config.get('fk_lookup', [])

    stats = {
        'total': 0, 'skipped_no_cedula': 0,
        'created': {}, 'updated': {}, 'errors': [],
    }
    for t in MODEL_MAP:
        stats['created'][t] = 0
        stats['updated'][t] = 0

    logger.info(f"Descargando CSV desde: {url}")
    csv_text = download_csv(url)
    rows = parse_csv(csv_text)
    logger.info(f"Filas leídas: {len(rows)}")

    # Map sheet column → DB field
    sheet_to_db = {k: v for k, v in columns.items() if v not in ('_skip', '_compose')}
    compose_cols = [k for k, v in columns.items() if v == '_compose']

    db = SessionLocal()
    try:
        for row_idx, row in enumerate(rows, start=2):
            stats['total'] += 1
            try:
                # --- Cargo → table ---
                cargo = row.get(cargo_col, '')
                table = classify_cargo(cargo, cargo_pat, cargo_def)

                # --- Nombre ---
                if 'nombre' in composed:
                    nombres = norm(row.get(composed['nombre']['from'][0], ''))
                    apellidos = norm(row.get(composed['nombre']['from'][1], ''))
                    nombre = f"{nombres} {apellidos}".strip()
                else:
                    nombre = ''

                # --- Cedula ---
                ced_col = next((s for s, d in sheet_to_db.items() if d == 'cedula'), None)
                cedula = clean_cedula(row.get(ced_col, '')) if ced_col else None
                if cedula is None:
                    stats['skipped_no_cedula'] += 1
                    logger.warning(f"  Fila {row_idx}: sin cédula válida → SKIP")
                    continue

                # --- Build datos dict ---
                datos = {'cedula': cedula, 'nombre': nombre}
                for s_col, d_field in sheet_to_db.items():
                    if d_field == 'cedula':
                        continue
                    raw = row.get(s_col, '')
                    cleaner = CLEANERS.get(d_field)
                    val = cleaner(raw) if cleaner else (norm(raw) or None)
                    if val is not None:
                        datos[d_field] = val

                # --- FK resolution from jerarquía column ---
                jer_raw = row.get(jer_col, '')
                jer_nombre = norm(jer_raw)
                propio = norm(nombre).lower()
                if jer_nombre and jer_nombre.lower() != propio:
                    for fk in fk_cfgs:
                        if table in fk.get('aplica_a', []):
                            fk_id = resolve_fk(db, fk['tabla'], jer_nombre)
                            if fk_id:
                                datos[fk['fk_destino']] = fk_id
                            else:
                                logger.warning(
                                    f"  Fila {row_idx}: '{jer_nombre}' no encontrado "
                                    f"en {fk['tabla']} → NULL"
                                )

                # --- Coordinadores → id_lider (único líder) ---
                if table == 'coordinadores':
                    lider = db.query(Lider).filter(Lider.is_deleted == False).first()
                    if lider:
                        datos['id_lider'] = lider.id

                # --- Upsert ---
                if dry_run:
                    model_rec = MODEL_MAP[table]
                    existing = db.query(model_rec).filter(
                        model_rec.cedula == cedula, model_rec.is_deleted == False
                    ).first()
                    if existing:
                        stats['updated'][table] += 1
                    else:
                        stats['created'][table] += 1
                    logger.info(f"  [{table}] {nombre} (céd {cedula}) → se crearía/actualizaría")
                    continue

                action = upsert(db, table, datos)
                if action == 'created':
                    stats['created'][table] += 1
                elif action == 'updated':
                    stats['updated'][table] += 1

            except Exception as e:
                msg = f"Fila {row_idx}: {e}"
                stats['errors'].append(msg)
                logger.error(f"  ERROR: {msg}")

        if not dry_run:
            db.commit()
            logger.info("✅ Transacción commiteada.")

    except Exception as e:
        db.rollback()
        logger.error(f"Error general: {e}")
        raise
    finally:
        db.close()

    return stats

def format_stats(stats):
    lines = ['=' * 50]
    lines.append('  REPORTE DE IMPORTACIÓN')
    lines.append('=' * 50)
    lines.append(f"  Procesados:          {stats['total']}")
    lines.append(f"  Creados:             {sum(stats['created'].values())}")
    lines.append(f"  Actualizados:        {sum(stats['updated'].values())}")
    lines.append(f"  Saltados (sin céd):  {stats['skipped_no_cedula']}")
    lines.append(f"  Errores:             {len(stats['errors'])}")
    lines.append('  ' + '-' * 46)
    lines.append('  Por tabla:')
    for t in ['coordinadores', 'capitanes', 'servidores', 'docentes', 'auxiliares', 'colaboradores']:
        c = stats['created'].get(t, 0)
        u = stats['updated'].get(t, 0)
        if c or u:
            lines.append(f"    {t:20} {c} creados, {u} actualizados")
    if stats['errors']:
        lines.append('  ' + '-' * 46)
        lines.append('  Errores:')
        for e in stats['errors'][:15]:
            lines.append(f"    - {e}")
        if len(stats['errors']) > 15:
            lines.append(f"    ... y {len(stats['errors']) - 15} más")
    lines.append('=' * 50)
    return '\n'.join(lines)

