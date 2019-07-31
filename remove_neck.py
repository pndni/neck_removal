from pndniworkflows.preprocessing import neck_removal_wf
import sys
from pathlib import Path
from nipype.pipeline import engine as pe
from nipype.interfaces import Function


def copy(infile, outfile):
    import shutil
    shutil.copy(infile, outfile)
    return outfile


if __name__ == '__main__':
    infile = sys.argv[1]
    outfile = sys.argv[2]
    model = sys.argv[3]
    wd = sys.argv[4]
    neck_rm = neck_removal_wf()
    wf = pe.Workflow('wrapper')
    wf.base_dir = wd
    neck_rm.inputs.inputspec.T1 = str(Path(infile).resolve())
    neck_rm.inputs.inputspec.model = str(Path(model).resolve())
    neck_rm.inputs.inputspec.limits = [90.0, 110.0, -85.0]
    write = pe.Node(Function(input_names=['infile', 'outfile'], output_names=['outfile'], function=copy), 'write')
    write.inputs.outfile = str(Path(outfile).resolve())
    wf.connect(neck_rm, 'outputspec.noneck', write, 'infile')
    wf.run()
