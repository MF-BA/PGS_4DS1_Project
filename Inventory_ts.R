library(tseries)
library(forecast)
library("strucchange")

product_gasoil_grouped.df<-read.table(file=file.choose(),header=TRUE,sep=",",dec=".")
str(product_gasoil_grouped.df)

# Convert GROSS_QUANTITY to numeric
product_gasoil_grouped.df$GROSS_QUANTITY <- as.numeric(product_gasoil_grouped.df$GROSS_QUANTITY)

# Convert X to Date format
product_gasoil_grouped.df$X <- as.Date(product_gasoil_grouped.df$X)

# Specify the start date directly
start_date <- min(product_gasoil_grouped.df$X)

# Create time series
product_gasoil_grouped.ts <- ts(product_gasoil_grouped.df$GROSS_QUANTITY, start = start_date, frequency = 365)

# Plot time series
plot(product_gasoil_grouped.ts)




boxplot(product_gasoil_grouped.ts, main = "Boxplot of GROSS_QUANTITY", ylab = "GROSS_QUANTITY")
# Calculate boxplot statistics
#bp <- boxplot.stats(product_gasoil_grouped.ts)
# Define the range for outliers
#lower_bound <- bp$stats[2] - 1.5 * IQR(product_gasoil_grouped.ts)
#upper_bound <- bp$stats[4] + 1.5 * IQR(product_gasoil_grouped.ts)
# Remove outliers
#cleaned_data <- product_gasoil_grouped.ts[product_gasoil_grouped.ts >= lower_bound & product_gasoil_grouped.ts <= upper_bound]
#re dipslay the plot
#cleaned_data.ts <- ts(cleaned_data, start = c(start_date), frequency = 12)
#plot(cleaned_data.ts)



time<- c(1:length(product_gasoil_grouped.ts))
lm_model <- lm(product_gasoil_grouped.ts ~ time + seasonaldummy(product_gasoil_grouped.ts))
summary(lm_model)

plot(product_gasoil_grouped.ts)
points(time(product_gasoil_grouped.ts),fitted(lm_model),col="blue",type="l")
acf(lm_model$residuals)
Box.test(lm_model$residuals) 

forecast_values <- forecast(lm_model$fitted.values, h =50)
forecast_values$fitted
# Create time series
product_gasoil_grouped.ts <- ts(forecast_values$fitted, start = start_date, frequency = 365)

# Plot time series
plot(product_gasoil_grouped.ts)
