from project.decision_tree.interfaces import IDecisionTree
from project.entities.decision_tree import DecisionTree
from project.entities.decision_tree_node import DecisionTreeNode

trees = [DecisionTree(category='I dont know', instruction='test_instruction1',
                      nodes=[DecisionTreeNode(title="test3", step="test_step3", instruction="test_instruction3",
                                              next_nodes=[DecisionTreeNode(title="test1", step="test_step1",
                                                                           instruction="test_instruction1",
                                                                           next_nodes=[
                                                                               DecisionTreeNode(title="test5",
                                                                                                step="test_step5",
                                                                                                instruction="test_instruction5"),
                                                                               DecisionTreeNode(title="test6",
                                                                                                step="test_step6",
                                                                                                instruction="test_instruction6")]),
                                                          DecisionTreeNode(title="test2", step="test_step2",
                                                                           instruction="test_instruction2",
                                                                           next_nodes=[
                                                                               DecisionTreeNode(title="test7",
                                                                                                step="test_step7",
                                                                                                instruction="test_instruction7"),
                                                                               DecisionTreeNode(title="test8",
                                                                                                step="test_step8",
                                                                                                instruction="test_instruction8")])])]),
         DecisionTree(category='A person has a trauma', instruction='test_instruction2',
                      nodes=[DecisionTreeNode(title="test3", step="test_step3", instruction="test_instruction3",
                                              next_nodes=[DecisionTreeNode(title="test1", step="test_step1",
                                                                           instruction="test_instruction1",
                                                                           next_nodes=[
                                                                               DecisionTreeNode(title="test5",
                                                                                                step="test_step5",
                                                                                                instruction="test_instruction5"),
                                                                               DecisionTreeNode(title="test6",
                                                                                                step="test_step6",
                                                                                                instruction="test_instruction6")]),
                                                          DecisionTreeNode(title="test2", step="test_step2",
                                                                           instruction="test_instruction2",
                                                                           next_nodes=[
                                                                               DecisionTreeNode(title="test7",
                                                                                                step="test_step7",
                                                                                                instruction="test_instruction7"),
                                                                               DecisionTreeNode(title="test8",
                                                                                                step="test_step8",
                                                                                                instruction="test_instruction8")])])])]


class DecisionTreeRepoFactory(object):
    @staticmethod
    def get() -> IDecisionTree:
        return DjDecisionTree()


class DjDecisionTree(IDecisionTree):

    def get_categories(self) -> [str]:
        categories = []
        global trees
        for tree in trees:
            categories.append(tree.category)
        return categories

    def get_decision_tree(self, category: str) -> DecisionTree:
        global trees

        for tree in trees:
            if tree.category == category:
                return tree
        return None
