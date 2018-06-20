import setuptools
from BLASTn_Extract.blastn_extract import __version__, __author__, __email__

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="BLASTn_Extract",
    version=__version__,
    author=__author__,
    author_email=__email__,
    description="Internal BFSSI package for querying BLASTn results and filtering contig FASTA files",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/bfssi-forest-dussault/BLASTn_Extract",
    packages=setuptools.find_packages(),
    scripts=['BLASTn_Extract/blastn_extract.py'],
    install_requires=['click']
)
