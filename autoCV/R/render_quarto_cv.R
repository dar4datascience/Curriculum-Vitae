
render_quarto_cv <- function(general_title, introduction_summary_text, formatted_work_entries, formatted_education_entries, contact_info){
  
  # Render the CV
  quarto_render(
    input = "~/Documents/Curriculum-Vitae/autoCV/AutoCV.qmd",
    output_file = "danielamievarodriguez_cv.pdf",
    execute_params = list(
      general_title = general_title,
      introduction = introduction_summary_text,
      formatted_work_entries = formatted_work_entries,
      formatted_education_entries = formatted_education_entries,
      contact_info = contact_info
    )
  )
  
}


format_cv_entries <- function(cv_entries){
    
    #command_start <- "\\cvevent"
    
    role_year_tags <- cv_entries |> 
      glue::glue_data("{[when]}{[what]}{[where]}",
                      .open = "[",
                      .close = "]")
    
    # res <- paste0(
    #     command_start, "{", work_entries[["when"]], "}",
    #     "{", work_entries[["what"]], "}",
    #     "{", work_entries[["where"]], "}")
    
    #print(work_entries |> dplyr::glimpse())
    
    coalesced_tasks <- cv_entries |> 
      #unlist() |> 
      dplyr::pull(tasks) |> 
      purrr::map_chr(~paste0("{", .x, "}", collapse = ","))
    
    # build details into 1
    
    # work_entries[["details2"]] <- sapply(work_entries[["tasks"]], function(x) paste0("{", x, "}", collapse = ","))
    
    #res_final <- paste0(res, "{",work_entries[["details2"]],"}")
    
    formatted_full_work_entries <- paste0("\\cvevent",
                                          role_year_tags,
                                          "{",
                                          coalesced_tasks,
                                          "}")
    
    return(formatted_full_work_entries)

}