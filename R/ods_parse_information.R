read_cv_ods <- function(cv_type_file_path, sheet_number, ...) {
  read_ods(cv_type_file_path, sheet = sheet_number, ...) |> 
    janitor::clean_names()
} 

build_cv_components <- function(cv_type_file_path) {
  list(
    entries = read_cv_ods(cv_type_file_path, 1, skip = 1),
    skills = read_cv_ods(cv_type_file_path, 2, skip = 1),
    text = read_cv_ods(cv_type_file_path, 3, skip = 1),
    contact = read_cv_ods(cv_type_file_path, 4, skip = 1)
  )
}

fetch_cv_entries <- function(cv_data) {
  cv_data |> 
    pluck("entries") |>
    filter(in_resume == 1) |>
    mutate(
      entry_type = case_when(
        section == "industry_positions" ~ "work",
        section == "education" ~ "education",
        .default = NA_character_
      )
    )
}

fetch_skills <- function(cv_data) {
  cv_data |> 
    pluck("skills") |> 
    pull(skill) |> 
    paste(collapse = ", ")
}

process_entries_to_match_cv_events <- function(unified_entries_df) {
  unified_entries_df |> 
    mutate(
      when = paste0(start, " - ", end),
      order = row_number(),
      across(description_1:description_3, ~coalesce(., "EMPTY"))
    ) |> 
    rowwise() |> 
    mutate(
      tasks = list(c(description_1, description_2, description_3))
    ) |> 
    ungroup() |>
    arrange(desc(order)) |>
    select(section, when, what = title, where = institution, tasks)
}

fetch_work_entries <- function(cv_events_entries) {
  cv_events_entries |> 
    filter(section == "industry_positions")
}

fetch_education_entries <- function(cv_events_entries) {
  cv_events_entries |> 
    filter(section == "education")
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

fetch_general_title <- function(cv_components) {
  cv_components |> 
    pluck("text") |>
    filter(location == "general title") |>
    pull(text)
}

fetch_summary_intro <- function(cv_components) {
  cv_components |> 
    pluck("text") |>
    filter(location == "summary") |>
    pull(text)
}