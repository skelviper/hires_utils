import argparse
import clean_leg
import clean_splicing
import clean_isolated
#import script
import pairsa
import sep_clean
from align import align_main

def cli():
    parser = argparse.ArgumentParser(prog="hires", description="Functions for hires pipline")
    subcommands = parser.add_subparsers(title="These are sub-commands",metavar="command")
#--------- clean_leg sub command ---
    clean_leg_arg = subcommands.add_parser(
                            "clean_leg",
                            help="clean promiscuous legs that contacts with multiple legs")
    clean_leg_arg.set_defaults(handle=clean_leg.cli)
    clean_leg_arg.add_argument(
                            dest="filename",
                            metavar="INPUT_FILE",
                            nargs=1)
    clean_leg_arg.add_argument(
                            "-t", "--thread",
                            type=int,
                            dest="thread",
                            action="store",
                            default=4,
                            help="set thread number")
    clean_leg_arg.add_argument(
                            "-d","--distance",
                            dest="max_distance",
                            metavar="MAX_DISTANCE",
                            type=int,
                            action="store",
                            default=1000,
                            help="max distance to calculate adjacent legs"
    )
    clean_leg_arg.add_argument(
                            "-n","--count",
                            metavar="MAX_COUNT",
                            dest="max_count",
                            type=int,
                            action="store",
                            default=10,
                            help="number threshold of adjacent legs"
    )                   
    clean_leg_arg.add_argument("-o", "--output", 
                            dest="out_name", action="store",
                            metavar="OUTPUT_FILE",
                            required=True,
                            help="set output file name")
 # ---------#clean_splicing sub command ---
    clean_splicing_arg = subcommands.add_parser(
                            "clean_splicing", 
                            help="clean exon splicing from mRNA in contact file")
    clean_splicing_arg.set_defaults(handle=clean_splicing.cli)
    clean_splicing_arg.add_argument(
                            dest="filename",
                            metavar="INPUT_FILE",
                            help="input filename",
                            nargs=1)     
    clean_splicing_arg.add_argument(
                            "-r", "--reference", 
                            dest="gtf_filename",
                            type = str,
                            action="store", 
                            help="annotation gtf file", 
                            required=True)
    clean_splicing_arg.add_argument(
                            "-o", "--output", 
                            dest="out_name",
                            metavar="OUTPUT_FILE",
                            required=True, 
                            help="output file name", 
                            action="store")
    clean_splicing_arg.add_argument(
                            "-t", "--thread",
                            type=int,
                            dest="num_thread",
                            action="store",
                            default=4,
                            help="set thread number")
    
#--------- align subcommand ------
    align = subcommands.add_parser(
                            "align",
                            help="caculate rmsd between .3dg replicates, print to stdout"
    )
    align.set_defaults(handle=align_main)
    align.add_argument(
                            dest="filenames",
                            metavar="INPUT_FILE",
                            help="input filename",
                            nargs="*"
    )
    align.add_argument(
                            "-o","--output_dir",
                            dest="output_dir",
                            type=str,
                            help="directory to store aligned 3dg file and rmsd info file",
                            required=True
    )
    align.add_argument(
        "-gd", "--good_dir",
        dest="good_dir",
        help="output directory for good(low rmsd) structure.",
        required=True
    )
    align.add_argument(
        "-bd", "--bad_dir",
        dest="bad_dir",
        help="output directory for bad(causing high rmsd) structure.",
        required=True
    )
#--------- clean_isolate subcommand ------
    clean_isolated_arg = subcommands.add_parser(
                            "clean_isolated",
                            help="remove isolated contacts according to L-0.5 distance"
    )
    clean_isolated_arg.set_defaults(handle=clean_isolated.cli)
    clean_isolated_arg.add_argument(
                            dest="filename",
                            metavar="INPUT_FILE",
                            help="input filename",
                            nargs=1
    )
    clean_isolated_arg.add_argument(
                            "-t","--thread",
                            dest="thread",
                            type=int,
                            help="set thread number",
                            default=4
    )     
    clean_isolated_arg.add_argument(
                            "-m","--dense",
                            dest="dense",
                            type=int,
                            help="number of contacts in proximity",
                            default=5)
    clean_isolated_arg.add_argument(
                            "-d","--distance",
                            dest="distance",
                            type=int,
                            help="check contacts in what L-0.5 range",
                            default=10000000) 
    clean_isolated_arg.add_argument(
                            "-o","--output",
                            dest="output_file",
                            action="store",
                            metavar="OUTPUT_FILE",
                            required=True,
                            help = "output file name",
                            type=str
    )
# --------- pairsa subcommand ------
    pairsa_arg = subcommands.add_parser(
        "pairsa",
        help = "transform .pairs to user-defined pairs-like file formats. e.g. validPairs."
    )
    pairsa_arg.set_defaults(handle=pairsa.cli)
    pairsa_arg.add_argument(
        "--input",
        dest="input_file",
        help="input file path",
        required=True
    )
    pairsa_arg.add_argument(
        "--target",
        dest="target",
        help="a blank seperated string giving out target format\n\
            must have 'chr_a' 'chr_b' 'cord_a' 'cord_b'\n\
                the position of the column name in this 'target string' will be the position of that column\n\
                e.g. 'id chr_a cord_a strand_a chr_b cord_b strand_b restriction_distance'\n\
                    defined the validPairs format from HiCPro and Juicer.",
        action="store",
        required=True
    )
    pairsa_arg.add_argument(
        "--output",
        dest="output_file",
        help="output file path",
        action="store",
        required=True
    )
# --------- sep_clean subcommand ---------
    sep_clean_arg = subcommands.add_parser(
                            "sep_clean",
                            help = "seperate homologous chromosome(add (mat)/(pat) for chra chrb colomns), clean isolated contacts again. \
                                generate one more hickit compatible output file.\
                                    works with hickit imputed pairs file"
    )
    sep_clean_arg.set_defaults(handle=sep_clean.cli)
    sep_clean_arg.add_argument(
                            dest="filename",
                            metavar="INPUT_FILE",
                            help="input filename",
                            nargs=1
    )
    sep_clean_arg.add_argument(
                            "-n", "--num_thread",
                            dest="num_thread",
                            help="number of thread use",
                            default="4"
    )
    sep_clean_arg.add_argument(
                            "-o1", "--output1",
                            dest="output_file1",
                            help="output file path for .dip.pairs (the chra(mat) format) file",
                            action="store",
                            required=True
    )
    sep_clean_arg.add_argument(
                            "-o2", "--output2",
                            dest="output_file2",
                            help="output file path for .pairs (the hickit -b default format) file",
                            required=True
    )
    sep_clean_arg.add_argument(
                            "-m","--dense",
                            dest="dense",
                            type=int,
                            help="number of contacts in proximity",
                            default=5
    )
    sep_clean_arg.add_argument(
                            "-d","--distance",
                            dest="distance",
                            type=int,
                            help="check contacts in what L-0.5 range",
                            default=10000000
    ) 

    args = parser.parse_args()
    #print(args.replace_switch)
    #print(args.out_name)
    #print(args.filenames)
    if hasattr(args, "handle"):
        args.handle(args)
    else:
        parser.print_help()
if __name__ == "__main__":
    cli()