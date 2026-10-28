from pathlib import Path
from typing import Optional
from typing_extensions import override

from pyfedappwrap.learning.app_types import BaseSelfLearnedApp

from config import MyAppConfig, MyAppInputConfig, MyAppOutputConfig
from model import dysregnet_trial


class MyAPP(BaseSelfLearnedApp[MyAppConfig, MyAppInputConfig, MyAppOutputConfig]):

    def __init__(self):
        super().__init__()

    def run_algorithm(self, data: MyAppInputConfig) -> MyAppOutputConfig:
        output_dir = Path("./output")
        output_dir.mkdir(exist_ok=True, parents=True)

        expr = data.expr
        grn = data.grn
        meta = data.meta

        return dysregnet_trial(expr, grn, meta, self.config, output_dir)

    @override
    def get_test_data(self) -> Optional[dict[str, Path]]:
        return {"meta": Path("data/meta.csv"),
                "expr": Path("data/expr.csv"),
                "grn": Path("data/grn.csv")}
