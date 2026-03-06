R-Bootcamp Group Assignment
Group 1: Duojie Jiahua, Maxim Aminov
HSLU, January 2026

=== PROJECT OVERVIEW ===
Title:    Coffee Shop Sales and Weather Analysis
Analysis: How weather conditions (temperature, precipitation) affect sales
          at Maven Roasters, a three-location NYC coffee shop chain.

=== FOLDER STRUCTURE ===
1_Duojie_Aminov/
├── readme.txt                          <- This file
├── Scripts/
│   └── 1_Duojie_Aminov.Rmd            <- Main R Markdown source file
├── Output/
│   └── 1_Duojie_Aminov.html           <- Rendered HTML report
└── Data/
    ├── Coffee Shop Sales.xlsx          <- Sales dataset (Maven Analytics)
    └── New York City,USA 2023-01-01    <- Weather dataset (Visual Crossing)
        to 2023-12-31.csv

=== HOW TO REPRODUCE ===
1. Open RStudio and set the working directory to Scripts/
   (Session → Set Working Directory → Choose Directory → select Scripts/)
   OR open 1_Duojie_Aminov.Rmd directly in RStudio.
2. Click "Knit" to render the HTML report.
   Output will appear in the Scripts/ folder (rename/move to Output/ if needed).

NOTE: Data paths in the Rmd are relative: "../Data/..."
      The Rmd must be run from the Scripts/ folder for paths to resolve correctly.

=== REQUIRED R PACKAGES ===
tidyverse, readxl, lubridate, janitor, leaflet, knitr, kableExtra, hms, scales, purrr

Install all at once:
  install.packages(c("tidyverse", "readxl", "lubridate", "janitor",
                     "leaflet", "knitr", "kableExtra", "hms", "scales"))

=== DATA SOURCES ===
Sales:   Maven Analytics Data Playground
         https://www.mavenanalytics.io/data-playground
Weather: Visual Crossing Weather API
         https://www.visualcrossing.com

=== NOTES ===
- Weather data covers full year 2023; only Jan–Jun 2023 is used in the analysis.
- HTML uses code_folding=hide; click "Show" buttons to reveal R code chunks.
- The join of the two datasets is highlighted in the "Merging Datasets" section.
