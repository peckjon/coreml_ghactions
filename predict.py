from coremltools.models import MLModel
import csv


def main():
    model = MLModel('pricing.mlmodel') #thanks https://github.com/princeSmall/CoreMLModel
    with open('input.csv') as input:
        csv_reader = csv.reader(input, delimiter=',')
        with open('output.csv', mode='w') as output:
            csv_writer = csv.writer(output, delimiter=',')
            for row in csv_reader:
                sqft = row[0]
                price = model.predict({'sqft': int(row[0])})['price']
                print([sqft, int(price)])
                csv_writer.writerow([sqft, int(price)])


if __name__ == "__main__":
    main()