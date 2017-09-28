library(dplyr)
j <- jsonlite::fromJSON("data/capitals.json")
names(j) %>% 
  purrr::map(.f = function(x) {
    list(cityName = x)
  }) -> jj

j %>% 
  purrr::map2(.y = jj, .f = function(x, y) {
    x <- unname(x)
    y[["coords"]] <- list(x = x[1], y = x[2])
    y
  }) %>% 
  unname() -> jj


jsonlite::toJSON(jj, auto_unbox = T) %>% 
  writeLines("data/cap.json")
