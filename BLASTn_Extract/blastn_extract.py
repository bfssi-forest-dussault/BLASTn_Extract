#!/usr/bin/env python3

import os
import click
import logging

script = os.path.basename(__file__)
logging.basicConfig(
    format=f'\033[92m \033[1m {script}:\033[0m %(message)s ',
    level=logging.INFO)


@click.command(help="")
@click.option('-i', '--infile',
              type=click.Path(exists=True),
              required=True,
              help='Path to BLASTn file you wish to query')
@click.option('-q', '--query',
              required=True,
              help='Query string to match against. Note that this is case insensitive.')
@click.option('-c', '--contigs',
              required=False,
              default=None,
              help='Path to contig file to pull matches from')
@click.option('-o', '--outdir',
              type=click.Path(exists=True),
              required=False,
              default=None,
              help='Path to directory to store filtered output according to query string. If not specified, output'
                   'will be stored in the same directory as the BLASTn file.')
def cli(infile: str, query: str, contigs: str, outdir: str):
    if contigs is None:
        logging.info("No contig FASTA file provided. Only performing query on BLASTn file.")
        contig_flag = False
    else:
        contig_flag = True

    # Output directory handling
    if outdir is None:
        outdir = os.path.dirname(infile)
    elif not os.path.isdir(outdir):
        os.mkdir(outdir)

    hits = query_blastn(infile, query)

    if len(hits) == 0:
        logging.info(f"No hits found matching query '{query}'. Quitting.")
        quit()

    node_dict = extract_nodes(hits)

    logging.info(f"Hits matching query '{query}':")
    for hit in hits:
        logging.info(hit)

    if contig_flag:
        logging.info(f"Extracting contigs from {contigs}")
        outfasta = extract_contigs(contigs, node_dict, outdir)
        logging.info(f"Extracted contigs available at {outfasta}")

    logging.info("Script complete")


def query_blastn(infile: str, query: str) -> list:
    """
    Checks a BLASTn file for matching the provided query string
    :param infile: Path to BLASTn file
    :param query: String containing query keywords
    :return: List of hits
    """
    # Make query lowercase as well as line to compare against so this is case insensitive
    query = query.lower()

    # Split on spaces so we can search for each keyword
    query = query.split(" ")

    # List to store lines with positive hits
    hits = []

    # Search the file
    with open(infile, "r") as infile:
        for line in infile:
            line_flag = True
            for keyword in query:
                if keyword not in line.lower():
                    line_flag = False
            if line_flag:
                hits.append(line.strip())
    return hits


def extract_nodes(hits) -> dict:
    nodes = [hit.split(",")[0] for hit in hits]  # Parses out only the node name
    node_dict = dict(zip(nodes, hits))
    return node_dict


def extract_contigs(contigs: str, node_dict: dict, outdir: str) -> str:
    """
    Searches through a FASTA file and extracts only contigs that are in the provided node list
    :param contigs: FASTA file
    :param node_dict: Dictionary generated with extract_nodes()
    :param outdir: String path to output directory
    :return: String path to output FASTA
    """
    outname = os.path.join(outdir, "blastn_search_output.fasta")
    outfile = open(outname, "w")

    write_flag = False
    with open(os.path.abspath(contigs), 'r') as infile:
        for line in infile:
            if line.startswith(">"):
                for node, hit in node_dict.items():
                    if node in line:
                        outfile.write(">" + node.rsplit("_", 2)[0] + " " + "".join(hit.split(",")[1:3]) + "\n")
                        write_flag = True
                        break
                    else:
                        write_flag = False
            elif write_flag:
                outfile.write(line)
    outfile.close()
    return outname


if __name__ == "__main__":
    cli()
