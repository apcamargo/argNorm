"""Major script to run on command line"""

import argparse
from .normalize import normalize

def main():
    """
    Major function to run when running `argnorm` in shell.
    """
    parser = argparse.ArgumentParser(
        description=('argNorm normalizes ARG annotation results from '
                     'different tools and databases to the same ontology, '
                     'namely ARO (Antibiotic Resistance Ontology).'),
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('tool', type=str,
                        choices=['argsoap', 'abricate', 'deeparg', 'resfinder', 'amrfinderplus'],
                        help='The tool you used to do ARG annotation.')
    parser.add_argument('--db', type=str,
                        choices=['sarg', 'ncbi', 'resfinder', 'deeparg', 'megares', 'argannot'],
                        help='The database you used to do ARG annotation.')
    parser.add_argument('--mode', type=str,
                        choices=['reads', 'orfs', 'both'],
                        help='The mode you run the annotation tool.')
    parser.add_argument('--hamronized', action='store_true', help='Use this if the input is hamronized (processed using the hAMRonization tool)')
    parser.add_argument('-i', '--input', type=str, help='The annotation result you have')
    parser.add_argument('-o', '--output', type=str, help='The file to save normalization results')
    args = parser.parse_args()

    result = normalize(args.input,
            tool=args.tool,
            database=args.db,
            is_hamronized=args.hamronized,
            mode=args.mode)

    prop_unmapped = ((result.ARO == 'ARO:nan').sum() + result.ARO.isna().sum()) / result.shape[0]
    print(f'{round(1 - prop_unmapped, 3):.2%} args mapped.')
    result.to_csv(args.output, sep='\t')
