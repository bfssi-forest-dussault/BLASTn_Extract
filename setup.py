import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="BLASTn_Extract",
    version="0.0.5",
    author="Forest Dussault",
    author_email="forest.dussault@canada.ca",
    description="Internal BFSSI package for querying BLASTn results and filtering contig FASTA files",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/bfssi-forest-dussault/BLASTn_Extract",
    packages=setuptools.find_packages(),
    scripts=['BLASTn_Extract/blastn_extract.py'],
    install_requires=['click']  # list all dependencies here
)
