import sys
from AmericanPutOption import AmericanPutNode
from AmericanPutOption import AmericanPutBinomialTree
from AsianCallOption import AsianCallNode
from AsianCallOption import AsianCallBinomialTree

def compute(r, T, n, sigma, S0, K):
    american_put_root = AmericanPutNode()
    american_put_root.set_price(S0)
    american_binomial_tree = AmericanPutBinomialTree(r, T, n, sigma, S0, K)
    american_binomial_tree.insert_root(american_put_root)
    print("American Put: ")
    print(american_put_root.option_price)

    asian_call_root = AsianCallNode()
    asian_call_root.set_price(50)
    asian_binomial_tree = AsianCallBinomialTree(r, T, n, sigma, S0, K)
    asian_binomial_tree.insert_root(asian_call_root)
    print("Asian Call: ")
    print(asian_call_root.option_price)

if __name__ == '__main__':

    file_path = sys.argv[1]
    data_file = open(file_path, "r")
    for line in data_file:
        data = line.split('\t')

        for i in range(len(data)):
            data[i] = float(data[i])

        compute(data[0], data[1], data[2], data[3], data[4], data[5])

    #compute(0.05, .5, 500, .3, 50, 52) #Testing