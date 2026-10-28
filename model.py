from pathlib import Path

import dysregnet
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

from config import MyAppConfig, MyAppOutputConfig


def dysregnet_trial(expr, grn, meta, config: MyAppConfig,
                    output_dir: Path) -> MyAppOutputConfig:
    con_col = config.con_col
    CatCov = config.cat_cov.split(",")
    ConCov = config.con_cov.split(",")

    meta[con_col] = meta[con_col].astype(int)

    """
    Run dysregnet
    """
    data = dysregnet.run(
        expression_data=expr,
        meta=meta,
        CatCov=CatCov,
        ConCov=ConCov,
        GRN=grn,
        normaltest=config.normaltest,
        R2_threshold=config.r2_threshold,
        bonferroni_alpha=config.bonferroni_alpha,
        zscoring=config.zscoring,
        direction_condition=config.direction_condition,
        conCol=con_col
    )

    results = data.get_results()
    output_dir.mkdir(exist_ok=True, parents=True)
    results.to_csv(output_dir / "results.csv", index=False)
    output = create_visualizations(results, output_dir)
    output.results = output_dir / "results.csv"
    return output


def create_visualizations(results: pd.DataFrame, output_dir: Path) -> MyAppOutputConfig:
    """
    Create visualization plots for DysRegNet results.

    Args:
        results: DysRegNet results DataFrame
        output_dir: Output directory for plots

    Returns:
        List of created plot file paths
    """
    plot_files = []
    output = MyAppOutputConfig()
    # Set style
    plt.style.use('default')
    sns.set_palette("husl")

    try:
        # Convert results to numpy array for easier handling
        results_array = results.values

        # 1. Distribution of non-zero values (representing interaction strengths)
        non_zero_values = results_array[results_array != 0]
        if len(non_zero_values) > 0:
            plt.figure(figsize=(10, 6))
            plt.hist(non_zero_values, bins=30, alpha=0.7, edgecolor='black')
            plt.xlabel('Interaction Strength Values')
            plt.ylabel('Frequency')
            plt.title('Distribution of Non-Zero Interaction Strengths')
            plt.grid(True, alpha=0.3)
            r2_plot = output_dir / "r2_distribution.png"
            plt.savefig(r2_plot, dpi=300, bbox_inches='tight')
            plt.close()
            output.adjacency_heatmap = r2_plot

        # 2. Heatmap of results matrix (sample of top interactions)
        if results_array.shape[0] > 0 and results_array.shape[1] > 0:
            plt.figure(figsize=(12, 8))

            # Take a sample for visualization if matrix is too large
            max_size = 50
            if results_array.shape[0] > max_size:
                sample_rows = np.random.choice(results_array.shape[0], max_size, replace=False)
                sample_data = results_array[sample_rows, :]
            else:
                sample_data = results_array

            if results_array.shape[1] > max_size:
                sample_cols = np.random.choice(results_array.shape[1], max_size, replace=False)
                sample_data = sample_data[:, sample_cols]

            sns.heatmap(sample_data, cmap='RdBu_r', center=0,
                        cbar_kws={'label': 'Interaction Strength'})
            plt.title('DysRegNet Results Heatmap (Sample)')
            plt.xlabel('Regulatory Interactions')
            plt.ylabel('Samples/Conditions')

            pval_plot = output_dir / "pvalue_distribution.png"
            plt.savefig(pval_plot, dpi=300, bbox_inches='tight')
            plt.close()
            plot_files.append(pval_plot)

            output.pvalue_distribution = pval_plot

        # 3. Top interactions bar plot
        if len(non_zero_values) > 0:
            plt.figure(figsize=(12, 8))

            # Get top 20 strongest interactions
            flat_values = results_array.flatten()
            top_indices = np.argsort(np.abs(flat_values))[-20:]
            top_values = flat_values[top_indices]

            y_pos = np.arange(len(top_values))
            plt.barh(y_pos, top_values)

            # Create simple labels
            labels = [f"Interaction {i + 1}" for i in range(len(top_values))]

            plt.yticks(y_pos, labels)
            plt.xlabel('Interaction Strength')
            plt.title('Top 20 Strongest Regulatory Interactions')
            plt.tight_layout()

            coef_plot = output_dir / "top_interactions.png"
            plt.savefig(coef_plot, dpi=300, bbox_inches='tight')
            plt.close()
            output.top_interactions = coef_plot

    except Exception as e:
        print(f"Warning: Could not create some visualizations: {e}")
        # Create a simple summary plot as fallback
        plt.figure(figsize=(10, 6))
        plt.text(0.5, 0.5,
                 f'DysRegNet Analysis Completed\n\nResults shape: {results.shape}\n\nVisualization error: {str(e)}',
                 ha='center', va='center', fontsize=12, transform=plt.gca().transAxes)
        plt.title('DysRegNet Analysis Summary')
        plt.axis('off')

        summary_plot = output_dir / "analysis_summary_plot.png"
        plt.savefig(summary_plot, dpi=300, bbox_inches='tight')
        plt.close()
        output.top_interactions = summary_plot

    return output
