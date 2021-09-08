### Data processing of iris data-set 

### process function (import if needed)
def process():
    with open('iris.data', 'r') as iris:
        irisdata = iris.read()

        # Replace the target string with a one-hot encoding
        irisdata = irisdata.replace('Iris-setosa', '001')
        irisdata = irisdata.replace('Iris-versicolor', '010')
        irisdata = irisdata.replace('Iris-virginica', '100')

        # Write the file out again
        with open('iris_clean.csv', 'w') as file: ### w will create new file if it doesn't already exist 
            file.write(irisdata)

process()
