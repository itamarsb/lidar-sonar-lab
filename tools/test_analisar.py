"""Regressão: timeouts continuam no denominador e não entram na acurácia."""

import unittest

import pandas as pd
from analisar import resumir


class ResumoTests(unittest.TestCase):
    def test_timeout_parcial_e_total(self) -> None:
        df = pd.DataFrame([
            {
                "placa": "mega", "ref_cm": 50, "echo_us": 2915, "temp_c": 24,
                "dist_fixa_cm": 50, "dist_comp_cm": 51,
                "valid_count": 1, "timeout_count": 4,
            },
            {
                "placa": "mega", "ref_cm": 50, "echo_us": 0, "temp_c": 24,
                "dist_fixa_cm": float("nan"), "dist_comp_cm": float("nan"),
                "valid_count": 0, "timeout_count": 5,
            },
        ])
        row = resumir(df).iloc[0]
        self.assertEqual(row["n_total"], 2)
        self.assertEqual(row["n_validas"], 1)
        self.assertEqual(row["timeouts"], 9)
        self.assertEqual(row["taxa_timeout_pct"], 90)
        self.assertEqual(row["mae_comp"], 1)

    def test_grupo_sem_eco_permanece_no_resumo(self) -> None:
        df = pd.DataFrame([{
            "placa": "mega", "ref_cm": 200, "echo_us": 0, "temp_c": 20,
            "dist_fixa_cm": float("nan"), "dist_comp_cm": float("nan"),
            "valid_count": 0, "timeout_count": 5,
        }])
        row = resumir(df).iloc[0]
        self.assertEqual(row["n_validas"], 0)
        self.assertEqual(row["taxa_timeout_pct"], 100)
        self.assertTrue(pd.isna(row["mae_comp"]))


if __name__ == "__main__":
    unittest.main()
