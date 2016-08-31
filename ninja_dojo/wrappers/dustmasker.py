from ninja_utils.utils import run_command


def dustmasker(infile, outfile, infmt='fasta', outfmt='fasta', shell=False):
    """
    Search a bowtie2 index with multiple alignment.
    :param infile: the query FASTA file
    :param outfile: the resulting SAM file
    :param database: path to the bowtie2 index
    :param alignments_to_report: the number of alignments to report (default=32)
    :param num_threads: the number of threads to use (default=SETTINGS)
    :param shell: whether to use the shell NOT RECOMMENDED (default=False)
    :return: the STDERR/STDOUT
    """
    cmd = [
        'dustmasker',
        '-in', infile,
        '-out', outfile,
        '-infmt', infmt,
        '-outfmt', outfmt
    ]
    cmd = [str(i) for i in cmd]
    return run_command(cmd, shell=shell)
