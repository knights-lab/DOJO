from setuptools import setup, find_packages

__author__ = "Knights Lab"
__copyright__ = "Copyright (c) 2016--, %s" % __author__
__credits__ = ["Benjamin Hillmann", "Dan Knights", "Gabe Al-Ghalith", "Tonya Ward", "Pajua Vangay"]
__email__ = "hillmannben@gmail.com"
__license__ = "GPL"
__maintainer__ = "Benjamin Hillmann"
__version__ = "0.0.1-dev"

long_description = ''

setup(
    name='dojo',
    version=__version__,
    packages=find_packages(),
    url='',
    license=__license__,
    author=__author__,
    author_email=__email__,
    description='',
    test_suite='nose.collector',
    long_description=long_description,
    # scripts=glob(os.path.join('scripts', '*py')),
    entry_points={
        'console_scripts': [
            'annotate_fasta = dojo.scripts.annotate_fasta:annotate_fasta',
            'extract_ncbi_tid_from_mp2_gold = dojo.scripts.extract_ncbi_tid_from_mp2_gold:extract_ncbi_tid',
            'refseq_get_ftp_links_from_file = dojo.scripts.refseq_get_ftp_links_from_file:refseq_get_ftp_links_from_file',
            'hardmasker = dojo.scripts.hardmasker:hardmasker',
            'add_green_genes_tax_to_gb_accession = dojo.scripts.add_green_genes_tax_to_gb_accession:add_green_genes_tax_to_gb_accession',
        ]
    },
    keywords='',
    install_requires=['click', 'networkx', 'nose', 'pandas', 'blaze', 'cytoolz']
)
#TODO scipy 0.18.1 breaks python date-utils installation currently, don't know why. Force this version in the actual setup.py
