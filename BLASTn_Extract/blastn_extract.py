#!/usr/bin/env python3

__version__ = "0.1.1"
__author__ = "Forest Dussault"
__email__ = "forest.dussault@canada.ca"

import os
import click
import logging

script = os.path.basename(__file__)
logging.basicConfig(
    format=f'\033[92m \033[1m {script}:\033[0m %(message)s ',
    level=logging.INFO)


def print_version(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    logging.info(f"Version: {__version__}")
    logging.info(f"Author: {__author__}")
    logging.info(f"Email: {__email__}")
    quit()


@click.command(help="This script will take an input query string and pull out all hits that match from a corresponding "
                    "BLASTn file. It will then extract all matching hits from an input contig FASTA file (if provided)."
                    ""
                    "Note that the BLASTn file should have the following outfmt format to be parsed correctly: "
                    "-outfmt '6 qseqid stitle slen length qstart qend pident score'")
@click.option('-i', '--infile',
              type=click.Path(exists=True),
              required=True,
              help='Path to the BLASTn file you wish to query.')
@click.option('-q', '--query',
              type=click.STRING,
              required=True,
              help='Query string to match against. Note that this is case insensitive.')
@click.option('-c', '--contigs',
              type=click.Path(exists=True),
              required=False,
              default=None,
              help='Path to the FASTA contig file to pull matches from.')
@click.option('-o', '--outfile',
              type=click.Path(exists=False),
              required=False,
              default=None,
              help='Path to the desired output file. If not specified, the output '
                   'will be stored in the same directory as the BLASTn file with a generic name.')
@click.option('-d', '--delimiter',
              type=click.STRING,
              default="\t",
              required=False,
              help='Delimiter used in your BLASTn file. Defaults to tab (\t) delimited. e.g. to change to comma '
                   'delimited use {--delimiter ","}')
@click.option('--version',
              help="Specify this flag to print the version and exit.",
              is_flag=True,
              is_eager=True,
              callback=print_version,
              expose_value=False)
def cli(infile: str, query: str, contigs: str, outfile: str, delimiter: str):
    if contigs is None:
        logging.info("No contig FASTA file provided. Only performing query on BLASTn file.")
        contig_flag = False
    else:
        contig_flag = True

    # Output file handling
    if outfile is None:
        outfile = os.path.join(os.path.dirname(infile), "BLASTn_search_output.fasta")

    # Run query against input file to generate hits
    hits = query_blastn(infile, query)

    if len(hits) == 0:
        logging.info(f"No hits found matching query '{query}'. Quitting.")
        quit()

    node_dict = extract_nodes(hits, delimiter)

    logging.info(f"Hits matching query '{query}':")
    for hit in hits:
        logging.info(hit)

    if contig_flag:
        logging.info(f"Extracting contigs from {contigs}")
        outfasta = extract_contigs(contigs, node_dict, outfile, delimiter)
        logging.info(f"Extracted contigs available at {outfasta}")


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


def extract_nodes(hits, delimiter) -> dict:
    nodes = [hit.split(delimiter)[0] for hit in hits]  # Parses out only the node name
    node_dict = dict(zip(nodes, hits))
    return node_dict


def extract_contigs(contigs: str, node_dict: dict, outfile: str, delimiter: str) -> str:
    """
    Searches through a FASTA file and extracts only contigs that are in the provided node list
    :param contigs: FASTA file
    :param node_dict: Dictionary generated with extract_nodes()
    :param outfile: String path to output file
    :param delimiter: String delimiter to split BLASTn file on (defaults to tab)
    :return: String path to output FASTA
    """
    outfile_ = open(outfile, "w")

    write_flag = False
    with open(os.path.abspath(contigs), 'r') as infile:
        for line in infile:
            if line.startswith(">"):
                for node, hit in node_dict.items():
                    if node in line:
                        outfile_.write(">" + node.rsplit("_", 2)[0] + " " + "".join(hit.split(delimiter)[1:3]) + "\n")
                        write_flag = True
                        break
                    else:
                        write_flag = False
            elif write_flag:
                outfile_.write(line)
        outfile_.close()
    return outfile


if __name__ == "__main__":
    cli()
