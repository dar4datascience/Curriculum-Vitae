# a function using the readODS package that reads an ODS file and has an argument to pass the sheet number to read
read_cv_ods <- function(cv_type_file_path,
                        sheet_number,
                        ...){
  
  # read the ODS file
  cv_data <- read_ods(cv_type_file_path,
                      sheet = sheet_number,
                      ...) |> 
    janitor::clean_names()
  
  # return the data
  return(cv_data)
  
} 

build_cv_components <- function(cv_type_file_path){
  
  # read the ODS file into a list of dataframes
  cv_data <- list(
    "entries" = read_cv_ods(cv_type_file_path, 1, skip = 1), #here goes education and work experience
    "skills" = read_cv_ods(cv_type_file_path, 2, skip = 1),
    "text" = read_cv_ods(cv_type_file_path, 3, skip = 1),
    "contact" = read_cv_ods(cv_type_file_path, 4, skip = 1)
  )
  
  # return the data
  return(cv_data)
  
}

fetch_cv_entries <- function(cv_data){
  
  cv_data_2_use <- cv_data |> 
    pluck("entries") |>
    filter(in_resume == 1)
  
  work_entries <- cv_data_2_use |> 
    filter(section == "industry_positions")
  
  education_entries <- cv_data_2_use |>
    filter(section == "education")
  
  #combine dfs but assign a column of work or education depending on the df
  unified_entries_df <- bind_rows(
    work_entries |> mutate(entry_type = "work"),
    education_entries |> mutate(entry_type = "education")
  )
  
  return(unified_entries_df)
  
  # we need to wrap all the bullet points into a single column
  
  
}

fetch_skills <- function(cv_data){
  
   cv_data |> 
    pluck("skills") |> 
    pull(skill) |> 
    paste(collapse = ", ")
    
  
}

process_entries_to_match_cv_events <- function(unified_entries_df){
  
  cv_events_entries <- unified_entries_df |> 
    mutate(
      when = paste0(start, " - ", end),
      order = row_number()
    ) |> 
    mutate(
      across(description_1:description_3,
             ~coalesce(., "EMPTY")
      )
    ) |> 
    rowwise() |> 
    mutate(
      coalesced_description_tasks = list(c(description_1, description_2, description_3))
    ) |> 
    arrange(desc(order)) |>
    select(section, when, title, institution, coalesced_description_tasks) |> 
    rename(
      "what" = title, #role
      "where" = institution, #not location it adds nothing 
      tasks = coalesced_description_tasks
    ) |> 
    ungroup()
  
  return(cv_events_entries)
  
}

fetch_work_entries <- function(cv_events_entries){
  
  work_entries <- cv_events_entries |> 
    filter(section == "industry_positions")
  
  return(work_entries)
  
}

fetch_education_entries <- function(cv_events_entries){
  
  education_entries <- cv_events_entries |> 
    filter(section == "education")
  
  return(education_entries)
  
}

cvevents <- function(tbl, when, what, where, details) {
  
  command_start <- "\\cvevent"
  
  res <- paste0(
    command_start, "{", tbl[[when]], "}", 
    "{", tbl[[what]], "}",
    "{", tbl[[where]], "}")
  
  tbl[[details]] <- sapply(tbl[[details]], function(x) paste0("{", x, "}", collapse = ","))
  res <- paste0(res, "{",tbl[[details]],"}")
  
  cat(res, sep = "\n")
}

fetch_general_title <- function(cv_components){
  
  general_title <- cv_components |> 
    pluck("text") |>
    filter(location == "general title") |>
    pull(text)
  
  
  return(general_title)
}

fetch_summary_intro <- function(cv_components){
  
  introduction_summary_text <- cv_components |> 
    pluck("text") |>
    filter(location == "summary") |>
    pull(text)
  
  return(introduction_summary_text)
  
}