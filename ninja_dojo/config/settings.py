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
    }

    return default_settings
