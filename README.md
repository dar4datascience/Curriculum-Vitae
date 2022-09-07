# CV

Repository for automating CV generation on-demand.

You can see the lastest version of my CV @[this github pages link](https://dar4datascience.github.io/Curriculum-Vitae/)

## Objective

Simplify the CV generation process by linking a live Google Sheets with the complete information into a process that curates the data and publishes that information into handy formats.

## Workflow


```mermaid
  graph LR;
      explanation>Using R to Automate your CV]
      A[Detailed Life Experiences]-->B[Google Sheets];
      B-->C[GoogleSheets4 R];
      C-->D[Render CV using Vitae package];
      D-->E[Customize CV with datadrivencv]
      E-->F[Automate and deploy a website with downloadable PDF];
```

## Assets

 - CV in pdf
 - CV as an html
 - R Scripts
 - css file
 - README

## References

 - [Data driven CVs](https://github.com/nstrayer/datadrivencv)
 - [Vitae Package](https://pkg.mitchelloharawild.com/vitae/)
 - [Tutorial of the Vitae Packge](https://www.youtube.com/watch?v=cMlRAiQUdD8&t=1929s)
 - [R Ladies Meetup about the datadrivencv package](https://www.youtube.com/watch?v=Fc1RwRskk08&t=3467s)
