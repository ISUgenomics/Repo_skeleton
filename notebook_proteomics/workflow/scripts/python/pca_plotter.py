import pandas as pd
import numpy as np
import argparse
from pathlib import Path
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from itertools import combinations
import plotly.express as px
from sklearn.cross_decomposition import PLSRegression
from sklearn.metrics import accuracy_score
from sklearn.model_selection import StratifiedKFold
from tqdm import tqdm  # For progress bars
import plotly.express as px
from helpers import configure_plotly_browser_env, get_columns_for_group


def safe_write_image(fig, path):
    configure_plotly_browser_env()
    try:
        fig.write_image(path)
    except Exception as exc:
        print(f"Warning: static export skipped for {path}: {exc}")


def compute_pca(df, comparison=('Obese_DMBA', 'Slim_DMBA'), samples_group1=['a','b','c','d'], samples_group2=['e','f','g','h'], n_components=3, scale_data=True):
    """
    Compute PCA on the given dataframe for the specified sample groups, returning both
    the PC scores DataFrame and the explained variance array.
    
    Args:
        df (pd.DataFrame): Input dataframe with rows as features (genes/proteins) and columns as samples.
        comparison (tuple): Tuple containing two group labels for the title and PC_df annotation.
        samples_group1 (list): Samples in the first group.
        samples_group2 (list): Samples in the second group.
        n_components (int): Number of principal components to compute.
        scale_data (bool): Whether to scale the data (standardize) before PCA.
    
    Returns:
        pc_df (pd.DataFrame): DataFrame with principal components and group assignment.
        explained_var (np.array): Array of explained variance ratios for each principal component.
    """
    group1, group2 = comparison
    sample_cols = samples_group1 + samples_group2
    df_subset = df[sample_cols].copy()
    
    # Handle zero/negative values (if needed) and log transform
    # Check for non-positive values if a log transform is needed
    if (df_subset <= 0).any().any():
        # Replace zeros with small positive number
        df_subset = df_subset.replace(0, np.nan)
        df_subset = df_subset.fillna(df_subset.min().min() * 0.1)
    
    # Log2 transform if not already done
    df_log = np.log2(df_subset)
    
    # Scale data if desired
    if scale_data:
        scaler = StandardScaler()
        data_for_pca = scaler.fit_transform(df_log.T)  # transpose so samples are rows
    else:
        data_for_pca = df_log.T.values

    pca = PCA(n_components=n_components)
    principal_components = pca.fit_transform(data_for_pca)
    explained_var = pca.explained_variance_ratio_ * 100

    # Create a DataFrame with PC scores
    pc_cols = [f"PC{i+1}" for i in range(n_components)]
    pc_df = pd.DataFrame(principal_components, index=df_log.columns, columns=pc_cols)
    
    # Assign groups for coloring
    pc_df['Group'] = np.where(pc_df.index.isin(samples_group1), group1, group2)
    
    return pc_df, explained_var

def plot_all_2d_pca_pairs(pc_df, comparison=('Obese_DMBA', 'Slim_DMBA'), explained_var=None, output_dirs=None):
    """
    Given a DataFrame with at least three PCA components (PC1, PC2, PC3),
    produce separate 2D scatter plots for each pair of the first three PCs.
    """
    group1, group2 = comparison
    pc_list = ['PC1', 'PC2', 'PC3']
    pc_pairs = list(combinations(pc_list, 2))

    for (x_pc, y_pc) in pc_pairs:
        if explained_var is not None:
            x_label = f"{x_pc} ({explained_var[int(x_pc[2])-1]:.2f}%)"
            y_label = f"{y_pc} ({explained_var[int(y_pc[2])-1]:.2f}%)"
        else:
            x_label, y_label = x_pc, y_pc

        fig = px.scatter(
            pc_df,
            x=x_pc,
            y=y_pc,
            color='Group',          # make sure to specify 'color' and 'symbol' to use maps
            symbol='Group',
            color_discrete_map={group1: "purple", group2: "green"},
            symbol_map={group1: "diamond", group2: "circle"},
            hover_name=pc_df.index,
            title=f"{x_pc} vs {y_pc} PCA: {group1} vs {group2}",
            labels={x_pc: x_label, y_pc: y_label}
        )

        fig.update_layout(
            xaxis_title=x_label,
            yaxis_title=y_label,
            paper_bgcolor='white',
            template='plotly_white'
        )
        fig.update_traces(marker=dict(size=10))
        fig.show()
        file_name = f"PCA_{group1}_vs_{group2}_{x_pc}_vs_{y_pc}"
        if output_dirs:
            html_path = Path(output_dirs['html']) / f"{file_name}.html"
            png_path = Path(output_dirs['png']) / f"{file_name}.png"
        else:
            html_path = Path(f"{file_name}.html")
            png_path = Path(f"{file_name}.png")
        fig.write_html(html_path, config={'toImageButtonOptions': {'format': 'svg'}})
        safe_write_image(fig, png_path)


def plot_pca_3d(pc_df, comparison=('group1', 'group2'), explained_var=None, output_dirs=None):
    """
    Given a DataFrame (pc_df) with at least three PCA components (PC1, PC2, PC3),
    produce a 3D scatter plot.
    
    Args:
        pc_df (pd.DataFrame): DataFrame containing columns 'PC1', 'PC2', 'PC3', and 'Group'.
        comparison (tuple): Tuple with labels for the title, e.g. ('Group1', 'Group2').
        explained_var (array-like): Explained variance ratios * 100 for each PC.
    """
    group1, group2 = comparison

    if explained_var is not None:
        x_label = f"PC1 ({explained_var[0]:.2f}%)"
        y_label = f"PC2 ({explained_var[1]:.2f}%)"
        z_label = f"PC3 ({explained_var[2]:.2f}%)"
    else:
        x_label, y_label, z_label = "PC1", "PC2", "PC3"

    fig = px.scatter_3d(
        pc_df,
        x='PC1',
        y='PC2',
        z='PC3',
        color='Group',          # make sure to specify 'color' and 'symbol' to use maps
        symbol='Group',
        color_discrete_map={group1: "purple", group2: "green"},
        symbol_map={group1: "diamond", group2: "circle"},
        hover_name=pc_df.index,
        title=f"3D PCA: {group1} vs {group2}",
        labels={
            'PC1': x_label,
            'PC2': y_label,
            'PC3': z_label
        }
    )

    fig.update_layout(
        scene=dict(
            xaxis_title=x_label,
            yaxis_title=y_label,
            zaxis_title=z_label
        ),
        paper_bgcolor='white',
        template='plotly_white'
    )

    fig.show()
    file_name = f"3D_PCA_{group1}_vs_{group2}.html"
    html_path = Path(output_dirs['html']) / file_name if output_dirs else Path(file_name)
    fig.write_html(html_path, config={'toImageButtonOptions': {'format': 'svg'}})


#NOTES
# Cross-Validated Accuracy: gives an estimate on how well the groups fit when we use Stratified K-Fold Cross-Validation with a default of 5 splits.  
# n_splits represents number of folds to use, # of subsets the data is split into
# Seeing a sample or two as not always placed in the correct group is not uncommon and usually are those that border the 95% ellipse of the other group.


def plot_pls_da_with_cv(df, 
                                comparison=('group1', 'group2'), 
                                samples_group1=['a','b','c','d'], 
                                samples_group2=['e','f','g','h'], 
                                n_components=2, 
                                scale_data=True, 
                                n_splits=5,
                                output_dirs=None):
    """
    Perform PLS-DA with cross-validation and create a score plot including confidence ellipses.
    """
    group1, group2 = comparison
    sample_cols = samples_group1 + samples_group2

    # Subset the dataframe for the samples of interest
    df_subset = df[sample_cols].copy()

    # Handle zero or negative values if log transform is needed
    if (df_subset <= 0).any().any():
        df_subset = df_subset.replace(0, np.nan)
        df_subset = df_subset.fillna(df_subset.min().min() * 0.1)

    # Log2 transform the data if not already done
    df_log = np.log2(df_subset)

    # Transpose to have samples as rows, features as columns
    X = df_log.T.values
    sample_names = df_log.columns.tolist()

    # Create a binary response vector: 0 for group1, 1 for group2
    y = np.array([0 if sample in samples_group1 else 1 for sample in sample_names])

    # Scale data if needed
    if scale_data:
        scaler = StandardScaler()
        X = scaler.fit_transform(X)

    # Initialize PLS-DA model
    pls = PLSRegression(n_components=n_components)

    # Cross-validation cannot exceed the smallest class size.
    class_counts = np.bincount(y)
    max_splits = int(class_counts.min()) if len(class_counts) else 0
    if max_splits < 2:
        raise ValueError("PLS-DA cross-validation requires at least 2 samples per group.")
    n_splits = min(n_splits, max_splits)
    skf = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=42)
    cv_scores = np.zeros_like(y, dtype=float)
    cv_predictions = np.zeros_like(y, dtype=float)

    for train_index, test_index in tqdm(skf.split(X, y), desc="Cross-Validation"):
        X_train, X_test = X[train_index], X[test_index]
        y_train, y_test = y[train_index], y[test_index]

        pls.fit(X_train, y_train)
        y_pred = pls.predict(X_test).ravel()
        y_pred_class = np.where(y_pred > 0.5, 1, 0)
        cv_predictions[test_index] = y_pred_class
        cv_scores[test_index] = accuracy_score(y_test, y_pred_class)
    print(cv_scores)
    overall_cv_accuracy = np.mean(cv_scores)
    print(f"Cross-Validated Accuracy: {overall_cv_accuracy:.2f}")

    # Fit the model on the entire dataset
    pls.fit(X, y)
    scores = pls.x_scores_

    # Create DataFrame for plotting
    score_df = pd.DataFrame(scores, index=sample_names, columns=[f"LV{i+1}" for i in range(n_components)])
    score_df['Group'] = np.where(score_df.index.isin(samples_group1), group1, group2)
    score_df['CV_Prediction'] = np.where(cv_predictions == 0, group1, group2)
    score_df['CV_Score'] = cv_scores

    # Initialize Plotly figure
    fig = px.scatter(
        score_df,
        x="LV1",
        y="LV2",
        color='Group',
        symbol='CV_Prediction',
        hover_name=score_df.index,
        hover_data={
            "LV1": ":.2f",
            "LV2": ":.2f",
            "CV_Score": True,  # Add CV score to the hover information
            "Group": True,
            "CV_Prediction": True,
        },
        title=f"PLS-DA Score Plot with Cross-Validation: {group1} vs {group2}               Cross-Validated Accuracy: {overall_cv_accuracy:.2f}",
        labels={"LV1": "LV1", "LV2": "LV2"},
        symbol_map={group1: "circle", group2: "diamond"},
        template='plotly_white',
        color_discrete_map={group1: "purple", group2: "green"}  # Map group1 to purple and group2 to green

    )

    # Function to generate confidence ellipse paths
    def confidence_ellipse(x, y, n_std=1.96, size=100):
        if x.size != y.size:
            raise ValueError("x and y must be the same size")

        cov = np.cov(x, y)
        mean = np.mean(x), np.mean(y)

        eigenvals, eigenvecs = np.linalg.eigh(cov)
        order = eigenvals.argsort()[::-1]
        eigenvals, eigenvecs = eigenvals[order], eigenvecs[:, order]

        angle = np.degrees(np.arctan2(*eigenvecs[:,0][::-1]))

        chisquare_val = 5.991  # 95% confidence interval in 2D
        width, height = 2 * np.sqrt(eigenvals * chisquare_val)

        theta = np.linspace(0, 2 * np.pi, size)
        ellipse = np.array([width / 2 * np.cos(t) for t in theta]), np.array([height / 2 * np.sin(t) for t in theta])

        R = np.array([[np.cos(np.radians(angle)), -np.sin(np.radians(angle))],
                      [np.sin(np.radians(angle)),  np.cos(np.radians(angle))]])
        ellipse_rotated = R @ ellipse

        ellipse_rotated[0] += mean[0]
        ellipse_rotated[1] += mean[1]

        path = "M " + " L ".join([f"{x_val},{y_val}" for x_val, y_val in zip(ellipse_rotated[0], ellipse_rotated[1])]) + " Z"
        return path

    # Add confidence ellipses for each group
    for grp, color in zip([group1, group2], ['purple', 'green']):
        grp_data = score_df[score_df['Group'] == grp]
        if len(grp_data) < 2:
            continue  # Cannot compute ellipse with less than 2 points

        x = grp_data['LV1'].values
        y_vals = grp_data['LV2'].values

        ellipse_path = confidence_ellipse(x, y_vals, n_std=2.4477, size=100)  # ~95% CI

        fig.add_shape(
            type="path",
            path=ellipse_path,
            line=dict(color=color, dash='dash'),
            fillcolor=color,
            opacity=0.2,
            layer="below"
        )

    # Update layout
    fig.update_layout(
        xaxis_title="LV1",
        yaxis_title="LV2",
        paper_bgcolor='white',
    )

    # Update marker properties
    fig.update_traces(marker=dict(size=10, opacity=0.7))

    # Display the plot
    fig.show()

    # Save plots
    file_name = f"PLS-DA_CV_Ellipses_{group1}_vs_{group2}"
    if output_dirs:
        html_path = Path(output_dirs['html']) / f"{file_name}.html"
        png_path = Path(output_dirs['png']) / f"{file_name}.png"
    else:
        html_path = Path(f"{file_name}.html")
        png_path = Path(f"{file_name}.png")
    fig.write_html(html_path)
    safe_write_image(fig, png_path)


def main():
    parser = argparse.ArgumentParser(description='Generate PCA and PLS-DA plots from a normalized matrix')
    parser.add_argument('--input', required=True, help='Path to normalized abundance matrix CSV')
    parser.add_argument('--metadata', required=True, help='Path to sample metadata CSV')
    parser.add_argument('--grouping-column', default='group')
    parser.add_argument('--group1', required=True)
    parser.add_argument('--group2', required=True)
    parser.add_argument('--output-dir', required=True)
    args = parser.parse_args()

    df = pd.read_csv(args.input, index_col=0)
    metadata = pd.read_csv(args.metadata)
    samples_group1 = get_columns_for_group(metadata, treatmentGroupColumnID=args.grouping_column, group_name=args.group1)
    samples_group2 = get_columns_for_group(metadata, treatmentGroupColumnID=args.grouping_column, group_name=args.group2)
    comparison = (args.group1, args.group2)

    output_root = Path(args.output_dir).resolve() / 'output'
    html_dir = output_root / 'HTML'
    png_dir = output_root / 'PNG'
    svg_dir = output_root / 'SVG'
    for directory in [output_root, html_dir, png_dir, svg_dir]:
        directory.mkdir(parents=True, exist_ok=True)
    output_dirs = {'html': html_dir, 'png': png_dir, 'svg': svg_dir}
    pc_df, explained_var = compute_pca(df, comparison=comparison, samples_group1=samples_group1, samples_group2=samples_group2, n_components=3, scale_data=True)
    plot_all_2d_pca_pairs(pc_df, comparison=comparison, explained_var=explained_var, output_dirs=output_dirs)
    plot_pca_3d(pc_df, comparison=comparison, explained_var=explained_var, output_dirs=output_dirs)
    plot_pls_da_with_cv(df, comparison=comparison, samples_group1=samples_group1, samples_group2=samples_group2, n_components=2, scale_data=True, n_splits=5, output_dirs=output_dirs)


if __name__ == '__main__':
    main()
