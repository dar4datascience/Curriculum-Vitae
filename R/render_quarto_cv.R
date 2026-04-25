render_quarto_cv <- function(general_title, introduction_summary_text, 
                             formatted_work_entries, formatted_education_entries, 
                             skillz, contact_info) {
  quarto_render(
    input = "AutoCV.qmd",
    output_file = "danielamievarodriguez_cv.pdf",
    execute_params = list(
      general_title = general_title,
      introduction = introduction_summary_text,
      formatted_work_entries = formatted_work_entries,
      formatted_education_entries = formatted_education_entries,
      skills = skillz,
      contact_info = contact_info
    )
  )
}

format_cv_entries <- function(cv_entries) {
  role_year_tags <- cv_entries |> 
    glue::glue_data("{[when]}{[what]}{[where]}",
                    .open = "[",
                    .close = "]")
  
  coalesced_tasks <- cv_entries |> 
    pull(tasks) |> 
    map(~ .x[!grepl("EMPTY", .x, ignore.case = FALSE)]) |> 
    map_chr(~ paste0("{", .x, "}", collapse = ","))
  
  paste0("\\cvevent", role_year_tags, "{", coalesced_tasks, "}")
}