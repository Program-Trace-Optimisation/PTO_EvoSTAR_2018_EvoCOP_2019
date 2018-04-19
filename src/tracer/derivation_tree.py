##### DERIVATION TREE

class DerivationTree:
    # naming schemes naturally induce a tree structure (analogous to
    # the derivation tree in GE). this structure should be useful for
    # understanding the effect of search operators at a phenotype
    # level wrt a naming scheme e.g., crossover on traces can be also
    # seen as recombining aligned tree structures

    class Node:
        def __init__(self, addr_part, value=None):
            self.addr_part = addr_part
            self.value = value
            self.children = []

        def add_child(self, obj):
            self.children.append(obj)

    def __init__(self, trace):
        self.trace = trace
        self.derivation_tree = None

    def trace_to_tree(self):
        root = self.Node(())
        for address in self.trace:
            self.add_trace_entry(root, address, self.trace[address])
        self.derivation_tree = root

    def add_trace_entry(self, parent, address, value):
        addr_part = address[0] #assumes the len of adrress is >= 1

        if addr_part not in [child.addr_part for child in parent.children]:
            if len(address) == 1:
                child = self.Node(addr_part, value)
            else:
                child = self.Node(addr_part)
            parent.add_child(child)
        else:
            child = [child for child in parent.children if child.addr_part == addr_part][0]

        if len(address) > 1:
            self.add_trace_entry(child, address[1:], value)
        else:
            return

    def tree_to_trace(self):
        return self.trace # cheating as we should reconstruct trace from tree

    def sort_tree(self):
        pass

    def flatten(self, s):
        # flattens two levels of nested sequences to one level, and
        # works even if some items at the first level are not
        # sequences.
        r = []
        for item in s:
            if isinstance(item, Sequence):
                r.extend(item)
            else:
                r.append(item)
        return r

    def display_tree(self, node = None, ident = 0):

        if node == None:
            node = self.derivation_tree

        print(" " * ident, node.addr_part, " -> ",)

        if node.value is not None:
            f, args, output = node.value
            print("args", args)
            args = self.flatten(args)
            args = [ arg.__name__ if hasattr(arg, "__name__") else arg for arg in args ]
            output = output.__name__ if hasattr(output, "__name__") else output
            print(f.__name__ + str(args) + " = " + str(output))
        else:
            print(".")

        for child in node.children:
            self.display_tree(child, ident + 4)

    def tree_to_graphviz(self, filename, ext="eps"):
        """Generate a tree diagram using Graphviz."""

        # First, setup.
        ID = itertools.count(0)
        def _r(n, n_ID):
            if n.value is not None:
                f, args, output = n.value
                label = output
                if callable(label):
                    label = label.__name__
            else:
                if len(n.addr_part):
                    label = n.addr_part[1]
                else:
                    label = "generator"
            label = str(label)
            label = label.replace("&", "&amp;")
            label = label.replace("<", "&lt;")
            label = label.replace(">", "&gt;")
            label = label.replace('"', "&quot;")
            if not len(n.children):
                # it's a leaf
                # print("leaf")
                ofile.write('    n%d [label=<<B>%d</B>: %s>,style=filled,fillcolor="#DDDDDD"];\n' % (n_ID, n_ID, label))
            else:
                ofile.write('    n%d [label=<<B>%d</B>: %s>];\n' % (n_ID, n_ID, label))

            for c in n.children:
                c_ID = next(ID)
                ofile.write("    n%d -> n%d;\n" % (n_ID, c_ID))
                _r(c, c_ID)

        # Next, output to a .dot file.
        ofile = open(filename + ".dot", "w")
        ofile.write("strict digraph tree {\n")
        ofile.write("    node [shape=box];\n")
        n0 = self.derivation_tree
        _r(n0, next(ID))
        ofile.write("}\n")
        ofile.close()


        # Finally, run Graphviz. Ask it to output svg, because the
        # HTML-style font attributes only work in svg output. Then
        # convert to desired format.
        command = "dot -Tsvg -o%s.svg < %s.dot" % (filename, filename)
        command2 = "convert %s.svg %s.%s" % (filename, filename, ext)
        try:
            os.system(command)
            os.system(command2)
            print("Created %s.%s" % (filename, ext))
        except:
            print("Failed to create %s.%s. Do you have Graphviz (dot) and ImageMagick (convert)?" % (filename, ext))



