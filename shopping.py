import csv
import sys

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")


def load_data(filename):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).

    evidence should be a list of lists, where each list contains the
    following values, in order:
        - 0 Administrative, an integer
        - 1 Administrative_Duration, a floating point number
        - 2 Informational, an integer
        - 3 Informational_Duration, a floating point number
        - 4 ProductRelated, an integer
        - 5 ProductRelated_Duration, a floating point number
        - 6 BounceRates, a floating point number
        - 7 ExitRates, a floating point number
        - 8 PageValues, a floating point number
        - 9 SpecialDay, a floating point number
        - 10 Month, an index from 0 (January) to 11 (December)
        - 11 OperatingSystems, an integer
        - 12 Browser, an integer
        - 13 Region, an integer
        - 14 TrafficType, an integer
        - 15 VisitorType, an integer 0 (not returning) or 1 (returning)
        - 16 Weekend, an integer 0 (if false) or 1 (if true)

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """
    with open(filename) as f:
        reader = csv.reader(f)
        next(reader)

        evidence = []
        labels = []
        for row in reader:
            row_by_row_evidence = []
            for i in range(0, len(row) - 1):
                if i == 0 or i == 2 or i == 4 or ( i > 10 and i < 15 ):
                    row_by_row_evidence.append(int(row[i]))
                elif i == 10:
                    row_by_row_evidence.append(["Jan","Feb","Mar","Apr","May","June","Jul","Aug","Sep","Oct","Nov","Dec"].index(row[i]))
                elif i == 15 and row[i] != "Returning_Visitor":
                    row_by_row_evidence.append(0)
                elif i == 15 and row[i] == "Returning_Visitor":
                    row_by_row_evidence.append(1)
                elif i == 1 or i == 3 or ( i > 4 and i < 10 ):
                    row_by_row_evidence.append(float(row[i]))
                elif i == 16 and row[i] == "FALSE":
                    row_by_row_evidence.append(0)
                elif i == 16 and row[i] == "TRUE":
                    row_by_row_evidence.append(1)

            evidence.append(row_by_row_evidence)
            labels.append(0 if row[17] == "FALSE" else 1)
    return (evidence, labels)

def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    neigh = KNeighborsClassifier(n_neighbors=1)
    return neigh.fit(evidence, labels)


def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificity).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """

    # CALCULATE sensitivity
    n = 0
    tpr_true = 0
    tpr_count = 0
    for result in labels:
        if result == 1:
            tpr_count += 1
            if predictions[n] == 1:
                tpr_true += 1
        n += 1
    
    sensitivity = tpr_true / tpr_count
    
    # CALCULATE specificity
    n = 0
    tnr_true = 0
    tnr_count = 0
    for result in labels:
        if result == 0:
            tnr_count += 1
            if predictions[n] == 0:
                tnr_true += 1
        n += 1
    specificity = tnr_true / tnr_count

    return (sensitivity, specificity)


if __name__ == "__main__":
    main()
