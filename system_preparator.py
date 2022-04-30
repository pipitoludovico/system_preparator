import os
import sys

""" usage: system_preparator.py target_folder
    NOTE: the target folder must contain the receptor.psf and pdb and the ligand.psf and ligand.pdb 
    (ligand name doesn't matter).
    Make sure you name the receptor this way."""


def main():
    for subdir, dirs, files in os.walk(sys.argv[1]):
        for f in files:
            if f.endswith(".pdb") and f != "receptor.pdb":
                print(f)
                os.system(f"pdb_seg -X {f} > {f.replace('.pdb', '_segX.pdb')}")
                os.system(f"rm {f} | mv {f.replace('.pdb', '_segX.pdb')} {f}")
                sys_builder = ["package require psfgen\n"
                               "resetpsf\n"
                               f"readpsf receptor.psf\n"
                               f"readpsf {f.replace('.pdb', '')}.psf\n"
                               "coordpdb receptor.pdb\n"
                               f"coordpdb {f}\n"
                               "writepsf all.psf\n"
                               "writepdb all.pdb\n"
                               'puts "merging complete!!!"\n'
                               'quit']

                config_file = open(f"{sys.argv[1]}/structure_merger.tcl", "w")

                for line in sys_builder:
                    config_file.write(line)
                config_file.close()

                sys_prep = ["package require autoionize\n"
                            "package require solvate\n\n"
                            "solvate all.psf all.pdb -t 10 -o solvate\n"
                            "autoionize -psf solvate.psf -pdb solvate.pdb -o ionized -sc 0.154\n"
                            "quit"]

                sys_prep_inp = open(f"{sys.argv[1]}/solv_and_ionize.tcl", "w")

                for line in sys_prep:
                    sys_prep_inp.write(line)
                sys_prep_inp.close()

        os.chdir(f"{sys.argv[1]}")
        os.system("vmd -dispdev text -e structure_merger.tcl")
        os.system("vmd -dispdev text -e solv_and_ionize.tcl")
        os.system("rm all.*")
        os.system("rm *.tcl")
        os.system("rm solvate.*")


if __name__ == '__main__':
    main()
