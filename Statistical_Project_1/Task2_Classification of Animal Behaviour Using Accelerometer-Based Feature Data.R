# Question NO. 2
# Animal Behavior Classification Using Accelerometer Data
# -----------------------------
# Research Questions:
# 1. Can animal behavior be accurately classified using accelerometer-derived features from a 5-second interval window?
# 2. How do Logistic Regression, k-Nearest Neighbors, Naive Bayes, and Neural Networks compare in classification accuracy?

#First of all, i am Loading Required Libraries
install.packages(c("caTools", "caret", "nnet", "e1071", "class", "ggplot2", "pROC", "reshape2"))
library(caTools)
library(caret)
library(nnet)
library(e1071)
library(class)
library(ggplot2)
library(pROC)
library(reshape2)

# Step 1: Load and Clean Data

# Load original dataset and keep it safe
raw_data <- read.csv("D:/DU-Sem1/Period 2/Statistical Learning/Assignment 1 Folder/Task 2/df4_5s 9 5 2025.csv")

# work on a copy of the data
data <- raw_data

# Remove rows with missing labels
data$Modifiers[data$Modifiers == "Missing data"] <- NA
data <- data[!is.na(data$Modifiers), ]
data$Modifiers <- as.factor(data$Modifiers)

# Drop unnecessary columns
data <- data[, !(names(data) %in% c("ID", "Timestamp"))]

# Normalize numerical features (important for kNN, Neural Net)
normalize <- function(x) (x - min(x)) / (max(x) - min(x))
data_norm <- as.data.frame(lapply(data[, -ncol(data)], normalize))
data_norm$Modifiers <- data$Modifiers

# i am saving the cleaned and normalized data to a new file
write.csv(data_norm, "D:/DU-Sem1/Period 2/Statistical Learning/Assignment 1 Folder/Task 2/df4_5s_cleaned.csv", row.names = FALSE)


# Step 2: i am spliting data  into Train and Test Set

set.seed(123)
split <- sample.split(data_norm$Modifiers, SplitRatio = 0.7)
train <- subset(data_norm, split == TRUE)
test <- subset(data_norm, split == FALSE)

train_x <- train[, -ncol(train)]
train_y <- train$Modifiers
test_x <- test[, -ncol(test)]
test_y <- test$Modifiers

# -----------------------------
# Step 3: Here, i am Training  and Evaluate Models


# ---- Logistic Regression ----
log_model <- multinom(Modifiers ~ ., data = train)
log_pred <- predict(log_model, test_x)
log_pred <- factor(log_pred, levels = levels(test_y))
confusionMatrix(log_pred, test_y)

# ---- k-Nearest Neighbors ----
k <- 5
knn_pred <- knn(train = train_x, test = test_x, cl = train_y, k = k)
knn_pred <- factor(knn_pred, levels = levels(test_y))
confusionMatrix(knn_pred, test_y)

# ---- Naive Bayes ----
nb_model <- naiveBayes(Modifiers ~ ., data = train)
nb_pred <- predict(nb_model, test_x)
nb_pred <- factor(nb_pred, levels = levels(test_y))
confusionMatrix(nb_pred, test_y)

# ---- Neural Network ----
set.seed(123)
nn_model <- nnet(Modifiers ~ ., data = train, size = 10, maxit = 200)
nn_pred <- predict(nn_model, test_x, type = "class")
nn_pred <- factor(nn_pred, levels = levels(test_y))
confusionMatrix(nn_pred, test_y)

# -----------------------------
# Step 4: Accuracy Summary

model_names <- c("Logistic Regression", "kNN", "Naive Bayes", "Neural Network")
accuracies <- c(
  mean(log_pred == test_y),
  mean(knn_pred == test_y),
  mean(nb_pred == test_y),
  mean(nn_pred == test_y)
)
accuracy_df <- data.frame(Model = model_names, Accuracy = accuracies)
print(accuracy_df)

# -----------------------------
# Step 5: Precision, Recall, F1 (multi-class averaged)

get_metrics <- function(pred, actual) {
  cm <- confusionMatrix(pred, actual)
  precision <- mean(cm$byClass[,"Precision"], na.rm = TRUE)
  recall <- mean(cm$byClass[,"Recall"], na.rm = TRUE)
  f1 <- mean(cm$byClass[,"F1"], na.rm = TRUE)
  return(c(precision, recall, f1))
}
# Call get_metrics with both prediction and actual vectors using mapply
predictions <- list(log_pred, knn_pred, nb_pred, nn_pred)

metrics_matrix <- mapply(get_metrics, predictions, MoreArgs = list(actual = test_y))
metrics_df <- data.frame(
  Model = model_names,
  t(metrics_matrix)
)
colnames(metrics_df)[2:4] <- c("Precision", "Recall", "F1_Score")
print(metrics_df)


# -----------------------------
# Step 6: Accuracy Bar Plot

# Accuracy Bar Plot with White Background
ggplot(accuracy_df, aes(x = Model, y = Accuracy, fill = Model)) +
  geom_bar(stat = "identity", width = 0.4) +  # thinner bars
  theme_minimal(base_size = 14) +
  theme(
    panel.background = element_rect(fill = "white", color = NA),  # no inner border
    plot.background = element_rect(fill = "white", color = "black", linewidth = 1),  # outer border only
    legend.position = "none"
  ) +
  labs(
    title = "Model Accuracy Comparison",
    x = "Model",
    y = "Accuracy"
  )
ggsave("D:/DU-Sem1/Period 2/Statistical Learning/Assignment 1 Folder/Task 2/accuracy_plot.png", width = 7, height = 5, dpi = 300)

# -----------------------------
# ROC Curve Note (for binary only)
# -----------------------------
# pROC's `roc()` only works for binary classification.
# If you're working with more than 2 behaviors, skip ROC or use `multiclass.roc()` (less visually helpful).
# For visual ROC, limit to 2 classes:
#   binary_data <- subset(data_norm, Modifiers %in% c("Walking", "Grazing"))
#   binary_data$Modifiers <- factor(binary_data$Modifiers)
#   ... (re-run steps for binary ROC)

# -----------------------------
# Confusion Matrix Heatmap for Neural Network
# -----------------------------


# Prepare data
nn_cm <- confusionMatrix(nn_pred, test_y)$table
nn_cm_df <- as.data.frame(nn_cm)
colnames(nn_cm_df) <- c("Predicted", "Actual", "Freq")

# Green heatmap
heatmap_plot <- ggplot(nn_cm_df, aes(x = Actual, y = Predicted, fill = Freq)) +
  geom_tile(color = "white", size = 0.5) +
  scale_fill_gradient(low = "#e5f5e0", high = "#006d2c", name = "Count") +  # green scale
  theme_minimal(base_size = 12) +
  theme(
    axis.text.x = element_text(angle = 45, hjust = 1),
    panel.background = element_rect(fill = "white", color = NA),
    plot.background = element_rect(fill = "white", color = "black", linewidth = 1),
    panel.grid = element_blank()
  ) +
  labs(
    title = "Confusion Matrix Heatmap – Neural Network",
    x = "Actual Behavior",
    y = "Predicted Behavior"
  )

# Show the plot
print(heatmap_plot)

# Save to Desktop
ggsave("D:/DU-Sem1/Period 2/Statistical Learning/Assignment 1 Folder/Task 2/confusion_heatmap_nn.png", plot = heatmap_plot, width = 8, height = 6, dpi = 300)

