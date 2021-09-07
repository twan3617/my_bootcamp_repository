### Data processing of iris data-set 

### process function (import if needed)
def process():
    with open('iris.data', 'r') as iris:
        irisdata = iris.read()

        # Replace the target string
        irisdata = irisdata.replace('Iris-setosa', '0')
        irisdata = irisdata.replace('Iris-versicolor', '1')
        irisdata = irisdata.replace('Iris-virginica', '2')

        # Write the file out again
        with open('iris_clean.csv', 'w') as file: ### w will create new file if it doesn't already exist 
            file.write(irisdata)
