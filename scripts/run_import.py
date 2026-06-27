#!/usr/bin/env python
"""
CLI entry point for Google Sheet import.
"""
import argparse
import logging
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.import_engine import run_import, format_stats

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%H:%M:%S',
)

def main():
    parser = argparse.ArgumentParser(description='Importar datos desde Google Sheet CSV')
    parser.add_argument('--config', default=None,
                        help='Ruta al archivo de configuracin YAML')
    parser.add_argument('--dry-run', action='store_true',
                        help='Solo mostrar lo que se hara, sin modificar BD')
    parser.add_argument('--log', default=None,
                        help='Archivo de log (opcional)')
    args = parser.parse_args()

    if args.log:
        fh = logging.FileHandler(args.log, encoding='utf-8')
        fh.setLevel(logging.INFO)
        logging.getLogger().addHandler(fh)

    # Default config path (script dir / import_config.yaml)
    config_path = args.config or os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        'import_config.yaml'
    )

    if not os.path.exists(config_path):
        print(f" Archivo de configuracin no encontrado: {config_path}")
        sys.exit(1)

    import yaml
    with open(config_path, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)

    print(f"\n Iniciando importacin{' (DRY RUN)' if args.dry_run else ''}...\n")
    stats = run_import(config, dry_run=args.dry_run)
    print(f"\n{format_stats(stats)}\n")

    if args.dry_run:
        print("  Modo dry-run  no se modific la base de datos.\n")
    else:
        errors = len(stats['errors'])
        created = sum(stats['created'].values())
        updated = sum(stats['updated'].values())
        skipped = stats['skipped_no_cedula']
        if errors == 0:
            print(" Importacin completada sin errores.\n")
        else:
            print(f"  Importacin completada con {errors} errores.\n")

if __name__ == '__main__':
    main()
