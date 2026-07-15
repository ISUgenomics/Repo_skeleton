import argparse
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio

from helpers import configure_plotly_browser_env


def safe_write_image(fig, path):
    configure_plotly_browser_env()
    try:
        pio.write_image(fig, path)
    except Exception as exc:
        print(f"Warning: static export skipped for {path}: {exc}")


def infer_static_label(row):
    for column in ["Gene Symbol", "GeneSymbol", "Feature", "Accession", "Description"]:
        if column in row.index:
            value = row[column]
            if pd.notna(value) and str(value).strip() and str(value).strip().lower() != "nan":
                return str(value).strip()
    return ""


def _text_positions(count):
    positions = ["top center", "bottom center", "middle left", "middle right"]
    return [positions[i % len(positions)] for i in range(count)]


def build_static_labeled_volcano(fig, df, x_col, y_col):
    static_fig = go.Figure(fig)
    labeled = df[df["Category"].isin(["Significant Positive", "Significant Negative"])].copy()
    if labeled.empty:
        return static_fig

    labeled["StaticLabel"] = labeled.apply(infer_static_label, axis=1)
    labeled = labeled[labeled["StaticLabel"].astype(str).str.strip() != ""]
    if labeled.empty:
        return static_fig

    for category, text_color in [
        ("Significant Positive", "darkred"),
        ("Significant Negative", "darkblue"),
    ]:
        subset = labeled[labeled["Category"] == category]
        if subset.empty:
            continue
        static_fig.add_trace(
            go.Scatter(
                x=subset[x_col],
                y=subset[y_col],
                mode="text",
                text=subset["StaticLabel"],
                textposition=_text_positions(len(subset)),
                textfont={"size": 10, "color": text_color},
                showlegend=False,
                hoverinfo="skip",
            )
        )

    return static_fig


# Volcano Plot function

def plot_volcano(df, columns=None, pvalue_limit=0.05, fold_change_limit=1, hoverDataList=None, plotTitle='Volcano Plot', outFileName='volcano_plot', q_values=False, output_dirs=None):
    """
    Creates a volcano plot of -log10(p-value) vs log2(fold change).
    """
    if columns is None:
        pval_col, l2fc_col = 'p-value_StudentTtest', 'log2FoldChange'
    else:
        pval_col, l2fc_col = columns

    if hoverDataList is None:
        hoverDataList = ['Feature', 'Description', l2fc_col]
 
  
    def _cat(r):
        pv, fc = r[pval_col], r[l2fc_col]
        if pv < pvalue_limit and fc > fold_change_limit:
            return 'Significant Positive'
        elif pv < pvalue_limit and fc < -fold_change_limit:
            return 'Significant Negative'
        else:
            return 'Not Significant'
        
    df['Category'] = df.apply(_cat, axis=1)

    # if '-log10(p-value)' doesn't exist, create it
    if '-log10(p-value)' not in df.columns:
        df['-log10(p-value)'] = -np.log10(df[pval_col])
    # if 'Feature' doesn't exist, create it
    if 'Feature' not in df.columns:
        df['Feature'] = df.index

    # Pick y-axis
    if q_values:
        if '-log10(q-value)' not in df.columns:
            df['-log10(q-value)'] = -np.log10(df[pval_col]) 
        ydata = '-log10(q-value)'
    else:
        ydata = '-log10(p-value)'
    
    # labels mapping
    labels = {
        l2fc_col: 'Log2 Fold Change',
        ydata: ydata.lstrip('-').replace('-', ' ').title()
    }

    fig = px.scatter(df, x=l2fc_col, y=ydata,
                     color='Category',
                     color_discrete_map={
                         'Significant Positive': 'red',
                         'Significant Negative': 'blue',
                         'Not Significant': 'grey'
                         },
                     title=plotTitle,
                     labels=labels,
                     hover_data=hoverDataList) 


    fig.add_hline(y = -np.log10(pvalue_limit), line_dash="dash", line_color="black")
    fig.add_vline(x = fold_change_limit, line_dash="dash", line_color="black")
    fig.add_vline(x = -fold_change_limit, line_dash="dash", line_color="black")

    # Save
    suffix = '_Q' if q_values else '_P'
    base_name = Path(outFileName).name
    if output_dirs:
        html_path = Path(output_dirs['html']) / f"{base_name}{suffix}.html"
        svg_path = Path(output_dirs['svg']) / f"{base_name}{suffix}.svg"
        png_path = Path(output_dirs['png']) / f"{base_name}{suffix}.png"
    else:
        html_path = Path(f"{outFileName}{suffix}.html")
        svg_path = Path(f"{outFileName}{suffix}.svg")
        png_path = Path(f"{outFileName}{suffix}.png")

    fig.write_html(html_path)
    static_fig = build_static_labeled_volcano(fig, df, l2fc_col, ydata)
    safe_write_image(static_fig, svg_path)
    safe_write_image(static_fig, png_path)

    fig.show()


def main():
    parser = argparse.ArgumentParser(description='Generate volcano plots from a comparison CSV file')
    parser.add_argument('--input', required=True, help='Path to comparison CSV')
    parser.add_argument('--output-dir', required=True, help='Directory for plot outputs')
    parser.add_argument('--pvalue-col', default='p-value_StudentTtest')
    parser.add_argument('--qvalue-col', default='q-value_StudentTtest')
    parser.add_argument('--log2fc-col', default='log2FoldChange')
    parser.add_argument('--pvalue-limit', type=float, default=0.05)
    parser.add_argument('--qvalue-limit', type=float, default=0.05)
    parser.add_argument('--fold-change-limit', type=float, default=1.0)
    args = parser.parse_args()

    df = pd.read_csv(args.input, index_col=0)
    output_root = Path(args.output_dir) / 'output'
    html_dir = output_root / 'HTML'
    png_dir = output_root / 'PNG'
    svg_dir = output_root / 'SVG'
    for directory in [output_root, html_dir, png_dir, svg_dir]:
        directory.mkdir(parents=True, exist_ok=True)
    stem = Path(args.input).stem.replace('_comparison', '').replace('_vs_', '-vs-')
    out_file = f'volcano_plot_{stem}'
    title = stem.replace('-vs-', ' vs ')

    output_dirs = {'html': html_dir, 'png': png_dir, 'svg': svg_dir}
    plot_volcano(df, columns=[args.pvalue_col, args.log2fc_col], pvalue_limit=args.pvalue_limit, fold_change_limit=args.fold_change_limit, plotTitle=title, outFileName=str(out_file), output_dirs=output_dirs)
    plot_volcano(df, columns=[args.qvalue_col, args.log2fc_col], pvalue_limit=args.qvalue_limit, fold_change_limit=args.fold_change_limit, plotTitle=title, outFileName=str(out_file), q_values=True, output_dirs=output_dirs)


if __name__ == '__main__':
    main()
