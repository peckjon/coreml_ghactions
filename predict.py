from coremltools.models import MLModel
import csv

def main():
    model = MLModel('pricing.mlmodel')
    with open('input.csv') as input:
        csv_reader = csv.reader(input, delimiter=',')
        with open('output.csv', mode='w') as output:
            csv_writer = csv.writer(output, delimiter=',')
            for row in csv_reader:
                sqft = int(row[0])
                price = int(model.predict({'sqft': sqft})['price'])
                csv_writer.writerow([sqft, price])
    print('Saved output.csv')


if __name__ == "__main__":
    main()
