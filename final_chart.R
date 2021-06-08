#
# This is a Shiny web application. You can run the application by clicking
# the 'Run App' button above.
#
# Find out more about building applications with Shiny here:
#
#    http://shiny.rstudio.com/
#

library(shiny)
library(dplyr)
library(ggplot2)

df1 = read.csv('~/R/R project/Datasets/mlb_games_cleaned.csv')

# Server
server <- function(input, output, session) {

    #Reactive
    data <- reactive({
        req(input$sel_cli)
        df <- df1 %>% filter(cli %in% input$sel_cli)
    })
    
    #Render
    output$plot <- renderPlot({
        g <- ggplot(data(), aes(x = runs))
        g + geom_bar(stat = 'count')
        #g + coord_cartesian(xlim = c(0,30))
    })
}

# UI
ui <- fluidPage(
    h1('MLB Analysis: How to Get More Runs'),
    
    sliderInput(inputId = 'sel_cli',
                label = 'Championship Leverage Index',
                #choices = unique(df1$cli),
                min = 0,
                max = 5,
                value = 0,
                step = 1,
            ),
    
    plotOutput('plot')

)



# Run the application 
shinyApp(ui = ui, server = server)
