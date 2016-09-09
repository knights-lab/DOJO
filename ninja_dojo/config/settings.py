def ninja_dojo_settings():
    default_settings = {
        'default_dir': [''],
        'docs_dir': ['docs'],
        'data_dir': ['data'],
        'results_dir': ['results'],
        'pickle_dir': ['data', 'pickle'],
        'ncbi_taxdmp_url': 'ftp://ftp.ncbi.nih.gov:/pub/taxonomy/taxdump.tar.gz',
        'ncbi_taxdmp_dir': ['data', 'ncbi_taxdmp'],
        'silva_taxdmp_urls': [
            'http://www.arb-silva.de/fileadmin/silva_databases/release_119/Exports/taxonomy/taxmap_embl_ssu_parc_119.txt',
            'http://www.arb-silva.de/fileadmin/silva_databases/release_119/Exports/taxonomy/taxmap_embl_lsu_parc_119.txt'],
        'silva_taxdmp_dir': ['data', 'silva_taxdmp'],
        'img_taxdmp_dir': ['data', 'img_taxdmp'],
        'log_persists': False,
        'refseq_summary_urls': ['ftp://ftp.ncbi.nlm.nih.gov/genomes/ASSEMBLY_REPORTS/assembly_summary_refseq.txt'],
        'refseq_summary_dir': ['data', 'refseq_summary'],
        'refseq_catalog_urls': ['ftp://ftp.ncbi.nlm.nih.gov/refseq/release/release-catalog/'],
        'refseq_catalog_dir': ['data', 'refseq_catalog'],
        'refseq_ftp_prefix': 'ftp://ftp.ncbi.nlm.nih.gov/genomes/all/',
        'db_dir': ['db'],
        'nucleotide_catalog_urls': ['ftp://ftp.ncbi.nih.gov/pub/taxonomy/accession2taxid/'],
        'nucleotide_catalog_dir': ['data', 'nucleotide_catalog']
    }

    return default_settings
