import argparse
import numpy as np
import pandas as pd
from scipy import stats
from scipy.stats import ttest_ind, levene
from statsmodels.stats.multitest import multipletests
from pathlib import Path
from functools import reduce

import yaml

from helpers import get_columns_for_group, parse_bool
from filter_and_Normalize import uq_normalization


def perform_student_t_test(df, samples_group1, samples_group2, astral):
    """
    Perform a student t-test on each feature in the dataframe between two groups of samples.
    df: pandas DataFrame with all treatment groups
    samples_group1: list of sample names for group 1
    samples_group2: list of sample names for group 2
    student_t_test(df, samples_group1, samples_group2)
    """
    # Combine sample names for the current comparison
    combined_samples = samples_group1 + samples_group2
    
    # Subset the data for the current comparison
    data_subset = df[combined_samples]
    data_subset = data_subset[data_subset.sum(axis=1) > 0]

    # Now, create data_group1 and data_group2 from the cleaned subset
    data_group1 = data_subset[samples_group1]
    data_group2 = data_subset[samples_group2]

    if astral:
        print("Astral data detected, skipping filtering step. No abundance in sample is implied to be 0.")
    else:
        # Filter for proteins where there are at least 3 non-zero values in each group
        # Filter 1: Proteins have >= 3 non-zero values in both data_group1 and data_group2
        filter1 = (data_group1 != 0).sum(axis=1) >= 3
        filter2 = (data_group2 != 0).sum(axis=1) >= 3

        # Filter 2: Proteins have >= 3 non-zero values in data_group1 and all zero values in data_group2
        filter3 = (data_group1 != 0).sum(axis=1) >= 3
        filter4 = (data_group2 == 0).all(axis=1)

        # Filter 3: Proteins have >= 3 non-zero values in data_group2 and all zero values in data_group1
        filter5 = (data_group2 != 0).sum(axis=1) >= 3
        filter6 = (data_group1 == 0).all(axis=1)

        # Combine filters
        combined_filter = (filter1 & filter2) | (filter3 & filter4) | (filter5 & filter6)

        # Debug: Print combined_filter
        # print("combined_filter head:\n", combined_filter.head())

        # Apply the combined filter to the DataFrame
        data_subset = data_subset[combined_filter]    

    # recreate data_group1 and data_group2 after filtering 
    data_group1 = data_subset[samples_group1]
    data_group2 = data_subset[samples_group2]

    # Function to retain only as many zeros as the other group has non-zeros
    
    def retain_zeros(values_group1, values_group2):
        non_zero_count_g1 = (values_group1 != 0).sum()
        non_zero_count_g2 = (values_group2 != 0).sum()

        if non_zero_count_g1 > 3 and non_zero_count_g2 == 0:
            # we remove zeros in group1 that has >3 non-zero abundances and keep equivalent number of zeros in group2
            values_group1 = values_group1[values_group1 != 0]
            values_group2 = values_group2[:non_zero_count_g1]
        elif non_zero_count_g2 > 3 and non_zero_count_g1 == 0:
            # we remove zeros in group1 that has >3 non-zero abundances and keep equivalent number of zeros in group1
            values_group1 = values_group1[:non_zero_count_g2]
            values_group2 = values_group2[values_group2 != 0]
        else:
            # Remove zeros only if neither of the specific conditions are met meaning both have >3 abundances
            values_group1 = values_group1[values_group1 != 0]
            values_group2 = values_group2[values_group2 != 0]

        return values_group1, values_group2

    results = []
    for feature in data_subset.index:  # Assuming each feature is a row
        # remove any potential na values
        values_group1 = data_group1.loc[feature].dropna()
        values_group2 = data_group2.loc[feature].dropna()

        if not astral:
            # retain only as many zeros as the other group has non-zeros
            values_group1, values_group2 = retain_zeros(values_group1, values_group2)

        if len(values_group1) > 2 and len(values_group2) > 2:
            # # Levene test (Brown–Forsythe)
            # lev_stat, lev_p = levene(values_group1, values_group2, center='median', nan_policy="omit")
            # print(f"Levene stat: ", lev_stat,  "  Levene p value: ", lev_p)
            # # t-test
            # if lev_p < 0.05:
            #     student = False
            #     print("Performing Welch's t-test")
            # else:
            #     student = True
            #     print("Performing Student's t-test")
            stat, p_value = ttest_ind(values_group1, values_group2)
            results.append((feature, stat, p_value))

     # Convert results into a DataFrame
    results_df = pd.DataFrame(results, columns=['Feature', 'studentT-testStatistic', 'p-value_StudentTtest'])
    _, qvalue, _, _ = multipletests(results_df['p-value_StudentTtest'], method='fdr_bh')
    results_df['q-value_StudentTtest'] = qvalue
    # create -log 10 of pvalue
    eps = np.finfo(float).tiny
    results_df['-log10(p-value_StudentTtest)'] = -np.log10(np.clip(results_df['p-value_StudentTtest'], eps, 1.0))

    results_df = results_df.set_index('Feature')
    return results_df.sort_values('p-value_StudentTtest', ascending=True)


def test_shapiro_wilk_normality(df, samples_group1, samples_group2):
    """
    Perform a shapiro test on each feature in the dataframe between two groups of samples.
    This test determines if the data is normally distributed.
    * low pvalue means the data is not normally distributed < 0.05 for example
    * high pvalue means the data is normally distributed
    * zero values are removed as they were added to indicate missing values in the data
    df: pandas DataFrame with all treatment groups
    samples_group1: list of sample names for group 1
    samples_group2: list of sample names for group 2
    """
    # Combine sample names for the current comparison
    combined_samples = samples_group1 + samples_group2
     
    # Subset the data for the current comparison
    data_subset = df[combined_samples]
    
    # Remove rows where all values are 0 in the subset
    data_subset = data_subset[data_subset.sum(axis=1) > 0]
    
    # Now, create data_group1 and data_group2 from the cleaned subset
    data_group1 = data_subset[samples_group1]
    data_group2 = data_subset[samples_group2]

    # Filter for proteins where there are at least 3 non-zero values in each group
        # creates a table of true false for values that equal 0 or not
    filter1 =(data_group1 !=0).sum(axis=1)>=3
    filter2 =(data_group2 !=0).sum(axis=1)>=3

    # leaves only rows where both data_group1 and data_group2 pass the filter (>= 3 proteins have non-zero values)
    data_subset = data_subset[filter2 & filter1]
    data_group1 = data_subset[samples_group1]
    data_group2 = data_subset[samples_group2]

    results = []
    for feature in data_subset.index:  # Assuming each feature is a row
        # remove NA values
        values_group1 = data_group1.loc[feature].dropna()
        values_group2 = data_group2.loc[feature].dropna()
        # remove zeros 
        values_group1 = values_group1[values_group1 != 0]
        values_group2 = values_group2[values_group2 != 0]

        if len(values_group1) > 2 and len(values_group2) > 2:
            # Perform Shapiro-Wilk test on the log-transformed data
            stat1, p_value1 = stats.shapiro(values_group1)
            stat2, p_value2 = stats.shapiro(values_group2)
            results.append((feature, stat1, p_value1, stat2, p_value2))

     # Convert results into a DataFrame
    results_df = pd.DataFrame(results, columns=['Feature', 'shapiroStatistic-G1', 'p-value_shapiro-G1','shapiroStatistic-G2', 'p-value_shapiro-G2'])
    results_df = results_df.drop('shapiroStatistic-G1', axis=1)
    results_df = results_df.drop('shapiroStatistic-G2', axis=1)
    # create column for normality
    results_df['Normality-G1'] =  np.where(results_df['p-value_shapiro-G1']>0.05, 'Normal', 'Not Normal')
    results_df['Normality-G2'] =  np.where(results_df['p-value_shapiro-G2']>0.05, 'Normal', 'Not Normal')

    results_df = results_df.set_index('Feature')
    return results_df.sort_values('p-value_shapiro-G1', ascending=True)



def calculate_foldchange(df, samples_group1, samples_group2):
    """
    Calculate, means, foldchange and log fold change on each feature in the dataframe between two groups of samples.
    df: pandas DataFrame with all treatment groups
    samples_group1: list of sample names for group 1
    samples_group2: list of sample names for group 2
    """
    # Combine sample names for the current comparison
    combined_samples = samples_group1 + samples_group2
     
    # Subset the data for the current comparison
    data_subset = df[combined_samples]
    
    # Remove rows where all values are 0 in the subset
    #data_subset = data_subset[(data_subset != 0).any(axis=1)]
    data_subset = data_subset[data_subset.sum(axis=1) > 0]
    
    # # Normalize the data between groups, upper quartile normalization
    # # Dec 13, 2024 I decided to remove the uq normalization within this function and instead normalize the data before calling this function
    # # I am keeping the structure here as I use the data_group1 and data_group2 downstream.
    # sample_group1_75=data_subset[samples_group1].mean(axis=1).describe()["75%"]
    # sample_group2_75=data_subset[samples_group2].mean(axis=1).describe()["75%"]
    # norm_factor = sample_group2_75/sample_group1_75

    # data_group1 = data_subset[samples_group1] # * norm_factor #Dec 13, 2024
    # data_group2 = data_subset[samples_group2]

    # Now, create data_group1 and data_group2 from the cleaned subset
    data_group1 = data_subset[samples_group1]
    data_group2 = data_subset[samples_group2]

    # Jul 10, 2024 changed the df to data_subset here to ensure the keys are present in case of all zeros case
    for feature in data_subset.index:  # Assuming each feature is a row
        values_group1 = data_group1.loc[feature].dropna()
        values_group2 = data_group2.loc[feature].dropna()

        if len(values_group1) > 1 and len(values_group2) > 1:
            # samples_group1 and samples_group2 are lists of column names for each group

            # Calculate mean expression levels for each group (the axis=1 argument specifies that the mean should be calculated across columns (by row))
            # Replace 0 with NaN in group1 and group2, then calculate mean ignoring NaN values

            data_subset['mean_expr_group1'] = data_group1.replace(0, np.nan).mean(axis=1)
            data_subset['mean_expr_group2'] = data_group2.replace(0, np.nan).mean(axis=1)

            # Calculate Fold Change (mean expression of group2 divided by mean expression of group1)
            # Here we add a small constant to avoid division by zero
            epsilon = 1e-8
            data_subset['FoldChange'] = (data_subset['mean_expr_group2'] + epsilon) / (data_subset['mean_expr_group1'] + epsilon)

            # Calculate log2 Fold Change
            data_subset['log2FoldChange'] = np.log2(data_subset['FoldChange'])
            # data_subset['log2FoldChange'].replace(np.log2(epsilon), 0, inplace=True)

        # else:
        #     print(f"Insufficient data for feature {feature}.")

     # Convert results into a DataFrame
    results_df = data_subset

    return results_df.sort_values('FoldChange', ascending=False)


def run_statistics(manifest_path):
    manifest_path = Path(manifest_path).resolve()
    project_root = manifest_path.parents[3]

    with open(manifest_path, 'r', encoding='utf-8') as handle:
        manifest = yaml.safe_load(handle)

    input_cfg = manifest['inputs']
    analysis_cfg = manifest['analysis']
    output_cfg = manifest['outputs']
    flags_cfg = manifest['flags']

    sample_metadata = pd.read_csv(project_root / input_cfg['sample_metadata_csv'])
    comparisons = pd.read_csv(project_root / input_cfg['comparisons_csv'])
    include_series = sample_metadata['include'].apply(parse_bool)
    metadata_used = sample_metadata.loc[include_series].copy()
    metadata_used['column_name'] = metadata_used['source_column']

    annotation = pd.read_csv(project_root / output_cfg['qc_dir'] / 'annotation.csv', index_col=0)
    normalized_data = pd.read_csv(project_root / output_cfg['qc_dir'] / 'normalized_abundance_matrix.csv', index_col=0)
    normalized_data = normalized_data.loc[~normalized_data.index.astype(str).str.startswith('PRTC-')].copy()

    results_dir = project_root / output_cfg['results_dir']
    results_csv_dir = results_dir / 'CSV'
    results_csv_dir.mkdir(parents=True, exist_ok=True)

    comparison_rows = comparisons[comparisons['enabled'].apply(parse_bool)].copy()
    comparison_counts = []
    default_grouping_column = analysis_cfg.get('grouping_column', 'group')
    astral_mode = parse_bool(flags_cfg.get('astral_mode', False))

    for _, row in comparison_rows.iterrows():
        comparison_id = row['comparison_id']
        grouping_column = row.get('grouping_column', default_grouping_column)
        if pd.isna(grouping_column) or str(grouping_column).strip() == '':
            grouping_column = default_grouping_column
        group1 = row['group1']
        group2 = row['group2']
        samples_group1 = get_columns_for_group(metadata_used, treatmentGroupColumnID=grouping_column, group_name=group1)
        samples_group2 = get_columns_for_group(metadata_used, treatmentGroupColumnID=grouping_column, group_name=group2)
        data_subset = normalized_data[samples_group1 + samples_group2].copy()
        if parse_bool(analysis_cfg.get('apply_uq_per_comparison', True)):
            _, data_subset = uq_normalization(data_subset)

        result_df_t = perform_student_t_test(data_subset, samples_group1, samples_group2, astral=astral_mode)
        result_df_shapiro = test_shapiro_wilk_normality(data_subset, samples_group1, samples_group2)
        result_df_fc = calculate_foldchange(data_subset, samples_group1, samples_group2)
        merged_result = reduce(
            lambda left, right: pd.merge(left, right, left_index=True, right_index=True),
            [result_df_t, result_df_shapiro, result_df_fc, annotation],
        ).sort_values('p-value_StudentTtest', ascending=True)

        comparison_filename = results_csv_dir / f'{group1}_vs_{group2}_comparison.csv'
        merged_result.to_csv(comparison_filename, index=True)

        p_cut = float(row['pvalue_cutoff'])
        q_cut = float(row['qvalue_cutoff'])
        fc_cut = float(row['abs_log2fc_cutoff'])
        p_sig = int(((merged_result['p-value_StudentTtest'] < p_cut) & (merged_result['log2FoldChange'].abs() > fc_cut)).sum())
        q_sig = int(((merged_result['q-value_StudentTtest'] < q_cut) & (merged_result['log2FoldChange'].abs() > fc_cut)).sum())
        comparison_counts.append({
            'comparison_id': comparison_id,
            'grouping_column': grouping_column,
            'group1': group1,
            'group2': group2,
            'significant_pvalue_hits': p_sig,
            'significant_qvalue_hits': q_sig,
            'output_file': str(comparison_filename),
        })

    counts_df = pd.DataFrame(comparison_counts)
    counts_df.to_csv(results_dir / 'significant_protein_counts.csv', index=False)
    return counts_df


def main():
    parser = argparse.ArgumentParser(description='Proteomics statistics utilities')
    subparsers = parser.add_subparsers(dest='command', required=True)

    run_parser = subparsers.add_parser('run', help='Run comparison-level statistics from project_manifest.yaml')
    run_parser.add_argument('--manifest', required=True, help='Path to workflow/00_raw_data/config/project_manifest.yaml')

    args = parser.parse_args()
    if args.command == 'run':
        counts_df = run_statistics(args.manifest)
        print(counts_df.to_string(index=False))


if __name__ == '__main__':
    main()
