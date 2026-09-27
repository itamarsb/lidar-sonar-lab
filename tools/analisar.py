"""Resume acurácia e falhas do Lab 01 sem apagar as leituras sem eco.

Uso: python tools/analisar.py [--csv caminho/medicoes.csv]
"""

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

BASE = Path(__file__).resolve().parent.parent / "labs/lab01-sonar-basico/resultados"
COLUNAS = {
    "placa", "ref_cm", "echo_us", "temp_c", "dist_fixa_cm", "dist_comp_cm",
    "valid_count", "timeout_count",
}


def resumir(df: pd.DataFrame) -> pd.DataFrame:
    faltantes = COLUNAS - set(df.columns)
    if faltantes:
        raise ValueError(f"CSV incompatível; colunas ausentes: {', '.join(sorted(faltantes))}")
    if df.empty:
        raise ValueError("CSV sem medições")
    if df[["placa", "ref_cm"]].isna().any().any():
        raise ValueError("Placa e distância de referência são obrigatórias")

    for coluna in COLUNAS - {"placa"}:
        df[coluna] = pd.to_numeric(df[coluna], errors="coerce")
    if df[["ref_cm", "echo_us", "valid_count", "timeout_count"]].isna().any().any():
        raise ValueError("CSV contém contadores ou referência inválidos")
    if (df["ref_cm"] <= 0).any() or (df["echo_us"] < 0).any():
        raise ValueError("Referência e tempo do eco devem ser positivos")
    contadores = df["valid_count"] + df["timeout_count"]
    if (
        (df[["valid_count", "timeout_count"]] < 0).any().any()
        or (contadores != 5).any()
        or (df["valid_count"] % 1 != 0).any()
        or (df["timeout_count"] % 1 != 0).any()
        or ((df["echo_us"] > 0) != (df["valid_count"] > 0)).any()
    ):
        raise ValueError("Contadores de ecos inválidos: esperado 5 disparos por linha")

    chaves = ["placa", "ref_cm"]
    total = df.groupby(chaves).agg(
        n_total=("echo_us", "size"),
        disparos=("valid_count", "sum"),
        timeouts=("timeout_count", "sum"),
    )
    total["taxa_timeout_pct"] = 100 * total["timeouts"] / (total["disparos"] + total["timeouts"])

    validas = df.loc[
        (df["valid_count"] > 0)
        & (df["echo_us"] > 0)
        & df[["dist_fixa_cm", "dist_comp_cm", "temp_c"]].notna().all(axis=1)
    ].copy()
    validas["erro_fixa"] = validas["dist_fixa_cm"] - validas["ref_cm"]
    validas["erro_comp"] = validas["dist_comp_cm"] - validas["ref_cm"]
    validas["abs_fixa"] = validas["erro_fixa"].abs()
    validas["abs_comp"] = validas["erro_comp"].abs()
    medidas = validas.groupby(chaves).agg(
        n_validas=("echo_us", "size"),
        temp_media=("temp_c", "mean"),
        media_fixa=("dist_fixa_cm", "mean"),
        media_comp=("dist_comp_cm", "mean"),
        desvio_comp=("dist_comp_cm", "std"),
        erro_fixa=("erro_fixa", "mean"),
        erro_comp=("erro_comp", "mean"),
        mae_fixa=("abs_fixa", "mean"),
        mae_comp=("abs_comp", "mean"),
    )
    resumo = total.join(medidas, how="left").reset_index()
    resumo["n_validas"] = resumo["n_validas"].fillna(0).astype(int)
    return resumo.round(2)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--csv", type=Path, default=BASE / "medicoes.csv")
    args = ap.parse_args()

    resumo = resumir(pd.read_csv(args.csv))
    print(resumo.to_string(index=False))
    saida_md = args.csv.with_name("resumo.md")
    saida_md.write_text(
        "# Resumo das medições\n\n"
        "Cada linha da serial agrega cinco disparos. A taxa de timeout conta os "
        "disparos sem eco, inclusive em linhas que produziram uma distância válida. "
        "Erros e MAE usam somente linhas com distância válida; grupos sem medição "
        "válida exibem valores ausentes. Dados simulados não são evidência experimental.\n\n"
        + resumo.fillna("—").to_markdown(index=False) + "\n",
        encoding="utf-8",
    )

    fig, ax = plt.subplots(figsize=(8, 4.5))
    com_dados = resumo.loc[resumo["n_validas"] > 0]
    for placa, g in com_dados.groupby("placa"):
        ax.errorbar(g["ref_cm"], g["erro_comp"], yerr=g["desvio_comp"].fillna(0),
                    marker="o", capsize=3, label=f"{placa}: compensado ± 1 desvio")
        ax.plot(g["ref_cm"], g["erro_fixa"], "x--", label=f"{placa}: 343 m/s")
    ax.axhline(0, color="gray", lw=0.8)
    ax.set_xlabel("Distância de referência (cm)")
    ax.set_ylabel("Viés médio das leituras válidas (cm)")
    ax.set_title("HC-SR04: erro por distância; veja também a taxa de timeout na tabela")
    ax.grid(alpha=0.3)
    if not com_dados.empty:
        ax.legend()
    fig.tight_layout()
    saida_png = args.csv.with_name("erro_por_distancia.png")
    fig.savefig(saida_png, dpi=150)
    plt.close(fig)
    print(f"\nGerados: {saida_md.name}, {saida_png.name}")


if __name__ == "__main__":
    main()
