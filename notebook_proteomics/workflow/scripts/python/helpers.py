import os
import shutil
from pathlib import Path
from itertools import combinations

import pandas as pd

def extractAnnotation(df, columns_to_select=None): 
    
    if columns_to_select is None:
        columns_to_select = [
            "Description",
            "Biological Process",
            "Cellular Component",
            "Molecular Function",
            "Pfam IDs",
            "Entrez Gene ID",
            "Ensembl Gene ID",
            "Gene Symbol",
            "Gene ID",
            "WikiPathways",
            "Reactome Pathways",
            "# Protein Pathway Groups"
        ]
    
    # Select only the columns that exist in the DataFrame
    existing_columns = df.columns.intersection(columns_to_select)
    
    # Check if any of the columns exist, raise an error if none are found
    if len(existing_columns) == 0:
        raise KeyError("None of the selected columns exist in the DataFrame")
    
    # Create a new DataFrame with only the selected existing columns
    annotation = df[existing_columns]
    print(existing_columns)
    return annotation


def renameColumns(df, regexes=[r'Abundances_\(Grouped\):_', r'_Female']):
    """
    Rename columns to something more manageable
    * This function will rename the column names 
        * It converts ',' to '_'
        * it removes spaces ' ' to '' 
        * takes a regular expression and removes any matches. 
    """
    # Replace spaces with underscores in column names
    df.columns = df.columns.str.replace(' ', '_')

    # Remove commas in column names 
    df.columns = df.columns.str.replace(',', '')

    for regexStr in regexes:
        # Remove redundant "Abundances_(Grouped):_" text from column names 
        df.columns = df.columns.str.replace(regexStr, '', regex=True)

    # Remove "_Female" text from column names 
    #df.columns = df.columns.str.replace('_Female', '', regex=True)

    return df.columns.tolist()

def addCategoryInPlace(df, mapping, sep='_', skip_if_present=True):
    """
    Append category text to each column name if its code substring appears in the name.
    Ensures exactly one underscore before the category. Mutates df in place.
    """
    new_cols = []
    for col in map(str, df.columns):
        updated = col
        for code, cat in mapping.items():
            if code in col:
                # If already ends with _CAT, leave as-is (idempotent)
                if skip_if_present and updated.endswith(f"{sep}{cat}"):
                    break
                # Normalize trailing separators to avoid double underscores
                base = updated.rstrip(sep)
                updated = f"{base}{sep}{cat}"
                break  # stop at first matching code
        new_cols.append(updated)
    df.columns = new_cols
    return df.columns.tolist()


def _resolve_metadata_columns(metadata, treatmentGroupColumnID='category_treatment'):
    """
    Support both legacy notebook metadata schemas and the template sample_metadata.csv schema.
    """
    group_column_candidates = [
        treatmentGroupColumnID,
        'group' if treatmentGroupColumnID in {'treatment', 'category_treatment'} else None,
        'treatment' if treatmentGroupColumnID == 'group' else None,
        'category_treatment',
    ]
    value_column_candidates = ['column_name', 'source_column', 'sample_id']

    group_column = next((c for c in group_column_candidates if c and c in metadata.columns), None)
    value_column = next((c for c in value_column_candidates if c in metadata.columns), None)

    if group_column is None:
        raise KeyError(
            f"None of the expected grouping columns were found in metadata: {group_column_candidates}"
        )
    if value_column is None:
        raise KeyError(
            f"None of the expected sample-name columns were found in metadata: {value_column_candidates}"
        )
    return group_column, value_column


def get_columns_for_group(metadata,treatmentGroupColumnID='category_treatment', group_name="group1"):
    
    # Retrieves column names from the metadata DataFrame for a specific group in the treatementGroupColumnID column.
    group_column, value_column = _resolve_metadata_columns(metadata, treatmentGroupColumnID)
    normalized_group = str(group_name).strip()
    group_series = metadata[group_column].astype(str).str.strip()
    subset = metadata[group_series == normalized_group]
    if 'include' in subset.columns:
        include_series = subset['include'].astype(str).str.strip().str.lower()
        subset = subset[include_series.isin({'true', '1', 'yes', 'y'})]
    return subset[value_column].tolist()


def parse_bool(value):
    if isinstance(value, bool):
        return value
    if value is None:
        return False
    return str(value).strip().lower() in {'true', '1', 'yes', 'y'}


def prepare_manifest(manifest):
    """
    Backward-compatible manifest normalization.
    Returns sections with defaults filled for the simplified manifest.
    """
    project_cfg = manifest.get('project', {})
    inputs = manifest.get('inputs', {})
    analysis = manifest.get('analysis', {})
    outputs = manifest.get('outputs', {})
    flags = manifest.get('flags', {})

    raw_data_file = inputs.get('raw_data_file') or inputs.get('provider_export') or ''
    metadata_source = inputs.get('metadata_source', '')
    analysis_cfg = {
        'input_format': analysis.get('input_format', 'xlsx'),
        'input_index_column': analysis.get('input_index_column', 4),
        'psm_threshold': analysis.get('psm_threshold', 3),
        'psm_column_contains': analysis.get('psm_column_contains', 'PSM'),
        'abundance_column_contains': analysis.get('abundance_column_contains', 'Abundances (Grouped):'),
        'column_rename_regexes': analysis.get('column_rename_regexes', [r'Abundances_\(Grouped\):_', r'_Female']),
        'grouping_column': analysis.get('grouping_column', analysis.get('default_grouping_column', 'group')),
        'normalization_primary': analysis.get('normalization_primary', 'none'),
        'normalization_secondary': analysis.get('normalization_secondary', 'optional'),
        'apply_uq_per_comparison': parse_bool(analysis.get('apply_uq_per_comparison', True)),
        'astral_mode': parse_bool(analysis.get('astral_mode', flags.get('astral_mode', False))),
        'between_group_bias_mode': analysis.get('between_group_bias_mode', 'none'),
        'run_block_size': analysis.get('run_block_size', 11),
        'control_column_contains': analysis.get('control_column_contains', 'Control_Control_Control'),
        'post_normalization_column_merges': analysis.get('post_normalization_column_merges', []),
        'generate_qvalue_plots': parse_bool(analysis.get('generate_qvalue_plots', flags.get('generate_qvalue_plots', True))),
    }
    input_cfg = {
        'provider_export': raw_data_file,
        'metadata_source': metadata_source,
        'sample_metadata_csv': inputs.get('sample_metadata_csv', 'workflow/00_raw_data/config/sample_metadata.csv'),
        'comparisons_csv': inputs.get('comparisons_csv', 'workflow/00_raw_data/config/comparisons.csv'),
        'comparisons_mode': str(inputs.get('comparisons_mode', 'generated')).strip().lower(),
    }
    output_cfg = {
        'qc_dir': outputs.get('qc_dir', 'workflow/01_qc_normalization'),
        'results_dir': outputs.get('results_dir', 'workflow/02_statistics'),
        'plots_dir': outputs.get('plots_dir', 'workflow/03_visualization'),
        'secondary_dir': outputs.get('secondary_dir', 'workflow/04_secondary_analyses'),
        'final_report_dir': outputs.get('final_report_dir', 'workflow/final_report'),
        'scripts_dir': outputs.get('scripts_dir', 'workflow/scripts'),
    }
    flags_cfg = {
        'astral_mode': analysis_cfg['astral_mode'],
        'use_prtc': str(analysis_cfg['normalization_primary']).strip().lower() == 'prtc',
        'generate_qvalue_plots': analysis_cfg['generate_qvalue_plots'],
    }
    return project_cfg, input_cfg, analysis_cfg, output_cfg, flags_cfg


def infer_sample_id(source_column):
    parts = str(source_column).split("_")
    return parts[1] if len(parts) > 1 else str(source_column)


def infer_labels_from_source_column(source_column):
    parts = str(source_column).split("_")
    result = {
        'sample_id': infer_sample_id(source_column),
        'source_column': str(source_column),
        'treatment': '',
        'group': '',
        'replicate': 1,
        'batch_or_run': parts[0] if parts else '',
        'include': True,
        'notes': '',
    }
    if len(parts) >= 5:
        result['treatment'] = parts[-2]
        result['group'] = parts[-1]
    return result


def generate_sample_metadata_from_columns(source_columns):
    rows = [infer_labels_from_source_column(col) for col in source_columns]
    df = pd.DataFrame(rows)
    replicate_counter = {}
    replicates = []
    for _, row in df.iterrows():
        key = (str(row['treatment']).strip(), str(row['group']).strip())
        replicate_counter[key] = replicate_counter.get(key, 0) + 1
        replicates.append(replicate_counter[key])
    df['replicate'] = replicates
    return df[['sample_id', 'source_column', 'treatment', 'group', 'replicate', 'batch_or_run', 'include', 'notes']]


def validate_sample_metadata_against_columns(sample_metadata, source_columns):
    required = {'sample_id', 'source_column', 'include'}
    missing = required.difference(sample_metadata.columns)
    if missing:
        raise KeyError(f'Missing required sample metadata columns: {sorted(missing)}')
    metadata_columns = {
        str(value).strip()
        for value in sample_metadata['source_column'].dropna().tolist()
        if str(value).strip()
    }
    observed_columns = {
        str(value).strip()
        for value in source_columns
        if str(value).strip()
    }
    missing_columns = sorted(metadata_columns - observed_columns)
    if missing_columns:
        raise KeyError(f'Source columns listed in sample_metadata.csv were not found in the data file: {missing_columns}')


def sample_metadata_has_usable_labels(sample_metadata):
    if 'group' in sample_metadata.columns:
        group_blank = sample_metadata['group'].astype(str).str.strip().eq('').all()
        if not group_blank:
            return True
    return len(comparison_grouping_columns(sample_metadata)) > 0


def comparison_grouping_columns(sample_metadata):
    reserved = {
        'sample_id',
        'source_column',
        'replicate',
        'batch_or_run',
        'include',
        'notes',
    }
    candidates = []
    for column in sample_metadata.columns:
        if column in reserved:
            continue
        values = [
            value for value in sample_metadata[column].dropna().astype(str).str.strip().tolist()
            if value
        ]
        if len(set(values)) >= 2:
            candidates.append(column)
    ordered = []
    for preferred in ['treatment', 'challenge', 'group']:
        if preferred in candidates:
            ordered.append(preferred)
    for column in candidates:
        if column not in ordered:
            ordered.append(column)
    return ordered


def generate_comparisons_from_metadata(sample_metadata):
    rows = []
    for grouping_column in comparison_grouping_columns(sample_metadata):
        values = sorted(v for v in sample_metadata[grouping_column].dropna().astype(str).str.strip().unique() if v)
        if len(values) < 2:
            continue
        for group1, group2 in combinations(values, 2):
            rows.append({
                'comparison_id': f'{group1}_vs_{group2}',
                'grouping_column': grouping_column,
                'group1': group1,
                'group2': group2,
                'use_qvalue': True,
                'pvalue_cutoff': 0.05,
                'qvalue_cutoff': 0.05,
                'abs_log2fc_cutoff': 1,
                'enabled': True,
                'notes': '',
            })
    return pd.DataFrame(rows)


def build_placeholder_comparisons():
    return pd.DataFrame([
        {
            'comparison_id': 'fill_in_comparison_01',
            'grouping_column': 'fill_in_grouping_column',
            'group1': 'fill_in_group_a',
            'group2': 'fill_in_group_b',
            'use_qvalue': True,
            'pvalue_cutoff': 0.05,
            'qvalue_cutoff': 0.05,
            'abs_log2fc_cutoff': 1,
            'enabled': True,
            'notes': '',
        }
    ])


def validate_comparisons_against_metadata(comparisons, sample_metadata):
    required = {'comparison_id', 'grouping_column', 'group1', 'group2', 'enabled', 'pvalue_cutoff', 'qvalue_cutoff', 'abs_log2fc_cutoff'}
    missing = required.difference(comparisons.columns)
    if missing:
        raise KeyError(f'Missing required comparison columns: {sorted(missing)}')
    for _, row in comparisons.iterrows():
        grouping_column = str(row['grouping_column']).strip()
        if grouping_column not in sample_metadata.columns:
            raise KeyError(f'Comparison grouping_column not found in sample_metadata.csv: {grouping_column}')
        values = set(sample_metadata[grouping_column].dropna().astype(str).str.strip())
        for field in ['group1', 'group2']:
            val = str(row[field]).strip()
            if val and val not in values:
                comparison_id = row.get('comparison_id', '<unknown>')
                raise KeyError(
                    f'Comparison {comparison_id} references {field}={val} not present in sample_metadata.csv column {grouping_column}'
                )


def configure_plotly_browser_env():
    """
    Prefer a native system browser when available instead of a downloaded browser
    that may not match the host architecture.
    """
    current = os.environ.get('BROWSER_PATH')
    if current:
        return current

    for name in ['google-chrome', 'google-chrome-stable', 'chromium', 'chrome', 'msedge']:
        path = shutil.which(name)
        if path:
            os.environ['BROWSER_PATH'] = path
            return path

    chromium_wrapper = shutil.which('chromium-browser')
    if chromium_wrapper:
        wrapper_text = Path(chromium_wrapper).read_text(encoding='utf-8', errors='ignore')
        if '/snap/bin/chromium' not in wrapper_text:
            os.environ['BROWSER_PATH'] = chromium_wrapper
            return chromium_wrapper

    return None


## for remaking plots
def load_comparison_files(csv_path):
    for f in Path(csv_path).glob("*_vs_*_comparison.csv"):
        stem = f.name.removesuffix("_comparison.csv")
        group1, group2 = stem.split("_vs_", 1)
        yield f, group1, group2
        
