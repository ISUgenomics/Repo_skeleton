import os
import shutil
from pathlib import Path

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
    subset = metadata[metadata[group_column] == group_name]
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
        
