def RunFileWriter(MESS_New_Name):
    
    Run_File = open("MESS_SHfile.sh", 'w')
    run_shell_script = f"""#!/bin/bash
#SBATCH --partition=amilan
#SBATCH --qos=normal
#SBATCH --nodes=1
#SBATCH --ntasks=4
#SBATCH --time=00:30:00
#SBATCH --job-name=MESS_{MESS_New_Name}
#SBATCH --account=ucb273_peak2
#SBATCH --mail-type=ALL
#SBATCH --mail-user=prsh1291@colorado.edu

module purge
module use /projects/nila3952/public/modules
module load miniconda
source activate mess-env
mess {MESS_New_Name}
    """
    Run_File.writelines(run_shell_script)
    Run_File.close()