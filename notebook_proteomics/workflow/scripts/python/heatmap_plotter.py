import argparse
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go

from helpers import configure_plotly_browser_env, get_columns_for_group


def safe_write_image(fig, path):
        configure_plotly_browser_env()
        try:
                fig.write_image(path)
        except Exception as exc:
                print(f"Warning: static export skipped for {path}: {exc}")


def plot_heatmap(df, columns=None, pvalueLimit=0.05, foldChangeLimit=1, 
                 comparison=None, samples_group1=None, samples_group2=None, 
                 top_n=50, q_values=False, output_dirs=None):

        columns = ['p-value_StudentTtest','log2FoldChange'] if columns==None else columns
        comparison = ('group1','group2') if comparison is None else comparison
        samples_group1 = ['a','b','c','d'] if samples_group1 is None else samples_group1
        samples_group2 = ['e','f','g','h'] if samples_group2 is None else samples_group2
        
        group1, group2 = comparison
        print(f"Processing comparison: {group1} vs {group2}")

        # Filter for significant proteins
        significant_prot = df[ (df[columns[0]] < pvalueLimit) 
                               & (abs(df[columns[1]]) > foldChangeLimit) ]
        
        # Check if there are sufficient significant proteins
        print("Number of Significant Proteins")
        n = len(significant_prot)
        print(n)
        sig_prot_ids = significant_prot.index.tolist()
        print("Significant Protein IDs")
        print(sig_prot_ids)

        if n < 2:
            print("Insufficient differentially abundant proteins for comparison:", comparison)
            return
        # use top_n hits by abs logFC (column[1])
        if n > top_n:
            print(f"Using only {top_n} proteins for plotting")
            n = top_n
            significant_prot = (significant_prot
                                .sort_values(by=columns[1], key=lambda s: s.abs(), ascending=False)
                                .head(top_n))

        selected_prot_ids = significant_prot.index.tolist()
        # Subset the data for heatmap (significant proteins across the samples of interest)
        heatmap_data = df.loc[selected_prot_ids, samples_group1 + samples_group2].copy()
        # ensure there are no zeros in the data
        heatmap_data.replace(0, np.nan, inplace=True)

        # Extract the descriptions for significant proteins
        significant_descriptions = df.loc[heatmap_data.index, 'Description'].fillna('No description')

        # Prepare the hover text with descriptions (row-based, applied across columns)
        hover_text = heatmap_data.apply(
            lambda row: [f"{val:.2f} ({significant_descriptions.loc[row.name]})" for val in row], 
            axis=1
        ).tolist() # Convert hover_text to a 2D list (one entry per cell)

        # Create the heatmap
        fig = go.Figure(data=go.Heatmap(
            z=np.log2(heatmap_data),  # Numeric values for the heatmap
            x=heatmap_data.columns,   # Sample names
            y=heatmap_data.index,     # Protein IDs
            colorscale='Viridis',
            hoverinfo="text",         # Enable hover text
            text=hover_text           # Set the custom hover text
        ))
        
        height = max(400, n * 20)   # 20px per row, minimum of 400px
        width  = max(600, len(heatmap_data.columns) * 80)
        tick_font = 10 if n <= 50 else (8 if n <= 100 else 6)

        fig.update_layout(
            title=f"Heatmap of Significantly differentially abundant proteins: {group1} vs {group2}",
            xaxis_title="Sample Name",
            yaxis_title="Protein ID",
            xaxis={'type':'category'},
            yaxis=dict(
                tickmode='linear',  # tells Plotly we want evenly spaced ticks
                dtick=1,            # exactly one tick per row
                tickfont=dict(size=tick_font)  
                ),
            autosize=False,
            width = width,
            height = height,
            margin=dict(
                l=150,  # Left margin
                t=50,  # Top margin
                b=50,  # Bottom margin
                pad=4   # Padding between the plot area and the axis lines
            ),
            paper_bgcolor='white',  # Sets the background color of the paper where the plot is drawn
        )

        fig.show()

        # Save
        suffix = '_Q' if q_values else '_P'
        outFileName = f"Heatmap_{group1}_vs_{group2}"
        if output_dirs:
                html_path = Path(output_dirs['html']) / f"{outFileName}{suffix}.html"
                svg_path = Path(output_dirs['svg']) / f"{outFileName}{suffix}.svg"
                png_path = Path(output_dirs['png']) / f"{outFileName}{suffix}.png"
        else:
                html_path = Path(f"{outFileName}{suffix}.html")
                svg_path = Path(f"{outFileName}{suffix}.svg")
                png_path = Path(f"{outFileName}{suffix}.png")
        fig.write_html(html_path,config={'toImageButtonOptions': {'format': 'svg'}})
        safe_write_image(fig, svg_path)
        safe_write_image(fig, png_path)


def main():
        parser = argparse.ArgumentParser(description='Generate heatmaps from a comparison CSV file')
        parser.add_argument('--input', required=True, help='Path to comparison CSV')
        parser.add_argument('--metadata', required=True, help='Path to sample metadata CSV')
        parser.add_argument('--grouping-column', default='group')
        parser.add_argument('--group1', required=True)
        parser.add_argument('--group2', required=True)
        parser.add_argument('--pvalue-col', default='p-value_StudentTtest')
        parser.add_argument('--qvalue-col', default='q-value_StudentTtest')
        parser.add_argument('--log2fc-col', default='log2FoldChange')
        parser.add_argument('--pvalue-limit', type=float, default=0.05)
        parser.add_argument('--qvalue-limit', type=float, default=0.05)
        parser.add_argument('--fold-change-limit', type=float, default=1.0)
        parser.add_argument('--output-dir', required=True)
        args = parser.parse_args()

        df = pd.read_csv(args.input, index_col=0)
        metadata = pd.read_csv(args.metadata)
        samples_group1 = get_columns_for_group(metadata, treatmentGroupColumnID=args.grouping_column, group_name=args.group1)
        samples_group2 = get_columns_for_group(metadata, treatmentGroupColumnID=args.grouping_column, group_name=args.group2)

        output_root = Path(args.output_dir).resolve() / 'output'
        html_dir = output_root / 'HTML'
        png_dir = output_root / 'PNG'
        svg_dir = output_root / 'SVG'
        for directory in [output_root, html_dir, png_dir, svg_dir]:
                directory.mkdir(parents=True, exist_ok=True)
        output_dirs = {'html': html_dir, 'png': png_dir, 'svg': svg_dir}
        plot_heatmap(df, columns=[args.pvalue_col, args.log2fc_col], pvalueLimit=args.pvalue_limit, foldChangeLimit=args.fold_change_limit, comparison=(args.group1, args.group2), samples_group1=samples_group1, samples_group2=samples_group2, output_dirs=output_dirs)
        plot_heatmap(df, columns=[args.qvalue_col, args.log2fc_col], pvalueLimit=args.qvalue_limit, foldChangeLimit=args.fold_change_limit, comparison=(args.group1, args.group2), samples_group1=samples_group1, samples_group2=samples_group2, q_values=True, output_dirs=output_dirs)


if __name__ == '__main__':
        main()
