import math
import time

class AmericanPutNode:

    def __init__(self):
        self.price = None
        self.option_price = None
        self.up_child = None
        self.down_child = None

    def set_price(self, price):
        self.price = price


class AmericanPutBinomialTree:

    def __init__(self, r, T, n, sigma, S0, K):
        self.root = None
        self.r = r
        self.dt = T/n
        self.n = n
        self.sigma = sigma
        self.S0 = S0
        self.K = K
        self.leaf_nodes_at_t = []
        self.level = 0

    def insert_root(self, root):
        self.root = root
        self.leaf_nodes_at_t.append(root)
        self.__fill_tree()

    def __fill_tree(self):
        u = self.__calculate_u()
        d = u ** -1
        p = self.__calculate_p(u,d)
        # start_time = time.time()*1000
        self.__compute_children_price(u,d)
        self.__compute_option_price(self.root, p)
        # final_time = (time.time()*1000)-start_time

        # print(final_time)

    def __calculate_u(self):
        u = math.e ** (self.sigma * math.sqrt(self.dt))
        return u

    def __compute_children_price(self, u, d):
        #print("called")

        if self.level == self.n:
            return

        leaf_nodes_at_t = self.leaf_nodes_at_t
        leaf_nodes_at_t_plus_1 = []
        for i in range(0, len(leaf_nodes_at_t)):
            # up_child = AmericanPutNode()
            # down_child = AmericanPutNode()
            current_node = leaf_nodes_at_t[i]

            if i == 0:
                up_child = AmericanPutNode()
                down_child = AmericanPutNode()
                up_child.set_price(current_node.price * u)
                down_child.set_price(current_node.price * d)
                current_node.up_child = up_child
                current_node.down_child = down_child
                leaf_nodes_at_t_plus_1.append(up_child)
                leaf_nodes_at_t_plus_1.append(down_child)

            else:
                down_child = AmericanPutNode()
                current_node.up_child = leaf_nodes_at_t[i-1].down_child
                down_child.set_price(current_node.price * d)
                current_node.down_child = down_child
                leaf_nodes_at_t_plus_1.append(down_child)

        self.leaf_nodes_at_t = leaf_nodes_at_t_plus_1
        self.level = self.level + 1
        self.__compute_children_price(u, d)

    def __calculate_p(self, u, d):
        p = (math.exp(self.r * self.dt) - d)/(u-d)
        return p

    def __compute_option_price(self, node, p):
        #print("called")
        if node.up_child is None or node.down_child is None:
            fl = max(self.K - node.price, 0)
            node.option_price = fl
            return fl

        f = math.exp(-1 * self.r * self.dt)*((p*self.__compute_option_price(node.up_child, p)) +
                                             ((1-p)*self.__compute_option_price(node.down_child, p)))
        f = max(f, self.K - node.price)
        node.option_price = f
        return f


# def calculate_option_price(r, T, n, sigma, S0, K):
#     leaf_nodes = []
#     for i in range(2 ** n):
