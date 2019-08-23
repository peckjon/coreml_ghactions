from coremltools.converters.sklearn import convert
import pandas as pd
from sklearn.linear_model import LinearRegression

# train simple linear regression model on prices.csv and export to CoreML
def main():
    data = pd.read_csv('prices.csv')
    model = LinearRegression()
    model.fit(data[["sqft"]], data["price"])
    coreml_model = convert(model, "sqft", "price")
    coreml_model.save('pricing.mlmodel')
    print('Saved pricing.mlmodel')


if __name__ == "__main__":
    main()