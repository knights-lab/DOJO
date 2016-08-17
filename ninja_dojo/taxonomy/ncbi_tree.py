"""
This library was adapted from:
        https://github.com/luo-chengwei/utilitomics

This library works with the taxonomy db download from NCBI FTP:

ftp://ftp.ncbi.nih.gov:/pub/taxonomy/taxdump.tar.gz

Init an taxonomy tree obj by:

t_tree = ncbi.NCBITree()
then you can get the taxonomy ranks by using:

path = t_tree.get_name_path_with_taxon_id(taxon_id)
"""
import os
import networkx as nx
import csv
from functools import lru_cache
from collections import defaultdict

from ninja_utils.factory import Pickleable, download

from .. import SETTINGS, LOGGER
from ..downloaders import NCBITaxdmp


class NCBITree(Pickleable):
    def __init__(self, mp_ranks=None, _downloaders=(NCBITaxdmp(),)):
        # Private variables (should be set in settings)
        self._downloaders = _downloaders
        if mp_ranks is None:
            self.mp_ranks = dict(zip(('superkingdom', 'phylum', 'class', 'order', 'family', 'genus', 'species'),
                     ('k__', 'p__', 'c__', 'o__', 'f__', 'g__', 's__')))
        else:
            self.mp_ranks = mp_ranks
        super().__init__(SETTINGS, LOGGER)

    @download
    def _parse(self):
        # Initialize variables
        self.tree = nx.DiGraph()
        self.name2taxon_id = defaultdict(int)
        self.taxon_id2name = defaultdict(str)
        ncbi_taxdmp_dir = self._downloaders[0].path
        # csv.field_size_limit(sys.maxsize)

        with open(os.path.join(ncbi_taxdmp_dir, 'names.dmp'), 'r') as handle:
            # csv_handle = csv.reader(handle, delimiter="\t")
            for cols in handle:
                cols = cols.split('\t')
                taxon_id = int(cols[0])
                name = cols[2]
                self.name2taxon_id[name] = taxon_id
                if cols[-2] == 'scientific name':
                    self.taxon_id2name[taxon_id] = name

        # construct node tree
        edges = []
        nodes = {}
        with open(os.path.join(ncbi_taxdmp_dir, 'nodes.dmp'), 'r') as handle:
            csv_handle = csv.reader(handle, delimiter="\t")
            for cols in csv_handle:
                parent_node = int(cols[2])
                child_node = int(cols[0])
                rank = cols[4]
                nodes[child_node] = rank
                if child_node != parent_node:
                    edges.append((child_node, parent_node))

        self.tree.add_edges_from(edges)
        nx.set_node_attributes(self.tree, 'rank', nodes)

    def dfs_traversal(self):
        # ncbi_tid, rank, name, parent_ncbi_tid
        with open(os.path.join(self._downloaders[0].path, 'nodes.dmp'), 'r') as inf:
            csv_handle = csv.reader(inf, delimiter='\t')
            for cols in csv_handle:
                node = int(cols[0])
                parent = int(cols[2])
                rank = self.tree.node[node]['rank']
                name = self.taxon_id2name[node]
                yield node, rank, name, parent

    def get_taxon_id_lineage_with_taxon_id(self, taxon_id):
        if taxon_id in self.tree:
            for i in nx.dfs_preorder_nodes(self.tree, taxon_id):
                yield i

    def get_taxon_id_lineage_with_name(self, name):
        if name not in self.name2taxon_id:
            return []
        return self.get_taxon_id_lineage_with_taxon_id(self.name2taxon_id[name])

    def get_name_lineage_with_taxon_id(self, taxon_id):
        tid_lineage = self.get_taxon_id_lineage_with_taxon_id(taxon_id)
        name_lineage = []
        for x in tid_lineage:
            rank = self.tree.node[x]['rank']
            name = self.taxon_id2name[x]
            name_lineage.append((name, rank))
        return name_lineage

    def get_name_lineage_with_name(self, name):
        if name not in self.name2taxon_id:
            return []
        path = self.get_name_lineage_with_taxon_id(self.name2taxon_id[name])
        return path

    def get_rank_with_taxon_id(self, taxon_id, rank):
        taxon_id_lineage = self.get_taxon_id_lineage_with_taxon_id(taxon_id)
        name_lineage = self.get_name_lineage_with_taxon_id(taxon_id)
        for tid, (name, x) in zip(taxon_id_lineage, name_lineage):
            if x == rank:
                return tid, name
        return None, None

    def get_name_at_rank(self, name, rank):
        if name not in self.name2taxon_id:
            return None, None
        return self.get_rank_with_taxon_id(self.name2taxon_id[name], rank)

    def get_lineage(self, taxon_id, ranks={'superkingdom', 'phylum', 'class', 'order', 'family', 'genus', 'species'}):
        taxon_id_lineage = self.get_taxon_id_lineage_with_taxon_id(taxon_id)
        name_lineage = []
        for x in taxon_id_lineage:
            rank = self.tree.node[x]['rank']
            name = self.taxon_id2name[x]
            if rank in ranks:
                name_lineage.append((name, x, rank))
        return name_lineage

    def get_lineage_depth(self, taxon_id, depth, ranks=('superkingdom', 'phylum', 'class', 'order', 'family', 'genus', 'species')):
        taxon_id_lineage = self.get_taxon_id_lineage_with_taxon_id(taxon_id)
        ranks = set(ranks[depth:])
        lineage = []
        for x in taxon_id_lineage:
            rank = self.tree.node[x]['rank']
            if rank in ranks:
                lineage.append(x)
        return lineage

    # Note that this will create a global cache for all instances of NCBITree.
    # Will be fine unless if you want to compare trees.
    #TODO: This method will be deprecated
    @lru_cache(maxsize=128)
    def gg_lineage(self, taxon_id):
        taxon_id_lineage = self.get_taxon_id_lineage_with_taxon_id(taxon_id)
        name_lineage = []
        for x in taxon_id_lineage:
            rank = self.tree.node[x]['rank']
            name = self.taxon_id2name[x]
            if rank in self.mp_ranks:
                name_lineage.append(self.mp_ranks[rank] + name.replace(' ', '_'))
        return ';'.join(reversed(name_lineage))

    @lru_cache(maxsize=128)
    def green_genes_lineage(self, taxon_id, depth=7):
        taxon_id_lineage = self.get_taxon_id_lineage_with_taxon_id(taxon_id)
        name_lineage = []
        for x in taxon_id_lineage:
            rank = self.tree.node[x]['rank']
            name = self.taxon_id2name[x]
            if rank in self.mp_ranks:
                name_lineage.append(self.mp_ranks[rank] + name.replace(' ', '_'))
        taxonomy = name_lineage[::-1]
        if len(taxonomy) >= depth:
            return ';'.join(taxonomy[:depth])

    @lru_cache(maxsize=128)
    def lowest_common_ancestor(self, p, q):
        path_p = nx.shortest_path(self.tree, p, 1)
        path_q = nx.shortest_path(self.tree, q, 1)

        size_p = len(path_p)
        size_q = len(path_q)

        p_off = size_p - size_q if size_p - size_q > 0 else 0
        q_off = size_q - size_p if size_q - size_p > 0 else 0

        for i, j in zip(path_p[p_off:], path_q[q_off:]):
            if i == j:
                return i


def main():
    ncbi_tree = NCBITree()
    print(ncbi_tree.gg_lineage(9606))

if __name__ == '__main__':
    main()
