from app.models import DecisionTreeModel
from project.decision_tree.interfaces import IDecisionTree
from project.entities.decision_tree import DecisionTree
from project.entities.decision_tree_node import DecisionTreeNode


class DecisionTreeRepoFactory(object):
    @staticmethod
    def get() -> IDecisionTree:
        return DjDecisionTree()


class DjDecisionTree(IDecisionTree):

    def get_categories(self) -> [str]:
        categories = []
        trees = DecisionTreeModel.objects.filter(level=0)

        for tree in trees:
            categories.append(str(tree))
        return categories

    def _fill_decision_tree(self, node: DecisionTreeNode, tree: DecisionTreeModel):
        children = tree.get_children()
        if len(children) == 0:
            return
        for ch in children:
            child_node = DecisionTreeNode(ch.id, title=ch.name, instruction=ch.instruction, image=ch.image,
                                          next_nodes=[], step=str(ch.id))
            self._fill_decision_tree(child_node, ch)

            node.next_nodes.append(child_node)

        return node

    def get_decision_tree(self, category: str) -> DecisionTree:
        root = DecisionTreeModel.objects.get(level=0, name=category)
        decision_tree = DecisionTree(id=root.id, category=root.name, instruction=root.instruction, image=root.image,
                                     nodes=[], created_at=root.created_at, updated_at=root.updated_at)
        children = root.get_children()
        for ch in children:
            node = DecisionTreeNode(ch.id, title=ch.name, instruction=ch.instruction, image=ch.image, next_nodes=[],
                                    step=str(ch.id))
            self._fill_decision_tree(node, ch)

            decision_tree.nodes.append(node)

        if decision_tree:
            return decision_tree

        return None
