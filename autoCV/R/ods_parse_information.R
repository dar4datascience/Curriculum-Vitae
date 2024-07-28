# a function using the readODS package that reads an ODS file and has an argument to pass the sheet number to read
read_cv_ods <- function(cv_type_file_path, sheet_number){
  
  # read the ODS file
  cv_data <- read_ods(cv_type_file_path, sheet = sheet_number) |> 
    janitor::clean_names()
  
  # return the data
  return(cv_data)
  
} 

build_cv_components <- function(cv_type_file_path){
  
  # read the ODS file into a list of dataframes
  cv_data <- list(
    "entries" = read_cv_ods(cv_type_file_path, 1), #here goes education and work experience
    "skills" = read_cv_ods(cv_type_file_path, 2),
    "text" = read_cv_ods(cv_type_file_path, 3),
    "contact" = read_cv_ods(cv_type_file_path, 4)
  )
  
  # return the data
  return(cv_data)
  
}

fetch_cv_entries <- function(cv_data){
  
  cv_data_2_use <- cv_data |> 
    pluck("entries") |>
    filter(include == 1)
  
  work_entries <- cv_data_2_use |> 
    filter(cv_category == "industry_positions")
  
  education_entries <- cv_data_2_use |>
    filter(cv_category == "education")
  
  #combine dfs but assign a column of work or education depending on the df
  unified_df <- bind_rows(
    work_entries |> mutate(entry_type = "work"),
    education_entries |> mutate(entry_type = "education")
  )
  
  return(unified_df)
  
  # we need to wrap all the bullet points into a single column
  
  
}

fetch_skills <- function(cv_data){
  
   cv_data |> 
    pluck("skills") 
  
}


