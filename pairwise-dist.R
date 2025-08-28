#!/usr/bin/env Rscript

# Define the required packages
required_packages <- c("castor", "ape", "readxl", "writexl")

# Check which packages are not installed
packages_to_install <- required_packages[!(required_packages %in% installed.packages()[,"Package"])]

# Install only the missing packages
if (length(packages_to_install) > 0) {
  install.packages(packages_to_install, dependencies = TRUE, repos = "https://cloud.r-project.org/")
}

# Load the packages
lapply(required_packages, library, character.only = TRUE)

# Get work dir
work_dir <- sub("/scripts$", "", getwd())
output_dir <- file.path(work_dir, "Output")

# Set directory to Output
setwd(output_dir)

# Initialize an empty list (dictionary equivalent in R)
dict <- list()

# Get all folders ending with "_failed_trees"
folders <- list.dirs(full.names = TRUE, recursive = FALSE)
failed_tree_folders <- grep("_failed_trees$", folders, value = TRUE)

# Iterate through folders
for (folder in failed_tree_folders) {
  # Get all files ending with ".failed_LRT" in the folder
  files <- list.files(folder, pattern = "\\.failed\\_LRT$", full.names = TRUE)

  # Iterate through files
  for (file in files) {
    # Read tree and compute mean pairwise distance
    trees <- read.tree(file)
    # Check if more than one tree is present
    if (class(trees) == "phylo") {
      mean_pd <- mean(get_all_pairwise_distances(trees))  # Single tree case
    } else {
      mean_pd <- mean(sapply(trees, function(tree) mean(get_all_pairwise_distances(tree))))  # Multiple trees case
    }

    # Store in dictionary
    folder_name <- gsub("^\\./|_failed_trees$", "", folder)
    key <- gsub("\\.failed\\_LRT$", "", basename(file))
    dict[[key]] <- list(folder = folder_name, mean_pd = mean_pd)
  }
}

# Convert dict (list) to a data frame
pairwise_dist_df <- do.call(rbind, lapply(names(dict), function(key) {
  data.frame(file = key, folder = dict[[key]]$folder, mean_pd = dict[[key]]$mean_pd, stringsAsFactors = FALSE)
}))

# Go back to main work dir
setwd(work_dir)

# Save as CSV
write.csv(pairwise_dist_df, "pairwise_dist_summary.csv", row.names = FALSE)

# Process lr_df_log.xlsx if present
lr_file <- "Sheets/lr_df_log.xlsx"
if (file.exists(lr_file)) {
  lr_df <- read_excel(lr_file)
  merged_lr_df <- merge(lr_df, pairwise_dist_df, by.x = "genus", by.y = "file", all.x = TRUE)
  # Keep only genera with mean pairwise dist > 0.02
  filtered_lr_df <- subset(merged_lr_df, mean_pd >= 0.02)
  # Remove redundant column
  filtered_lr_df$folder <- NULL
  # Save to Excel
  filtered_lr_file <- "Sheets/lr_df_log_filtered.xlsx"
  write_xlsx(filtered_lr_df, filtered_lr_file)
  print(paste0("Successfully removed genera with mean pairwise distance < 0.02 from loglikelihood file, results written to ", filtered_lr_file))
} else {
  print("'lr_df_log.xlsx' is not present in 'Sheets/' directory")
}

# Process cluster_log.xlsx if present
cluster_file <- "Sheets/cluster_log.xlsx"
if (file.exists(cluster_file)) {
  cluster_df <- read_excel(cluster_file)
  merged_cluster_df <- merge(cluster_df, pairwise_dist_df, by.x = "genus", by.y = "file", all.x = TRUE)
  # Keep only genera with mean pairwise dist > 0.02
  filtered_cluster_df <- subset(merged_cluster_df, mean_pd >= 0.02)
  # Remove redundant column
  filtered_cluster_df$folder <- NULL
  # remove cluster columns where every value = 0
  filtered_cluster_df <- filtered_cluster_df[, sapply(filtered_cluster_df, function(col) !is.numeric(col) || any(col != 0))]
  # Save to Excel
  filtered_cluster_file <- "Sheets/cluster_log_filtered.xlsx"
  write_xlsx(filtered_cluster_df, filtered_cluster_file)
  print(paste0("Successfully removed genera with mean pairwise distance < 0.02 from cluster file, results written to ", filtered_cluster_file))
} else {
  print("'cluster_log.xlsx' is not present in 'Sheets/' directory")
}





### plot
library(ggplot2)
library(dplyr)
library(scales)

data <- read.csv("/Users/thibaultbret/Documents/Radiations-2024/failed_trees_summary.csv")


# Summary statistics by class
class_summary <- data %>%
  group_by(folder) %>%
  summarize(
    mean_value = mean(mean_pd),
    median_value = median(mean_pd),
    min_value = min(mean_pd),
    max_value = max(mean_pd),
    count = n()
  )

# Boxplot by class
p1 <- ggplot(data, aes(x = folder, y = mean_pd, fill = folder)) +
  geom_boxplot() +
  geom_jitter(width = 0.2, alpha = 0.5) +  # Add individual points
  labs(
    title = "Distribution of Mean PD Values by Taxonomic Group",
    x = "Higher Taxonomy",
    y = "Mean PD"
  ) +
  theme_minimal() +
  theme(
    legend.position = "none",
    axis.text.x = element_text(angle = 45, hjust = 1)
  ) +
  scale_y_continuous(trans = "log2", breaks = scales::log_breaks(n = 20, base = 2),
                     labels = function(x) round(x, 5))


ggsave("/Users/thibaultbret/Documents/Radiations-2024/mean-pairwise-dists.jpg", p1, width = 16, height = 12, dpi = 300)
