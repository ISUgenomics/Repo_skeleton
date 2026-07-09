import argparse
import sys
import numpy as np
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.cluster.hierarchy import dendrogram, linkage
from pathlib import Path

import yaml

from helpers import extractAnnotation, renameColumns, parse_bool


## Filter
def filterLowPSM(df, psm_value=3, controlColumnContains='PSM'):
    ## data size before filtering
    df_before = df.shape
    ## Filtering the data for PSM > psm_value
    # Identify the PSM column
    psm_col = [col for col in df.columns if controlColumnContains in col]
    print("PSM Column is " + str(psm_col))
    #print(df.columns)
    if not psm_col:
        print("PSM column not found.")
        sys.exit(1)
    psm_col = psm_col[0]  # Assumes first matching column name is correct

    # Filter for # PSMs > psm_value, remove all rows that contain PRTC, 
    # PRTC columns shouldn't exist in column 11 type data.
    filtered_data = df[(df[psm_col] > psm_value) | df.index.str.contains("PRTC")]
    print("The size of the data before and after filtering are usually different.")
    # data size after filtering
    df_after = filtered_data.shape
    print(df_before,"Original data size")
    print(df_after,"New data size after filtering")
    return filtered_data

def extractAbundanceData(df, abundanceColumnContains='Abundances (Grouped):'):
    """ Retain only Abundance data for each Accession 
    """

    # Identify columns to keep: Accession number and abundances
    columns_to_keep = [col for col in df.columns if abundanceColumnContains in col]

    # Select specified columns and replace missing values with zeros
    df = df[columns_to_keep].fillna(0)

    ## Filter for 0 abundance across all samples

    # Despite filtering for PSMs some proteins are still too low to have abundances. Remove proteins with 0 abundance across all samples
    rowsumFilter = (df.sum(axis=1) != 0)
    filtered_data = df[rowsumFilter]

    # data size after filtering
    df_after = filtered_data.shape

    # Print before and after filtering data size
   
    print(df_after,"New data size after filtering")
    return filtered_data


## PCA

def perform_prtc_pca(normalized_data_sorted, PRTC_rows, n_components=3, perform_log2=True):
    """
    Performs PCA and related analyses on PRTC proteins from a normalized proteomics dataset.

    Parameters:
    - normalized_data_sorted (pd.DataFrame): The normalized proteomics data with proteins as rows and samples as columns.
    - PRTC_rows (list or array-like): List of indices corresponding to PRTC proteins in the DataFrame.
    - n_components (int, optional): Number of principal components to compute. Default is 3.
    - perform_log2 (bool, optional): Whether to apply log2 transformation. Default is True.

    Returns:
    - pc_df (pd.DataFrame): DataFrame containing the principal components for each sample.
    - explained_var (np.ndarray): Array of explained variance ratios for each principal component.
    - correlation_matrix (pd.DataFrame): Correlation matrix of log2-transformed PRTC proteins.
    """

    # Step 1: Extract PRTC Proteins
    try:
        prtc_data = normalized_data_sorted.loc[PRTC_rows].copy()
        print(f"Extracted {prtc_data.shape[0]} PRTC proteins.")
    except KeyError as e:
        raise KeyError(f"One or more PRTC_rows not found in the DataFrame: {e}")

    # Step 2: Replace Zeroes with NaN
    prtc_data.replace(0, np.nan, inplace=True)
    print("Replaced zeroes with NaN.")

    # Step 3: Impute Missing Values (Median Imputation)
    missing_before = prtc_data.isnull().sum().sum()
    prtc_data_imputed = prtc_data.fillna(prtc_data.median())
    missing_after = prtc_data_imputed.isnull().sum().sum()
    print(f"Imputed missing values. Missing before: {missing_before}, after: {missing_after}")

    # Step 4: Log2 Transformation (Optional)
    if perform_log2:
        prtc_data_log = np.log2(prtc_data_imputed + 1)
        print("Applied log2 transformation.")
    else:
        prtc_data_log = prtc_data_imputed.copy()
        print("Skipped log2 transformation.")

    # Step 5: Transpose the Data (Proteins as Columns, Samples as Rows)
    prtc_data_transposed = prtc_data_log.T
    print("Transposed the data to have samples as rows and proteins as columns.")

    # Step 6: Scale the Data
    scaler = StandardScaler()
    scaled_prtc_data = scaler.fit_transform(prtc_data_transposed)
    scaled_prtc_df = pd.DataFrame(scaled_prtc_data,
                                  index=prtc_data_transposed.index,
                                  columns=prtc_data_transposed.columns)
    print("Scaled the data using StandardScaler.")

    # Step 7: Perform PCA
    pca = PCA(n_components=n_components)
    principal_components = pca.fit_transform(scaled_prtc_df)
    pc_columns = [f'PC{i+1}' for i in range(n_components)]
    pc_df = pd.DataFrame(data=principal_components,
                         columns=pc_columns,
                         index=scaled_prtc_df.index)
    explained_var = pca.explained_variance_ratio_
    print(f"Performed PCA with {n_components} components.")

    # Step 8: Explained Variance Output
    for i, var in enumerate(explained_var):
        print(f"PC{i+1} explains {var*100:.2f}% of the variance.")

    # Step 9: 2D PCA Plot Without 'hue'
    plt.figure(figsize=(10, 8))
    sns.scatterplot(x='PC1', y='PC2',
                    data=pc_df,
                    # palette='Set1',
                    s=100, alpha=0.7)
    plt.title('PCA of PRTC Proteins: PC1 vs PC2')
    plt.xlabel(f'PC1 ({explained_var[0]*100:.1f}%)')
    plt.ylabel(f'PC2 ({explained_var[1]*100:.1f}%)')
    plt.grid(True)
    plt.tight_layout()
    plt.show()
    print("Displayed 2D PCA plot (PC1 vs PC2).")

    # Step 10: 3D PCA Plot
    fig = plt.figure(figsize=(12, 10))
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(pc_df['PC1'], pc_df['PC2'], pc_df['PC3'],
               c='skyblue', s=100, alpha=0.7)
    ax.set_title('3D PCA of PRTC Proteins')
    ax.set_xlabel(f'PC1 ({explained_var[0]*100:.1f}%)')
    ax.set_ylabel(f'PC2 ({explained_var[1]*100:.1f}%)')
    ax.set_zlabel(f'PC3 ({explained_var[2]*100:.1f}%)')
    plt.tight_layout()
    plt.show()
    print("Displayed 3D PCA plot (PC1 vs PC2 vs PC3).")

    # Step 11: Hierarchical Clustering Dendrogram
    linked = linkage(prtc_data_imputed, method='ward')
    plt.figure(figsize=(10, 7))
    dendrogram(linked,
               labels=prtc_data_imputed.index.tolist(),
               orientation='top',
               distance_sort='descending',
               show_leaf_counts=True)
    plt.title('Hierarchical Clustering of PRTC Proteins')
    plt.xlabel('PRTC Proteins')
    plt.ylabel('Distance')
    plt.tight_layout()
    plt.show()
    print("Displayed Hierarchical Clustering Dendrogram.")

    # Step 12: Heatmap with Clustering
    sns.clustermap(prtc_data_log, cmap='viridis', linewidths=.5, standard_scale=1)
    plt.title('Heatmap of Log2-Transformed PRTC Proteins with Clustering')
    plt.show()
    print("Displayed Heatmap with Clustering.")

    # Step 13: Correlation Matrix Heatmap
    correlation_matrix = prtc_data_log.T.corr()
    plt.figure(figsize=(12, 10))
    sns.heatmap(correlation_matrix, cmap='coolwarm', annot=False)
    plt.title('Correlation Matrix of PRTC Proteins')
    plt.tight_layout()
    plt.show()
    print("Displayed Correlation Matrix Heatmap.")

    return pc_df, explained_var, correlation_matrix


## Normalize

def normalize_prtc(df):
    # Grab all PRTC rows
    filtered_data_raw=df.copy()
    abundPRTC = df.loc[df.index.str.startswith("PRTC-")]
    # replace the zero values with NAN so it isn't included in the mean calculation 
    abundPRTC = abundPRTC.replace(0, np.nan)

    # calculate the median of each column
      # median was chosen because it is less sensitive to outliers
      # I also tried it with the mean and it resulted in many of the PRTC proteins being differentially expressed.
    medianPRTCvalues=abundPRTC.median(axis=0) # calculate the column means

    # Here we are dividing each column in df dataframe by its corresponding medianPRTC value then multiplying by the mean of PRTC medians to bring the abundance back to a reasonable number 
    filtered_data_normalized=df.divide(medianPRTCvalues)*medianPRTCvalues.mean() 
    print("median:",medianPRTCvalues.median(),"mean:",medianPRTCvalues.mean())  
    return filtered_data_raw, filtered_data_normalized


def uq_normalization(data):
    """
    Perform Upper Quartile (UQ) normalization on the dataset.

    Parameters:
        data (pd.DataFrame): A DataFrame where rows represent features (e.g., genes, proteins)
                            and columns represent samples.

    Returns:
        pd.DataFrame: The UQ-normalized DataFrame.
    """
    ## save raw data 
    raw_data = data.copy()

    # Calculate the 75th percentile (upper quartile) for each sample
    uq_values = data.quantile(0.75, axis=0)

    # Divide each value in the sample by its upper quartile
    normalized_data = data.divide(uq_values, axis=1)

    # Scale back to a common reference (multiply by the mean upper quartile)
    global_uq = uq_values.mean()
    normalized_data *= global_uq

    return raw_data, normalized_data


def plot_data_distribution(raw_data, normalized_data):
    """
    Plot the overall distribution of raw and normalized data using violin plots of log10 values.

    Parameters:
        raw_data (pd.DataFrame): The raw dataset with rows as features and columns as samples.
        normalized_data (pd.DataFrame): The normalized dataset with the same format as raw_data.

    Returns:
        None: Displays the plots.
    """
    # Log10 transform the data for better visualization
    raw_data_log10 = np.log10(raw_data + 1)
    normalized_data_log10 = np.log10(normalized_data + 1)

    # Prepare data for plotting
    raw_melted = raw_data_log10.melt(var_name="Sample", value_name="Log10(Expression/Abundance)")
    normalized_melted = normalized_data_log10.melt(var_name="Sample", value_name="Log10(Expression/Abundance)")

    plt.figure(figsize=(12, 6))

    # Plot raw data distribution
    plt.subplot(1, 2, 1)
    sns.violinplot(x="Log10(Expression/Abundance)", y="Sample", data=raw_melted, density_norm="width")
    plt.title("Raw Data Distribution")

    # Plot normalized data distribution
    plt.subplot(1, 2, 2)
    sns.violinplot(x="Log10(Expression/Abundance)", y="Sample", data=normalized_melted, density_norm="width")
    plt.title("Normalized Data Distribution")

    plt.tight_layout()
    plt.show()


def run_qc_and_normalization(manifest_path):
    manifest_path = Path(manifest_path).resolve()
    project_root = manifest_path.parents[3]

    with open(manifest_path, 'r', encoding='utf-8') as handle:
        manifest = yaml.safe_load(handle)

    input_cfg = manifest['inputs']
    analysis_cfg = manifest['analysis']
    output_cfg = manifest['outputs']
    flags_cfg = manifest['flags']

    provider_export = project_root / input_cfg['provider_export']
    cleaned_export = input_cfg.get('cleaned_export')
    if cleaned_export and str(cleaned_export).strip():
        data_path = project_root / cleaned_export
    else:
        data_path = provider_export

    sample_metadata_path = project_root / input_cfg['sample_metadata_csv']
    qc_dir = project_root / output_cfg['qc_dir']
    plots_dir = project_root / output_cfg['plots_dir']
    qc_dir.mkdir(parents=True, exist_ok=True)
    plots_dir.mkdir(parents=True, exist_ok=True)

    sample_metadata = pd.read_csv(sample_metadata_path)

    input_format = str(analysis_cfg.get('input_format', 'xlsx')).lower()
    index_col = analysis_cfg.get('input_index_column', 4)
    if input_format in {'xlsx', 'xls'}:
        data = pd.read_excel(data_path, index_col=index_col)
    elif input_format == 'csv':
        data = pd.read_csv(data_path, index_col=index_col)
    else:
        raise ValueError(f'Unsupported input_format: {input_format}')

    annotation = extractAnnotation(data)
    filtered_psm = filterLowPSM(
        data,
        psm_value=int(analysis_cfg.get('psm_threshold', 3)),
        controlColumnContains=analysis_cfg.get('psm_column_contains', 'PSM'),
    )
    abundance_data = extractAbundanceData(
        filtered_psm,
        abundanceColumnContains=analysis_cfg.get('abundance_column_contains', 'Abundances (Grouped):'),
    )
    renameColumns(
        abundance_data,
        regexes=analysis_cfg.get('column_rename_regexes', [r'Abundances_\(Grouped\):_', r'_Female']),
    )

    include_series = sample_metadata['include'].apply(parse_bool)
    metadata_used = sample_metadata.loc[include_series].copy()
    missing_columns = sorted(set(metadata_used['source_column']) - set(abundance_data.columns))
    if missing_columns:
        raise KeyError(f'Source columns listed in sample_metadata.csv were not found after column renaming: {missing_columns}')

    abundance_data = abundance_data[metadata_used['source_column'].tolist()].copy()
    metadata_used['column_name'] = metadata_used['source_column']
    metadata_used['treatment'] = metadata_used[analysis_cfg.get('grouping_column', 'group')]

    use_prtc = parse_bool(flags_cfg.get('use_prtc', True))
    prtc_mask = abundance_data.index.astype(str).str.startswith('PRTC-')
    if use_prtc and prtc_mask.any():
        raw_data, normalized_data = normalize_prtc(abundance_data)
    else:
        raw_data = abundance_data.copy()
        normalized_data = abundance_data.copy()

    metadata_used.to_csv(qc_dir / 'sample_metadata_used.csv', index=False)
    metadata_used.to_csv(qc_dir / 'metadata.txt', index=False)
    metadata_used.to_csv(plots_dir / 'metadata.txt', index=False)
    annotation.to_csv(qc_dir / 'annotation.csv', index=True)
    raw_data.to_csv(qc_dir / 'raw_abundance_matrix.csv', index=True)
    normalized_data.to_csv(qc_dir / 'normalized_abundance_matrix.csv', index=True)

    return {
        'qc_dir': str(qc_dir),
        'raw_matrix': str(qc_dir / 'raw_abundance_matrix.csv'),
        'normalized_matrix': str(qc_dir / 'normalized_abundance_matrix.csv'),
        'annotation': str(qc_dir / 'annotation.csv'),
        'metadata_used': str(qc_dir / 'sample_metadata_used.csv'),
    }


def main():
    parser = argparse.ArgumentParser(description='Proteomics QC and normalization utilities')
    subparsers = parser.add_subparsers(dest='command', required=True)

    run_parser = subparsers.add_parser('run', help='Run QC and normalization from project_manifest.yaml')
    run_parser.add_argument('--manifest', required=True, help='Path to workflow/00_raw_data/config/project_manifest.yaml')

    args = parser.parse_args()
    if args.command == 'run':
        result = run_qc_and_normalization(args.manifest)
        for key, value in result.items():
            print(f'{key}: {value}')


if __name__ == '__main__':
    main()
