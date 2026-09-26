#!/usr/bin/env python3
"""
Analisa as medições do Lab 01: erro, desvio padrão e comparação entre a
distância com velocidade fixa (343 m/s) e com compensação de temperatura.

Uso:
    pip install pandas matplotlib
    python tools/analisar.py
    python tools/analisar.py --csv caminho/medicoes.csv
"""
import argparse
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

BASE = Path(__file__).resolve().parent.parent / "labs/lab01-sonar-basico/resultados"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--csv", type=Path, default=BASE / "medicoes.csv")
    args = ap.parse_args()

    df = pd.read_csv(args.csv).dropna(subset=["dist_comp_cm"])
    df["erro_fixa"] = df["dist_fixa_cm"] - df["ref_cm"]
    df["erro_comp"] = df["dist_comp_cm"] - df["ref_cm"]

    resumo = (
        df.groupby(["placa", "ref_cm"])
        .agg(
            n=("dist_comp_cm", "size"),
            temp_media=("temp_c", "mean"),
            media_fixa=("dist_fixa_cm", "mean"),
            media_comp=("dist_comp_cm", "mean"),
            desvio_comp=("dist_comp_cm", "std"),
            erro_fixa=("erro_fixa", "mean"),
            erro_comp=("erro_comp", "mean"),
        )
        .round(2)
        .reset_index()
    )
    print(resumo.to_string(index=False))

    saida_md = args.csv.with_name("resumo.md")
    saida_md.write_text(resumo.to_markdown(index=False), encoding="utf-8")

    fig, ax = plt.subplots(figsize=(7, 4))
    for placa, g in resumo.groupby("placa"):
        ax.errorbar(g["ref_cm"], g["erro_comp"], yerr=g["desvio_comp"],
                    marker="o", capsize=3, label=f"{placa} compensado")
        ax.plot(g["ref_cm"], g["erro_fixa"], "x--", label=f"{placa} 343 m/s fixo")
    ax.axhline(0, color="gray", lw=0.8)
    ax.set_xlabel("Distância de referência (cm)")
    ax.set_ylabel("Erro médio (cm)")
    ax.set_title("HC-SR04: erro de medição por distância")
    ax.grid(alpha=0.3)
    ax.legend()
    fig.tight_layout()
    saida_png = args.csv.with_name("erro_por_distancia.png")
    fig.savefig(saida_png, dpi=150)
    print(f"\nGerados: {saida_md.name}, {saida_png.name}")


if __name__ == "__main__":
    main()
