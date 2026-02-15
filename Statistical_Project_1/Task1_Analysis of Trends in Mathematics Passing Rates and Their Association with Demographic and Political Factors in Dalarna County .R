# =========================
# STEP 1: Load Libraries
# =========================
# Install only if not already installed
packages <- c("readxl", "dplyr", "ggplot2", "corrplot", "reshape2", "openxlsx")
installed <- rownames(installed.packages())
to_install <- setdiff(packages, installed)
if(length(to_install)) install.packages(to_install)

# Load libraries
library(readxl)
library(dplyr)
library(openxlsx)
library(ggplot2)
library(corrplot)
library(reshape2)

# =========================
# STEP 2: Read Excel Files
# =========================
election <- read_excel("D:/DU-Sem1/Period 2/Statistical Learning/Assignment 1 Folder/Cleaned Excel files/Municipality Election.xlsx")
education <- read_excel("D:/DU-Sem1/Period 2/Statistical Learning/Assignment 1 Folder/Cleaned Excel files/Population Higher education.xlsx")
income <- read_excel("D:/DU-Sem1/Period 2/Statistical Learning/Assignment 1 Folder/Cleaned Excel files/Avg income.xlsx")
results <- read_excel("D:/DU-Sem1/Period 2/Statistical Learning/Assignment 1 Folder/Cleaned Excel files/Results.xlsx")

# =========================
# STEP 3: Clean and Merge Data
# =========================

# Rename columns for clarity
election <- election %>% rename(Year = `Election Year`)
education <- education %>%
  rename(
    EducationLessThan3Y = `post-secondary education, less than 3 years (ISCED97 4+5B)`,
    HigherEducationRaw = `post-secondary education 3 years or more (ISCED97 5A)`
  )

# Calculate percentage of higher education from population
education <- education %>%
  mutate(HigherEducationPercent = (HigherEducationRaw / Population) * 100)

income <- income %>%
  rename(
    AverageIncome = Average_income,
    IncomeInequality = `Income Inequality`,
    MedianIncome = Median_income
  )

results <- results %>%
  rename(PassingRate = Marks) %>%
  filter(Year >= 2015 & Year <= 2024)

# Merge datasets
merged_data <- results %>%
  left_join(education, by = c("Municipality", "Year")) %>%
  left_join(income, by = c("Municipality", "Year")) %>%
  left_join(election, by = c("Municipality", "Year"))

# Select relevant columns
final_data <- merged_data %>%
  select(
    Municipality, Year, Code.x, County, Subject, PassingRate,
    HigherEducationPercent, EducationLessThan3Y, Population,
    AverageIncome, IncomeInequality, MedianIncome,
    `The Moderate Party`, `The Centre Party`, `The Liberal Party`,
    `The Christian Democratic Party`, `The Green Party`,
    `The Social Democratic Party`, `The Left Party`,
    `The Sweden Democrats`, `Other Parties`
  ) %>%
  rename(Code = Code.x)

# Export to Excel
write.xlsx(final_data, "D:/DU-Sem1/Period 2/Statistical Learning/Assignment 1 Folder/Cleaned Excel files/Final_Merged_All_Columns.xlsx")
# =========================
# STEP 4: Reload Cleaned File
# =========================
data <- read_excel("D:/DU-Sem1/Period 2/Statistical Learning/Assignment 1 Folder/Cleaned Excel files/Final_Merged_All_Columns.xlsx")

# Clean and prepare final working dataset
data <- data %>%
  rename(
    SocialDemocrats = `The Social Democratic Party`,
    Moderates = `The Moderate Party`
  ) %>%
  select(Municipality, Year, PassingRate, AverageIncome, HigherEducationPercent, SocialDemocrats, Moderates) %>%
  mutate(Year = as.numeric(Year)) %>%
  arrange(Municipality, Year)

# =========================
# STEP 5: Trend Plot
# =========================

p_municipality <- ggplot(data, aes(x = Year, y = PassingRate, group = Municipality)) +
  geom_line(color = "forestgreen", linewidth = 1.2, na.rm = TRUE) +
  geom_point(color = "black", size = 2) +
  facet_wrap(~ Municipality, scales = "free_y") +
  scale_x_continuous(breaks = seq(2015, 2024, by = 1)) +
  scale_y_continuous(breaks = seq(50, 100, by = 5)) +
  labs(title = "Math Passing Rate Trends by Municipality (2015–2024)",
       x = "Year", y = "Passing Rate (%)") +
  theme_minimal(base_size = 13) +
  theme(strip.text = element_text(face = "bold"),
        axis.text.x = element_text(angle = 45, hjust = 1),
        plot.title = element_text(hjust = 0.5, face = "bold"),
        plot.background = element_rect(color = "black", fill = NA, linewidth = 1)
        )
ggsave("D:/DU-Sem1/Period 2/Statistical Learning/Assignment 1 Folder/Cleaned Excel files/Plot_Municipality_Trends.png",
       plot = p_municipality, width = 12, height = 8, bg = "white")
print(p_municipality)


# =========================
# STEP 5B: Overall Average Trend Plot (Dalarna County)
# =========================

# Load if not already loaded
library(scales)

# Compute average PassingRate per year
avg_trend <- data %>%
  group_by(Year) %>%
  summarise(AvgPassingRate = mean(PassingRate, na.rm = TRUE)) %>%
  mutate(AvgPassingRate = round(AvgPassingRate))  # Optional: round values

# Plot overall average trend with rounded y-axis labels
p_overall <- ggplot(avg_trend, aes(x = Year, y = AvgPassingRate)) +
  geom_line(color = "forestgreen", size = 1.2) +
  geom_point(color = "darkgreen", size = 2) +
  geom_smooth(method = "lm", se = TRUE, color = "black", linetype = "dashed") +
  scale_x_continuous(breaks = 2015:2024) +  # <- Fix x-axis to show full years
  scale_y_continuous(breaks = seq(80, 100, by = 1)) +
  labs(
    title = "Overall Math Passing Rate Trend in Dalarna County (2015–2024)",
    x = "Year",
    y = "Average Passing Rate (%)"
  ) +
  theme_minimal(base_size = 14) +
  theme(
    plot.title = element_text(hjust = 0.5, face = "bold"),
    plot.background = element_rect(color = "black", fill = NA, linewidth = 1)
  )

# Save & display
ggsave("D:/DU-Sem1/Period 2/Statistical Learning/Assignment 1 Folder/Cleaned Excel files/Plot_Overall_Trend.png",
       plot = p_overall, width = 10, height = 6, bg = "white")
print(p_overall)
# =========================
# STEP 6: Regression Models
# =========================
model <- lm(PassingRate ~ Year, data = data)
summary(model)

model2 <- lm(PassingRate ~ Year + HigherEducationPercent + AverageIncome + SocialDemocrats + Moderates, data = data)
summary(model2)

# =========================
# STEP 7: Correlation Matrix
# =========================
cor_data <- data %>%
  select(PassingRate, HigherEducationPercent, AverageIncome, SocialDemocrats, Moderates)

cor_matrix <- cor(cor_data, use = "complete.obs")
corrplot(cor_matrix, method = "circle")

#..........................Passing Rate vs Higher Education Percent
# Example 1: Passing Rate vs Higher Education %
# Plot 1: Passing Rate vs Higher Education %
p1 <- ggplot(data, aes(x = HigherEducationPercent, y = PassingRate)) +
  geom_point(aes(color = Municipality), size = 2) +
  geom_smooth(method = "lm", color = "darkgreen") +
  labs(title = "Math Passing Rate vs Higher Education (%)",
       x = "Higher Education (%)", y = "Passing Rate (%)") +
  theme_minimal(base_size = 14) +
  theme(
    plot.title = element_text(hjust = 0.5, face = "bold"),
    plot.background = element_rect(color = "black", fill = NA, linewidth = 1)
  )

ggsave("D:/DU-Sem1/Period 2/Statistical Learning/Assignment 1 Folder/Cleaned Excel files/Plot1_HigherEducation.png", plot = p1, width = 8, height = 6, bg = "white")
print(p1)

#..............Passing Rate vs Average Income
p2 <- ggplot(data, aes(x = AverageIncome, y = PassingRate)) +
  geom_point(aes(color = Municipality), size = 2) +
  geom_smooth(method = "lm", se = TRUE, color = "blue") +
  labs(title = "Math Passing Rate vs Average Income",
       x = "Average Income (SEK)", y = "Passing Rate (%)") +
  theme_minimal(base_size = 14) +
  theme(
    plot.title = element_text(hjust = 0.5, face = "bold"),
    plot.background = element_rect(color = "black", fill = NA, linewidth = 1)
  )

ggsave("D:/DU-Sem1/Period 2/Statistical Learning/Assignment 1 Folder/Cleaned Excel files/Plot2_AverageIncome.png", plot = p2, width = 8, height = 6, bg = "white")
print(p2)

#............... Passing Rate vs Social Democrats Vote Share
p3 <- ggplot(data, aes(x = SocialDemocrats, y = PassingRate)) +
  geom_point(aes(color = Municipality), size = 2) +
  geom_smooth(method = "lm", se = TRUE, color = "red") +
  labs(title = "Math Passing Rate vs Social Democrats Vote Share",
       x = "Social Democrats (%)", y = "Passing Rate (%)") +
  theme_minimal(base_size = 14) +
  theme(
    plot.title = element_text(hjust = 0.5, face = "bold"),
    plot.background = element_rect(color = "black", fill = NA, linewidth = 1)
  )

ggsave("D:/DU-Sem1/Period 2/Statistical Learning/Assignment 1 Folder/Cleaned Excel files/Plot3_SocialDemocrats.png", plot = p3, width = 8, height = 6, bg = "white")
print(p3)

#................... Passing Rate vs Moderates Vote Share
p4 <- ggplot(data, aes(x = Moderates, y = PassingRate)) +
  geom_point(aes(color = Municipality), size = 2) +
  geom_smooth(method = "lm", color = "blue", se = TRUE) +
  labs(title = "Math Passing Rate vs Moderates Vote Share",
       x = "Moderates (%)", y = "Passing Rate (%)") +
  theme_minimal(base_size = 14) +
  theme(
    plot.title = element_text(hjust = 0.5, face = "bold"),
    plot.background = element_rect(color = "black", fill = NA, linewidth = 1)
  )

ggsave("D:/DU-Sem1/Period 2/Statistical Learning/Assignment 1 Folder/Cleaned Excel files/Plot4_Moderates.png",
       plot = p4, width = 8, height = 6, bg = "white")
print(p4)

