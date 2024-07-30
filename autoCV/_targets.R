# Created by use_targets().
# Follow the comments below to fill in this target script.
# Then follow the manual to check and run the pipeline:
#   https://books.ropensci.org/targets/walkthrough.html#inspect-the-pipeline

# Load packages required to define the pipeline:
library(targets)
# library(tarchetypes) # Load other packages as needed.

# Set target options:
tar_option_set(
  packages = c("dplyr",
               "readODS",
               "purrr"), # Packages that your targets need for their tasks.
  cue = tar_cue(mode = 'always')
  # format = "qs", # Optionally set the default storage format. qs is fast.
  #
  # Pipelines that take a long time to run may benefit from
  # optional distributed computing. To use this capability
  # in tar_make(), supply a {crew} controller
  # as discussed at https://books.ropensci.org/targets/crew.html.
  # Choose a controller that suits your needs. For example, the following
  # sets a controller that scales up to a maximum of two workers
  # which run as local R processes. Each worker launches when there is work
  # to do and exits if 60 seconds pass with no tasks to run.
  #
  #   controller = crew::crew_controller_local(workers = 2, seconds_idle = 60)
  #
  # Alternatively, if you want workers to run on a high-performance computing
  # cluster, select a controller from the {crew.cluster} package.
  # For the cloud, see plugin packages like {crew.aws.batch}.
  # The following example is a controller for Sun Grid Engine (SGE).
  # 
  #   controller = crew.cluster::crew_controller_sge(
  #     # Number of workers that the pipeline can scale up to:
  #     workers = 10,
  #     # It is recommended to set an idle time so workers can shut themselves
  #     # down if they are not running tasks.
  #     seconds_idle = 120,
  #     # Many clusters install R as an environment module, and you can load it
  #     # with the script_lines argument. To select a specific verison of R,
  #     # you may need to include a version string, e.g. "module load R/4.3.2".
  #     # Check with your system administrator if you are unsure.
  #     script_lines = "module load R"
  #   )
  #
  # Set other options as needed.
)

# Run the R scripts in the R/ folder with your custom functions:
tar_source()
# tar_source("other_functions.R") # Source other scripts as needed.

# Change ODS positions locally
# Pull Positions into dataframe
# 1. introduction
# 2. Industry experience
# 3. SKills
# 4. Education
# 5. Certifications
# 6. COntact INformation

cv_type <- "cv types/dar_cv_engineer.ods"

list(
  tar_target( 
    name = cv_components,
    command = build_cv_components(cv_type)
  ),
  tar_target( # fetch entries (industry positions and education)
    name = cv_entries, # this only fetched education entries
    command = fetch_cv_entries(cv_components)
  ),
  tar_target( # fetch skills entries
    name = skills_entries,
    command = fetch_skills(cv_components)
  )
  # parse work n education from: cv category,	title of entry,	location,	primary institution,	Start date of entry (year),	End year of entry Set to "current" if entry is still ongoing,	Each description column is a separate bullet point for the entry. If you need more description bullet points simply add a new column with title "description_{4,5,..}"	,		include?

  # render cv
  # synch proton drive
)
