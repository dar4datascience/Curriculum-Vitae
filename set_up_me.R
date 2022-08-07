# set up once
#install.packages('devtools')
#devtools::install_github("nstrayer/datadrivencv")

datadrivencv::use_datadriven_cv(
  full_name = "Daniel Amieva Rodriguez",
  data_location = "https://docs.google.com/spreadsheets/d/1LDvJX4MpZYm6DsK_4P8XPVpBGDhEqoffoP0jHSwPEBQ",
  pdf_location = "https://github.com/dar4datascience/Curriculum-Vitae/raw/main/dar_cv.pdf",
  html_location = "https://dar4datascience.github.io/Curriculum-Vitae/",
  source_location = "https://github.com/dar4datascience/Curriculum-Vitae"
)