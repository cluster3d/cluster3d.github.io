import os

project_dir = '/scratch/yk1962/ABC2'
data_dir_relative = 'data'
result_dir_relative = 'result'
code_dir_relative = 'code'
output_dir_relative = 'output'
sbatch_dir_relative = 'job_request'
activate_dir = '/scratch/yk1962/miniconda3/bin/activate'
env_name = 'pytorch3d'

data_dir = os.path.join(project_dir, data_dir_relative)
result_dir = os.path.join(project_dir, result_dir_relative)
code_dir = os.path.join(project_dir, code_dir_relative)
output_dir = os.path.join(project_dir, output_dir_relative)
sbatch_dir = os.path.join(project_dir, sbatch_dir_relative)

activate_env_command = '{} {}'.format(activate_dir, env_name)
