"""
Grava a saída CSV do Arduino em arquivo, marcando cada linha com a
distância de referência medida com trena.

Uso:
    pip install pyserial
    python tools/serial_logger.py --porta COM3 --ref 50 --segundos 30
    python tools/serial_logger.py --porta /dev/ttyUSB0 --ref 100 --segundos 30

Gera/acrescenta em labs/lab01-sonar-basico/resultados/medicoes.csv
"""
import argparse
import csv
import math
import time
from pathlib import Path

import serial

CABECALHO = [
    "ms", "echo_us", "temp_c", "c_ms", "dist_fixa_cm", "dist_comp_cm",
    "valid_count", "timeout_count",
]
RAIZ = Path(__file__).resolve().parent.parent
SAIDA_PADRAO = RAIZ / "labs/lab01-sonar-basico/resultados/medicoes.csv"


def main() -> None:
    ap = argparse.ArgumentParser(description="Logger serial do Lab 01")
    ap.add_argument("--porta", required=True, help="ex.: COM3 ou /dev/ttyUSB0")
    ap.add_argument("--baud", type=int, default=115200)
    ap.add_argument("--ref", type=float, required=True, help="distância real (trena), em cm")
    ap.add_argument("--segundos", type=float, default=30)
    ap.add_argument("--placa", default="mega", help="rótulo da placa (mega, stm32...)")
    ap.add_argument("--saida", type=Path, default=SAIDA_PADRAO)
    args = ap.parse_args()
    if not math.isfinite(args.ref) or args.ref <= 0 or args.segundos <= 0:
        ap.error("--ref e --segundos devem ser números positivos e finitos")

    args.saida.parent.mkdir(parents=True, exist_ok=True)
    novo = not args.saida.exists()
    esperado = ["ref_cm", "placa", *CABECALHO]
    if not novo:
        with args.saida.open(newline="", encoding="utf-8-sig") as existente:
            if next(csv.reader(existente), None) != esperado:
                ap.error("CSV existente tem outro cabeçalho; use --saida com um novo arquivo")

    with serial.Serial(args.porta, args.baud, timeout=2) as porta, \
         args.saida.open("a", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        if novo:
            w.writerow(esperado)

        time.sleep(2)              # o Mega reinicia ao abrir a serial
        porta.reset_input_buffer()
        fim = time.time() + args.segundos
        n = 0
        invalidas = 0
        while time.time() < fim:
            linha = porta.readline().decode(errors="ignore").strip()
            if not linha or linha.startswith(("#", "ms,")):
                continue
            campos = linha.split(",")
            if len(campos) != len(CABECALHO):
                invalidas += 1
                continue
            try:
                echo = int(campos[1])
                validos, timeouts = int(campos[6]), int(campos[7])
                temp, velocidade = float(campos[2]), float(campos[3])
                distancias = [float(campos[4]), float(campos[5])]
                correto = (
                    0 <= validos <= 5 and timeouts == 5 - validos
                    and (echo > 0) == (validos > 0)
                    and math.isfinite(temp) and math.isfinite(velocidade)
                    and (all(math.isfinite(d) for d in distancias) if validos else
                         all(math.isnan(d) for d in distancias))
                )
            except ValueError:
                correto = False
            if not correto:
                invalidas += 1
                continue
            w.writerow([args.ref, args.placa] + campos)
            n += 1
            print(f"[{n:3d}] ref={args.ref:6.1f} cm  medido={campos[5]:>7} cm  "
                  f"T={campos[2]} °C  ecos={validos}/5")

    print(f"\n{n} linhas gravadas; {invalidas} linhas malformadas ignoradas em {args.saida}")


if __name__ == "__main__":
    main()
