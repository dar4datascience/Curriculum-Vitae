# This script builds both the HTML and PDF versions of your CV

# If you want to speed up rendering for googlesheets driven CVs you can cache a
# version of your data This avoids having to fetch from google sheets twice and
# will speed up rendering. It will also make things nicer if you have a
# non-public sheet and want to take care of the authentication in an interactive
# mode.
# To use, simply uncomment the following lines and run them once.
# If you need to update your data delete the "ddcv_cache.rds" file and re-run

library(tidyverse)
source("CV_printing_functions.R")
here::i_am("render_cv.R")



cv_data <- create_CV_object(
  data_location = "https://docs.google.com/spreadsheets/d/1UjkIAPFN03q1RJCrNoULZnE_4wDZFZ-CZHH4KFFRz6M/edit#gid=917338460",
  cache_data = FALSE,
  sheet_is_publicly_readable = FALSE
)

readr::write_rds(cv_data, 'cached_positions.rds')
cache_data <- TRUE

print("hellow im here 1")

# Knit the HTML version
rmarkdown::render("cv.Rmd",
                  params = list(pdf_mode = FALSE, cache_data = cache_data),
                  output_file = 
                    here::here("docs","index.html")
)

print("hellow im here 2")
# Knit the PDF version to temporary html location
tmp_html_cv_loc <- fs::file_temp(ext = ".html")
rmarkdown::render("cv.Rmd",
                  params = list(pdf_mode = TRUE, cache_data = cache_data),
                  output_file = tmp_html_cv_loc)
print("hellow im here 3")
# Convert to PDF using Pagedown
pagedown::chrome_print(input = tmp_html_cv_loc,
                       output = "dar_cv.pdf")
print("hellow im here 4")