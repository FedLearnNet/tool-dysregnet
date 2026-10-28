from pathlib import Path
from typing import Any

from pydantic.dataclasses import dataclass
from pyfedappwrap.learning.run_runfig import AppConfig, AppInputConfig, AppOutputConfig


@dataclass
class MyAppConfig(AppConfig):
    zscoring: bool = False
    bonferroni_alpha: float = 1e-2
    r2_threshold: float | None = None
    normaltest: bool = False
    normaltest_alpha: float = 1e-3
    direction_condition: bool = False
    con_cov: str = None
    cat_cov: str = None
    con_col: str = None

@dataclass
class MyAppInputConfig(AppInputConfig):
    meta: Any = None
    expr: Any = None
    grn: Any = None

# outputs
@dataclass
class MyAppOutputConfig(AppOutputConfig):
    pvalue_distribution: Path | None = None
    adjacency_heatmap: Path | None = None
    top_interactions: Path | None = None
    results: Path | None = None
