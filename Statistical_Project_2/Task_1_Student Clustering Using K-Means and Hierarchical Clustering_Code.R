# Install all missing packages
install.packages("factoextra")     # For elbow & silhouette plots
install.packages("dendextend")     # For enhanced dendrograms
install.packages("NbClust")        # To calculate the best number of clusters
install.packages("cluster")        # Just in case it's also not installed
install.packages("tidyverse")      # In case tidyverse wasn’t installed properly


# Load necessary libraries

library(tidyverse)      # For data wrangling
library(cluster)        # For silhouette analysis
library(factoextra)     # For clustering visualization
library(dendextend)     # For dendrogram enhancements
library(NbClust)        # For optimal clusters
library(caret)          # For dummy variables

library(ggplot2)

# Read the dataset 
data <- read.csv("C:/Users/Lenovo/Desktop/Statistical Learning/SL 2nd Assignmnet/student_performance_large_dataset_new (1).csv")

# View structure
str(data)

# Step 1: Remove extra columns (correcting the name "X" instead of "Unnamed..0")
data_clean <- data %>%
  select(-c(X, Student_ID, Final_Grade))  # use "X" not "Unnamed..0"

# Step 2a: Convert character columns to factors
data_clean$Gender <- as.factor(data_clean$Gender)
data_clean$Preferred_Learning_Style <- as.factor(data_clean$Preferred_Learning_Style)
data_clean$Participation_in_Discussions <- as.factor(data_clean$Participation_in_Discussions)
data_clean$Use_of_Educational_Tech <- as.factor(data_clean$Use_of_Educational_Tech)
data_clean$Self_Reported_Stress_Level <- as.factor(data_clean$Self_Reported_Stress_Level)

# Step 2b: Create dummy variables
dummies <- dummyVars(" ~ .", data = data_clean)
data_ready <- predict(dummies, newdata = data_clean)
data_ready <- as.data.frame(data_ready)

# Step 2c: Scale the data
data_scaled <- scale(data_ready)

# Optional: View preview
head(data_scaled)


# STEP 3: Find the Optimal Number of Clusters (k)

# Elbow Method — Total Within-Cluster Sum of Squares (WSS)
elbow_plot <- fviz_nbclust(data_scaled, kmeans, method = "wss") +
  labs(title = "Elbow Method for Optimal k") +
  theme(
    plot.title = element_text(hjust = 0.5, face = "bold", size = 14)
  )

print(elbow_plot)

# Save Elbow plot to Desktop
ggsave("C:/Users/Lenovo/Desktop/elbow_plot.png", 
       plot = elbow_plot, 
       width = 8, height = 6)


# Silhouette Method — Mean Silhouette Width for different k
silhouette_plot <- fviz_nbclust(data_scaled, kmeans, method = "silhouette") +
  labs(title = "Silhouette Method for Optimal k") +
  theme(
    plot.title = element_text(hjust = 0.5, face = "bold", size = 14)
    
  )
print(silhouette_plot)

# Save Silhouette plot to Desktop
ggsave("C:/Users/Lenovo/Desktop/silhouette_plot.png", 
       plot = silhouette_plot, 
       width = 8, height = 6)


# STEP 4: Apply K-means Clustering (k = 2 and k = 3)

# Set seed for reproducibility
set.seed(123)

# Run K-means with k = 2
km2 <- kmeans(data_scaled, centers = 2, nstart = 25)

# Run K-means with k = 3
km3 <- kmeans(data_scaled, centers = 3, nstart = 25)

# Cluster Profiling – Summarize average feature values per cluster

# Combine the scaled dataset with k = 2 cluster assignments

# Combine scaled data with cluster assignments as a data frame (not a matrix)
clustered_data <- as.data.frame(data_scaled)
clustered_data$Cluster_K2 <- km2$cluster

# Calculate the average of each variable within each cluster
cluster_profile <- aggregate(clustered_data[, 1:(ncol(clustered_data)-1)], 
                             by = list(Cluster = clustered_data$Cluster_K2), 
                             FUN = mean)

# Round the output for readability
round(cluster_profile, 2)

# Create plot with centered title and border
km2_plot <- fviz_cluster(km2, data = data_scaled,
                         geom = "point",
                         ellipse.type = "convex",
                         palette = "jco",
                         ggtheme = theme_minimal(),
                         main = "K-means Clustering with k = 2") +
  theme(
    plot.title = element_text(hjust = 0.5, face = "bold", size = 14),  # Center title
    panel.border = element_rect(color = "black", fill = NA, size = 1) # Add border
  )

# Print the plot
print(km2_plot)

# Save the plot with border and centered title
ggsave("C:/Users/Lenovo/Desktop/KMeans_k2.png",
       plot = km2_plot,
       width = 10, height = 6,
       bg = "white")

# Visualize k = 3 clustering
# Create and save K-means (k = 3) cluster plot
km3_plot <- fviz_cluster(km3, data = data_scaled,
                         geom = "point",
                         ellipse.type = "convex",
                         palette = "jco",
                         ggtheme = theme_minimal(),
                         main = "K-means Clustering with k = 3")
print (km3_plot)
ggsave("C:/Users/Lenovo/Desktop/KMeans_k3.png",
       plot = km3_plot,
       width = 10, height = 6,
       bg = "white")

# STEP 5: Evaluate Clusters by Comparing with Final Grades

# Step 5a: Reload original dataset with Final_Grade
data_with_grade <- read.csv("C:/Users/Lenovo/Desktop/Statistical Learning/SL 2nd Assignmnet/student_performance_large_dataset_new (1).csv")

# Step 5b: Add the k = 2 cluster assignments
data_with_grade$Cluster_K2 <- km2$cluster

# Step 5c: View how Final_Grades are distributed across the two clusters
table(data_with_grade$Cluster_K2, data_with_grade$Final_Grade)

# Calculate percentages in R
# Calculate % distribution within each cluster
grade_table <- table(data_with_grade$Cluster_K2, data_with_grade$Final_Grade)

# Convert to proportions by row
grade_percent <- prop.table(grade_table, margin = 1) * 100

# Round and print nicely
round(grade_percent, 1)

# Save the final dataset with cluster labels for report use
write.csv(data_with_grade,
          "C:/Users/Lenovo/Desktop/student_clusters_k2.csv",
          row.names = FALSE)
# STEP 6: Hierarchical Clustering and Comparison with K-means
# Step 6a: Compute distance matrix (Euclidean distance)
dist_matrix <- dist(data_scaled, method = "euclidean")

# Step 6b: Perform hierarchical clustering using Ward's method
hc_model <- hclust(dist_matrix, method = "ward.D2")
plot(hc_model, labels = FALSE, hang = -1,
     main = "Full Dendrogram of Hierarchical Clustering (k = 2)",
     ylab = "Height")

# Step 6c: Plot dendrogram ( try plotting only first 100 students if it's too big)
# Save dendrogram manually
png("C:/Users/Lenovo/Desktop/Hierarchical_Dendrogram.png", width = 1000, height = 600)
plot(hc_model, labels = FALSE, hang = -1,
     main = "Dendrogram of Hierarchical Clustering", ylab = "Height")
dev.off()


# Step 6c.2: Clean Dendrogram for First 100 Students (with colored branches)
# Load necessary library
# Load dendextend library
# Load necessary library
library(dendextend)

# Subset first 100 rows
small_data <- data_scaled[1:100, ]

# Create distance matrix and clustering
small_dist <- dist(small_data, method = "euclidean")
small_hc <- hclust(small_dist, method = "ward.D2")

# Convert to dendrogram and color branches
dend <- as.dendrogram(small_hc)
dend_colored <- color_branches(dend, k = 4)

# move all leaf labels to avoid clutter
labels(dend_colored) <- rep("", length(labels(dend_colored)))

# Save clean plot (no X labels, only Y-axis shown)
png("C:/Users/Lenovo/Desktop/Dendrogram_First_100_Clean.png", width = 1000, height = 600)
par(mar = c(5, 5, 4, 2))  # Set margins
plot(dend_colored,
     main = "Dendrogram of First 100 Students",
     ylab = "Height")
box()
dev.off()



# Step 6d: Cut the tree into 2 clusters
hc_clusters <- cutree(hc_model, k = 2)

# Step 6e: Add hierarchical clusters to original dataset
data_with_grade$Cluster_HC2 <- hc_clusters

# Step 6f: Compare with Final Grade like we did for k-means
table(data_with_grade$Cluster_HC2, data_with_grade$Final_Grade)

# Show % for Hierarchical Clusters
# Show grade distribution by hierarchical clusters
table(data_with_grade$Cluster_HC2, data_with_grade$Final_Grade)

# Convert to percentages
grade_table_hc <- table(data_with_grade$Cluster_HC2, data_with_grade$Final_Grade)
grade_percent_hc <- prop.table(grade_table_hc, margin = 1) * 100
round(grade_percent_hc, 1)

# Plot: Final Grade distribution by Hierarchical Clustering (k = 2)
# Create the plot with theme_minimal
hc_plot <- ggplot(data_with_grade, aes(x = Final_Grade, fill = as.factor(Cluster_HC2))) +
  geom_bar(position = "dodge") +
  labs(title = "Grade Distribution by Hierarchical Cluster (k=2)",
       x = "Final Grade",
       y = "Number of Students",
       fill = "Cluster (HC)") +
  theme_minimal()
print (hc_plot)
# Save with white background
ggsave("C:/Users/Lenovo/Desktop/HC2_Grade_Distribution.png", 
       plot = hc_plot,
       width = 10, height = 5,
       bg = "white")


# Comparison Summary
# Both clustering methods (K-means and Hierarchical) suggested k = 2 as optimal.
# Grade distributions were very similar across clusters in both methods.
# This suggests that while behavioral patterns can separate students,
# final grades are only weakly aligned.
# K-means is more efficient for large datasets, while Hierarchical gave more 
# visual insight via dendrogram.



# ==========================
# RADAR CHART OF CLUSTER TRAITS
# ==========================

# Install and load required package
install.packages("fmsb")     # Only needed once
# Adjusted radar chart code with better scaling and appearance
# ==========================
# RADAR CHART – FINAL POLISHED VERSION
# ==========================

# Install packages only if not already installed
if (!require(fmsb)) install.packages("fmsb")
if (!require(scales)) install.packages("scales")

# Load libraries
library(fmsb)
library(scales)

# Prepare trait data
radar_data <- data.frame(
  Participation = c(1.22, -0.82),
  EdTech_Use = c(0.02, -0.01),
  Stress_Low = c(-0.01, 0.01),
  Kinesthetic = c(-0.02, 0.02),
  Online_Courses = c(0.01, -0.01),
  Study_Hours = c(-0.01, 0.01),
  Social_Media = c(0, 0)
)
rownames(radar_data) <- c("Cluster 1", "Cluster 2")

# Set shorter, clearer axis labels with line breaks
colnames(radar_data) <- c("Participation", "EdTech\nUse", "Stress\nLow", 
                          "Kinesthetic\nLearner", "Online\nCourses", 
                          "Study\nHours", "Social\nMedia")

# Add max and min rows (required for radar)
radar_data <- rbind(
  rep(1.3, ncol(radar_data)),   # Max
  rep(-0.1, ncol(radar_data)),  # Min
  radar_data
)

# Set up colors
colors_border <- c("red", "blue")
colors_fill <- c(alpha("red", 0.2), alpha("blue", 0.2))

# Open plotting window and save PNG
png("C:/Users/Lenovo/Desktop/radar_clusters_final.png", width = 900, height = 600)

# Plot with white background and border
par(mar = c(2, 2, 4, 2), bg = "white")  # Margin + white background
radarchart(radar_data,
           axistype = 1,
           pcol = colors_border,
           pfcol = colors_fill,
           plwd = 3,
           plty = 1,
           cglcol = "darkgray",
           cglty = 1,
           cglwd = 1,
           axislabcol = "black",
           caxislabels = seq(-0.1, 1.3, 0.3),
           vlcex = 1.0,
           title = "Radar Chart: Behavioral Comparison of Clusters")

# Add black border around plot
box(lwd = 2)

# Add legend
legend("topright", legend = c("Cluster 1", "Cluster 2"),
       bty = "n", pch = 20,
       col = colors_border,
       text.col = "black", cex = 1.2)

# Save and close device
dev.off()

# Also show in RStudio Plot Viewer
par(mar = c(2, 2, 4, 2), bg = "white")  # Reset par
radarchart(radar_data,
           axistype = 1,
           pcol = colors_border,
           pfcol = colors_fill,
           plwd = 3,
           plty = 1,
           cglcol = "darkgray",
           cglty = 1,
           cglwd = 1,
           axislabcol = "black",
           caxislabels = seq(-0.1, 1.3, 0.3),
           vlcex = 1.0,
           title = "Radar Chart: Behavioral Comparison of Clusters")
box(lwd = 2)
legend("topright", legend = c("Cluster 1", "Cluster 2"),
       bty = "n", pch = 20,
       col = colors_border,
       text.col = "black", cex = 1.2)

