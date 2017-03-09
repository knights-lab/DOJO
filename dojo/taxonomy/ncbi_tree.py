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
from collections import defaultdict, OrderedDict
import itertools
import cytoolz
from ninja_utils.factory import Pickleable, download

from .. import SETTINGS, LOGGER
from ..downloaders import NCBITaxdmp


class NCBITree(Pickleable):
    def __init__(self, lineage_ranks=None, _downloaders=(NCBITaxdmp(),)):
        # Private variables (should be set in settings)
        self._downloaders = _downloaders
        if lineage_ranks is None:
            self.lineage_ranks = OrderedDict(zip(('superkingdom', 'phylum', 'class', 'order', 'family', 'genus', 'species'),
                                                 ('k__', 'p__', 'c__', 'o__', 'f__', 'g__', 's__')))
        else:
            self.lineage_ranks = lineage_ranks
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

    def get_rank_from_taxon_id(self, taxon_id):
        if taxon_id in self.tree:
            return self.tree.node[taxon_id]['rank']

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
            if rank in self.lineage_ranks:
                name_lineage.append(self.lineage_ranks[rank] + name.replace(' ', '_'))
        return ';'.join(reversed(name_lineage))

    @cytoolz.memoize()
    def green_genes_lineage(self, taxon_id, depth=7, depth_force=False):
        taxon_id_lineage = self.get_taxon_id_lineage_with_taxon_id(taxon_id)
        lineage = GreenGenesLineage(depth=depth, depth_force=depth_force)
        for node_id in taxon_id_lineage:
            rank = self.tree.node[node_id]['rank']
            name = self.taxon_id2name[node_id]
            lineage[rank] = name
        try:
            return str(lineage)
        except TypeError:
            return None

    @cytoolz.memoize()
    def lowest_common_ancestor(self, p, q):
        try:
            path_p = nx.shortest_path(self.tree, p, 1)
            path_q = nx.shortest_path(self.tree, q, 1)

            size_p = len(path_p)
            size_q = len(path_q)

            p_off = size_p - size_q if size_p - size_q > 0 else 0
            q_off = size_q - size_p if size_q - size_p > 0 else 0

            for i, j in zip(path_p[p_off:], path_q[q_off:]):
                if i == j:
                    return i
        # Unable to find a node in the digraph
        except nx.exception.NetworkXError:
            return None


class GreenGenesLineage:
    def __init__(self, depth_force=False, depth=7):
        self.depth_force = depth_force
        self.depth = depth
        self.strain_flag = self.depth == 8
        self.names = list(itertools.repeat('', self.depth))
        self._lineage_ranks = dict(zip(('superkingdom', 'phylum', 'class', 'order', 'family', 'genus', 'species', 'strain'), range(self.depth)))
        self._prefixes = ('k', 'p', 'c', 'o', 'f', 'g', 's', 't')
        self.previous_name = None
        self.current_name = None
        self.first_name = None
        self.first_flag = True

    def __setitem__(self, rank, name):
        self.previous_name = self.current_name
        self.current_name = name.replace(" ", "_")

        if self.first_flag:
            self.first_flag = False
            self.first_name = self.current_name

        if self.strain_flag:
            if rank == 'species':
                self.names[self._lineage_ranks['strain']] = self.first_name
                self.names[self._lineage_ranks['species']] = self.current_name
                self.strain_flag = False
        elif rank in self._lineage_ranks:
            self.names[self._lineage_ranks[rank]] = self.current_name
        if self.current_name == "Viruses":
            self.names[self._lineage_ranks['phylum']] = self.previous_name

    def __getitem__(self, rank):
        if rank in self._lineage_ranks:
            return '%s__%s' % (self._prefixes[self._lineage_ranks[rank]], self.names[self._lineage_ranks[rank]])

    def __str__(self):
        if not self.depth:
            for indx, val in enumerate(reversed(self.names)):
                if val:
                    return ';'.join('%s__%s' % i for i in zip(self._prefixes, itertools.islice(self.names, 8-indx)))
        elif self.depth_force:
            return ';'.join('%s__%s' % i for i in zip(self._prefixes, self.names))
        elif self.names[self.depth-1]:
            return ';'.join('%s__%s' % i for i in zip(self._prefixes, itertools.islice(self.names, self.depth)))

    def reset(self):
        self.names = list(itertools.repeat('', self.depth))
        self.strain_flag = self.depth == 8
        self.previous_name = None
        self.current_name = None
        self.first_name = None
        self.first_flag = True



def main():
    ncbi_tree = NCBITree()
    print(ncbi_tree.green_genes_lineage(9606))

if __name__ == '__main__':
    main()
