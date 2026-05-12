generate_carousel <- function(json_path = "data/carousel_icons.json") {
  icons <- jsonlite::read_json(json_path)$icons
  
  icon_html <- function(name) {
    alt_text <- tools::toTitleCase(gsub("apache|github", "", name))
    sprintf(
      '    <div class="carousel-item"><img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/%s/%s-original.svg" alt="%s"></div>',
      name, name, alt_text
    )
  }
  
  single_set <- paste(sapply(icons, icon_html), collapse = "\n")
  
  all_sets <- paste(
    single_set,
    "    <!-- Duplicate for seamless loop -->",
    single_set,
    "    <!-- Third set for bulletproof loop -->",
    single_set,
    sep = "\n"
  )
  
  sprintf(
    '<div class="tech-carousel">\n  <div class="carousel-track">\n%s\n  </div>\n</div>',
    all_sets
  )
}
