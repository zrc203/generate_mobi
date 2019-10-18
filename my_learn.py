# Import Library
# Import other necessary libraries like pandas, numpy...
from sklearn import linear_model

# Load Train and Test datasets
# Identify feature and response variable(s) and values must be numeric and numpy arrays
x_train = 3
y_train = 6
x_test = 2

# Create linear regression object
linear = linear_model.LinearRegression()
linear.fit([[3, 6], [2, 4]], [[4, 8], [8, 16]])
# Train the model using the training sets and check score
linear.score([[3, 6], [2, 4]], [[4, 8], [8, 16]])

# Equation coefficient and Intercept
# print('Coefficient: n', linear.coef_)
# print('Intercept: n', linear.intercept_)

# Predict Output
predicted = linear.predict([[3, 7], [2, 5]])
print(predicted)
