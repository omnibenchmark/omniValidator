

args <- (commandArgs(trailingOnly = TRUE))
data_folder <- args[1]
# data_folder <- "data/cellbench"

print(data_folder)
dat_files <- list.files(data_folder, pattern = "cellbench")

if(length(dat_files) == 0) stop("dummy error for orchestrator")






