# dysregnet

Infers sample-specific dysregulated networks with DysRegNet and exports network results and plots.

## Runtime inputs

Supply input files according to the schemas in `app.yml`.

## Inputs and outputs

### Inputs

| Name | Type | Description |
| --- | --- | --- |
| `grn` | CSV | Gene Regulatory Network (GRN) with two columns in the following order ['TF', 'target']. |
| `meta` | CSV | Gene expression matrix in the format patients as rows (first column - patients/samples ids), and genes as columns. |
| `expr` | CSV | Gene expression matrix in the format - patients as rows (first column - patients/samples ids), and genes as columns. |

### Outputs

| Name | Type | Description |
| --- | --- | --- |
| `adjacency_heatmap` | IMAGE | Distribution of non-zero values (representing interaction strengths) |
| `pvalue_distribution` | IMAGE | Heatmap of results matrix (sample of top interactions) |
| `top_interactions` | IMAGE | Top 20 Strongest Regulatory Interactions |
| `results` | CSV | Results of the analysis in CSV format |

## Configuration

| Name | Default | Description |
| --- | --- | --- |
| `zscoring` | `false` | Apply z-score normalization to expression values before analysis. |
| `bonferroni_alpha` | `0.01` | Bonferroni-corrected significance level (alpha). |
| `r2_threshold` | `0.2` | R² threshold for filtering; set to null to disable. |
| `normaltest` | `false` | Perform D’Agostino-Pearson normality test on residuals. |
| `normaltest_alpha` | `0.001` | Alpha level for the normality test. |
| `direction_condition` | `false` | Enforce directionality condition when assessing dysregulation. |
| `con_cov` | `birth_days_to` | List of continuous covariates. They should match the name of their columns in the meta Dataframe, separated by commas. |
| `cat_cov` | `race,gender` | List of categorical variable names. They should match the name of their columns in the meta Dataframe, separated by commas. |
| `con_col` | `sample_type` | Column name for the condition in the meta DataFrame. |

## Development

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
cp .env.example .env
# Set APP_ID and platform URLs before connecting.
python main.py
```

The Docker base image provides the FL-Net API. `requirements.txt` lists additional
runtime dependencies; `requirements-dev.txt` includes the API for local development.
Runtime datasets and trained models must be supplied separately; see `data/README.md`.

Build with `docker build -t tool-dysregnet .`.
