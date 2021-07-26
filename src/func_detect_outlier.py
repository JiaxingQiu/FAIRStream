#pip install rpy2
import rpy2.robjects as robjects

robjects.r('''
    if (!require(lazyeval))  install.packages("lazyeval")
    library(dplyr)
    library(car)
    library(ggplot2)

    viz_outlier <- function(x, y, data, keys){
        # subset data by input columns
        data <- dplyr::distinct(data[,c(keys,x,y)])

        # ---- univariable outlier detection for each feature ----
        p_uni_x <- plot_outlier_uni(x, data)
        p_uni_y <- plot_outlier_uni(y, data)

        # ---- bivariable outlier detection ----
        p_bi <- plot_outlier_bi(x, y, data)

        plot_object <- ggarrange(p_uni_x,p_uni_y,
                                nrow = 1, ncol = 2)

        plot_object <- ggarrange(plot_object, p_bi,
                                nrow=2, ncol=1,
                                heights = c(1,5))

        return(plot_object)

    }

    # plot outlier from univariable boxplot
    plot_outlier_uni <- function(fea, data, keys){

        #data <- dplyr::distinct(data[,c(keys,fea)])

        # function to detect outliers logically 
        is_outlier <- function(x) {
        return(x<quantile(x,0.25,na.rm=TRUE)-1.5*IQR(x,na.rm=TRUE)|x>quantile(x,0.75,na.rm=TRUE)+1.5*IQR(x,na.rm=TRUE))
        }
        # add outlier subject number to a new column
        data <- data %>% mutate(outlier = ifelse(is_outlier(data[,fea]), data[,keys], as.numeric(NA)))
        outlier_lst <- unique(data$outlier[!is.na(data$outlier)])

        plot_object <- ggplot(data, aes(x=data[,fea])) +
            geom_boxplot() +
            geom_text(aes(y=0.2,label = outlier), na.rm = TRUE, size=2) +
            xlab(fea)+
            ggtitle(
                paste( 
                paste0("*#subjects: ", n_distinct(data[!is.na(data[,fea]),keys]), "    #points: ", nrow(data[!is.na(data[,fea]),]), "*<br>"),
                paste0("only list 10 outlier(s): ", paste(outlier_lst[1:min(10,length(outlier_lst))], collapse = " "))
                )
            ) +
            theme(axis.title.y=element_blank(),
                    axis.text.y=element_blank(),
                    axis.ticks.y=element_blank(),
                    plot.title=ggtext::element_textbox_simple())
        return(plot_object)

    }

    plot_outlier_bi <- function(x, y, data, keys){
        # keep complete rows for bi-variable viz and summary stats
        data <- na.omit(data)
        # find the center point
        data.center = colMeans(data[,c(x,y)])
        # find the covariance matrix
        data.cov <- cov(data[,c(x,y)])
        # Ellipse radius from Chi-Sqaure distribution
        rad  = sqrt(qchisq(p = 0.95 , df = ncol(data[,c(x,y)])))
        # Finding ellipse coordiantes
        ellipse <- car::ellipse(center = data.center, shape = data.cov, radius = rad,
                                segments = 150 , draw = FALSE)

        # scatter plot with ellipse coordinates
        ellipse <- as.data.frame(ellipse)
        colnames(ellipse) <- colnames(data[,c(x,y)])

        # Finding distances
        distances <- mahalanobis(x = data[,c(x,y)] , center = data.center , cov = data.cov)
        # Cutoff value for ditances from Chi-Sqaure Dist
        cutoff <- qchisq(p = 0.95 , df = ncol(data[,c(x,y)]))
        # Display observation whose distance greater than cutoff value
        data <- data %>% mutate(outlier = ifelse(distances>cutoff, data[,keys], as.numeric(NA)))
        outlier_lst <- unique(data$outlier[!is.na(data$outlier)])

        # scattor plot with 
        plot_object <- ggplot(data, aes(x=data[,x], y=data[,y])) +
            geom_point(size=2, alpha=0.7) +
            geom_polygon(data=ellipse, aes(ellipse[,x],ellipse[,y]), fill = "orange", color = "orange", alpha = 0.3)+
            geom_point(aes(data.center[1], data.center[2]), size = 3, color = "blue") +
            geom_text(aes(label = outlier), hjust = 1, vjust = -1.5, size = 2) +
            xlab(x)+
            ylab(y)+
            ggtitle(
                paste( 
                paste0("#subjects: ", n_distinct(data[,keys]), "    #points: ", nrow(data)),
                paste0("only list 10 outlier(s): ", paste(outlier_lst[1:min(10,length(outlier_lst))], collapse = " ")),
                sep="\n"
                )
            )
        return(plot_object)
    }


''')

viz_outlier = robjects.globalenv['viz_outlier']
plot_outlier_uni = robjects.globalenv['plot_outlier_uni']
plot_outlier_bi = robjects.globalenv['plot_outlier_bi']
