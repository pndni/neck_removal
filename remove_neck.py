import sys
from pathlib import Path
from nipype.pipeline import engine as pe
from nipype.interfaces import Function
import argparse
from pndniworkflows.preprocessing import neck_removal_wf
from pndniworkflows.interfaces.io import ExportFile


def copy(infile, outfile):
    import shutil
    shutil.copy(infile, outfile)
    return outfile


def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('infile', type=str)
    parser.add_argument('outfile', type=str)
    parser.add_argument('model', type=str,
                        help='File name of model to use.')
    parser.add_argument('--working_directory', type=str)
    parser.add_argument('--limits', nargs=3, type=float,
                        default=[90.0, 110.0, -105.0],
                        metavar='LIMIT',
                        help='x, y, and z (RAS) points to determine cutting plane. '
                             'Four points (+/- x, +/- y, z) will be transformed from '
                             'model space to native space. The cutting plane will be '
                             'chosen to line up in native voxel coordinates and include '
                             'each point (or possibly cut exactly through one).')
    return parser


if __name__ == '__main__':
    args = get_parser().parse_args()
    neck_rm = neck_removal_wf(True)
    wf = pe.Workflow('wrapper')
    if args.working_directory is not None:
        wf.base_dir = args.working_directory
    neck_rm.inputs.inputspec.T1 = Path(args.infile).resolve()
    neck_rm.inputs.inputspec.model = Path(args.model).resolve()
    neck_rm.inputs.inputspec.limits = args.limits
    write = pe.Node(ExportFile(check_extension=True, clobber=True), 'write')
    write.inputs.out_file = str(Path(args.outfile).resolve())
    wf.connect(neck_rm, 'outputspec.cropped', write, 'in_file')
    wf.run()
