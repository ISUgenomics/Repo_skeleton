library(clusterProfiler)
library(org.Mm.eg.db) ## organism database Mm = mouse
library(dplyr)
library(ggplot2)
set.seed(123)

# Input files
path_to_files <- "path to Proteomics/CSV dir"  # dir containing the comparisons
csv_files <- list.files(path = path_to_files,
  pattern = ".*comparison\\.csv$",      ## look for files with this pattern
  full.names = TRUE)

if (length(csv_files) == 0) {stop("No comparison CSV files found in ", path_to_files)}

message("Found ", length(csv_files), " comparison files.")

# Build a global universe of Entrez IDs across input files
universe_ids <- lapply(csv_files, function(f) {
    df0 <- tryCatch(
      read.csv(f, row.names = 1, stringsAsFactors = FALSE, check.names = FALSE),
      error = function(e) NULL
    )
    if (is.null(df0) || !"Entrez Gene ID" %in% colnames(df0)) return(character(0))
    ids0 <- df0[["Entrez Gene ID"]] %>%
        as.character() %>%
        strsplit(split = "[;,]") %>%
        unlist() %>%
        trimws()
    ids0 <- ids0[grepl("^\\d+$", ids0)]
    unique(ids0)
}) %>% unlist() %>% unique()

if (length(universe_ids) == 0) {
    stop("No valid Entrez IDs found across comparison files.")}
message("Universe size (Entrez IDs): ", length(universe_ids))

# Significance parameters
p_col <- "p-value_StudentTtest"
fc_col <- "log2FoldChange"
p_cutoff <- 0.05  ## p value threshold
q_cutoff <- 1
fc_thresh <- 1   ## Fold Change threshold
show_n <- 10  # top GO terms to plot
out_path <- "Temp/out_plot"  # path to output plots 

# Loop over each comparison
for (csv_path in csv_files) {
    fname <- basename(csv_path)
    comp_name <- sub("_comparison\\.csv$", "", fname)
    message("\nProcessing ", comp_name)

    df <- tryCatch(
        read.csv(csv_path, row.names = 1, stringsAsFactors = FALSE, check.names = FALSE),
        error = function(e) {
            warning("Could not read ", fname, ": ", e$message)
            return(NULL)
        }
    )
    if (is.null(df)) next

    # Check required columns
    if (!all(c(p_col, fc_col, "Entrez Gene ID") %in% colnames(df))) {
        warning("Skipping ", fname, ": missing required columns.")
        next
    }

    # Filter significant proteins
    sig_df <- df %>%
        filter(!is.na(.data[["Entrez Gene ID"]]) & .data[["Entrez Gene ID"]] != "") %>%
        filter(.data[[p_col]] < p_cutoff, abs(.data[[fc_col]]) > fc_thresh)

    if (nrow(sig_df) == 0) {
        message("No significant proteins (", p_col, "<", p_cutoff, " & |", fc_col, "|>", fc_thresh, "). Skipping.")
        next
    }

    # Extract Entrez IDs for significant proteins
    sig_entrez <- sig_df[["Entrez Gene ID"]] %>%
        as.character() %>%
        strsplit(split = "[;,]") %>%
        unlist() %>%
        trimws()
    sig_entrez <- unique(sig_entrez[grepl("^\\d+$", sig_entrez)])
    sig_entrez <- intersect(sig_entrez, universe_ids)
    if (length(sig_entrez) == 0) {
        message("No valid Entrez IDs. Skipping.")
        next
    }
    message("Significant Entrez IDs count: ", length(sig_entrez))

    # GO BP enrichment
    ego_bp <- enrichGO(
        gene          = sig_entrez,
        universe      = universe_ids,
        OrgDb         = org.Mm.eg.db,  # mouse
        keyType       = "ENTREZID",
        ont           = "BP",
        pAdjustMethod = "BH",
        pvalueCutoff  = p_cutoff,
        qvalueCutoff  = q_cutoff,
        readable      = TRUE
    )
    ego_df <- as.data.frame(ego_bp)
    if (nrow(ego_df) == 0) {
        message("No enriched GO BP terms. Skipping.")
    } else {
        message("Enriched GO BP terms: ", nrow(ego_df))

        # Dotplot via clusterProfiler
        p <- dotplot(ego_bp, showCategory = show_n) +
            ggtitle(paste0(comp_name, " — GO BP (top ", show_n, ")")) +
            theme(plot.title = element_text(hjust = 0.5))

        # Save outputs
        out_png <- file.path(out_path, paste0("GO_BP_dotplot_", comp_name, ".png"))
        out_pdf <- file.path(out_path, paste0("GO_BP_dotplot_", comp_name, ".pdf"))
        ggsave(out_png, plot = p, width = 6, height = 4, dpi = 300)
        ggsave(out_pdf, plot = p, width = 6, height = 4)

        out_csv <- file.path(out_path, paste0("GO_BP_results_", comp_name, ".csv"))
        write.csv(ego_df, file = out_csv, row.names = FALSE)
    }
  
  ## KEGG enrichment
  kegg_enrich <- enrichKEGG(
    gene          = sig_entrez,
    universe      = universe_ids,
    organism      = "mmu", ## organism #  mmu = mouse
    keyType       = "ncbi-geneid",   # Entrez IDs
    pAdjustMethod = "BH",
    pvalueCutoff  = p_cutoff,            
    qvalueCutoff  = q_cutoff,            
    minGSSize     = 5,              
    maxGSSize     = 500,             
    use_internal_data = FALSE
  )
  
  kegg_df <- as.data.frame(kegg_enrich)
  if (nrow(kegg_df) == 0) {
    message("No enriched KEGG pathways.")
  } else {
    message("KEGG pathways found: ", nrow(kegg_df))
    
    # further filter on raw p-value
    kegg_df <- dplyr::filter(kegg_df, pvalue < 0.05)
    
    # Dotplot
    p_kegg <- dotplot(kegg_enrich, showCategory = show_n) +
      ggtitle(paste0(comp_name, " — KEGG (top ", show_n, ")")) +
      theme(plot.title = element_text(hjust = 0.5))
    
    # Save to PNG and CSV
    out_kegg_png <- file.path(out_path, paste0("KEGG_dotplot1_", comp_name, ".png"))
    out_kegg_csv <- file.path(out_path, paste0("KEGG_results1_",  comp_name, ".csv"))
    
    ggsave(out_kegg_png, plot = p_kegg, width = 6, height = 6, dpi = 300)
    write.csv(kegg_df, out_kegg_csv, row.names = FALSE)
  }
}
