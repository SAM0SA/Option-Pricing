import math
import time

class AsianCallNode:

    def __init__(self):
        self.price = None
        self.option_price = None
        self.up_child = None
        self.down_child = None
        self.running_avg = None
        self.sum = None

    def set_price(self, price):
        self.price = price
        self.running_avg = price
        self.sum = price

class AsianCallBinomialTree:

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
        # start_time = time.time() * 1000
        self.__compute_children_price(u,d)
        self.__compute_option_price(self.root, p)

        # final_time = (time.time()*1000)-start_time
        #
        # print(final_time)

    def __calculate_u(self):
        u = math.e ** (self.sigma * math.sqrt(self.dt))
        return u

    def __compute_children_price(self, u, d):

        if self.level == self.n:
            return

        leaf_nodes_at_t = self.leaf_nodes_at_t
        leaf_nodes_at_t_plus_1 = []
        for i in range(0, len(leaf_nodes_at_t)):
            up_child = AsianCallNode()
            down_child = AsianCallNode()
            current_node = leaf_nodes_at_t[i]
            current_node.up_child = up_child
            current_node.down_child = down_child
            leaf_nodes_at_t_plus_1.append(up_child)
            leaf_nodes_at_t_plus_1.append(down_child)
            Su = current_node.price * u
            Sd = current_node.price * d
            up_child.set_price(Su)
            down_child.set_price(Sd)
            sum_u = Su + current_node.sum
            sum_d = Sd + current_node.sum
            up_child.sum = sum_u
            down_child.sum = sum_d
            up_child.running_avg = sum_u/(self.level + 2)
            down_child.running_avg = sum_d/(self.level + 2)

        self.leaf_nodes_at_t = leaf_nodes_at_t_plus_1
        self.level = self.level + 1
        self.__compute_children_price(u, d)

    def __calculate_p(self, u, d):
        p = (math.exp(self.r * self.dt) - d)/(u-d)
        return p

    def __compute_option_price(self, node, p):

        if node.up_child is None or node.down_child is None:
            fl = max(node.running_avg - self.K, 0)
            node.option_price = fl
            return fl

        f = math.exp(-1 * self.r * self.dt)*((p*self.__compute_option_price(node.up_child, p)) +
                                             ((1-p)*self.__compute_option_price(node.down_child, p)))
        #f = max(f, self.K - node.price)
        node.option_price = f
        return f
