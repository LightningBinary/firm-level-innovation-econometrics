library(dplyr)
library(plm)
library(stargazer)
library(psych)

rm(list = ls())
df <- read.table("D:/AAA/UPennHW/STAT5210/Project/resources/data.mc", header = FALSE);
colnames(df) <- c("firm_id", "sector", "region", 
                  paste0("patents_", 1983:1991),
                  paste0("log_RD_", 1983:1991),
                  paste0("log_spillover_", 1983:1991))

# See Descriptive statistics
desc_stats <- describe(df)
print(desc_stats)
stargazer(df, type = "text", title = "Descriptive Statistics", digits = 2, 
          summary.stat = c("mean", "sd", "min", "median", "max"))


long_df <- reshape(df,
                   varying = list(
                     patents = paste0("patents_", 1983:1991),
                     log_RD = paste0("log_RD_", 1983:1991),
                     log_spillover = paste0("log_spillover_", 1983:1991)
                   ),
                   v.names = c("patents", "log_RD", "log_spillover"),
                   timevar = "year",
                   times = 1983:1991,
                   direction = "long",
                   idvar = "firm_id")


pdata <- pdata.frame(long_df, index = c("firm_id", "year"))

model_within <- plm(patents ~ log_RD + log_spillover, 
                    data = pdata, 
                    model = "within")

summary(model_within)

#Hausman test (random effects vs fixed effects) 
#To compare whether the estimates of randome effects models and fixed effects models are significantly different. 
model_random <- plm(patents ~ log_RD + log_spillover, data = pdata, model = "random")
phtest(model_within, model_random)

summary(model_random)

# 2SLS
pdata$lag_log_RD <- ave(pdata$log_RD, pdata$firm_id, FUN = function(x) c(NA, x[-length(x)]))
pdata$lag_log_spill <- ave(pdata$log_spillover, pdata$firm_id, FUN = function(x) c(NA, x[-length(x)]))

pdata_iv <- na.omit(pdata)

# IV regression
model_iv <- plm(patents ~ log_RD + log_spillover | lag_log_RD + lag_log_spill + log_spillover, 
                data = pdata_iv, 
                model = "within")

summary(model_iv)



#Hausman test (instrumental variables vs fixed effects) 
#To compare whether the estimates of IV models and non-IV models are significantly different. 
phtest(model_within, model_iv)

# Pooled OLS 
pool_ols <- plm(patents ~ log_RD + log_spillover,
                data = pdata_iv,
                index = c("firm_id", "year"),
                model = "pooling")

summary(pool_ols)

# create a table for comparison
stargazer(pool_ols, model_within, model_random, model_iv,
          type = "text",
          title = "Comparison of Panel Data Models",
          column.labels = c("Pooled OLS", "Fixed Effects", "Random Effects", "2SLS-IV"),
          dep.var.labels = "Patents",
          keep.stat = c("n", "rsq", "adj.rsq", "f"),
          no.space = TRUE)


summary(pool_ols)
summary(model_random)
summary(model_within)
summary(model_iv)

