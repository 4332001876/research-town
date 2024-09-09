import os
import datetime
import json

import sys  
sys.path.append(os.path.abspath('..'))

from beartype.typing import Literal

from research_town.configs import Config
from research_town.dbs import AgentProfileDB, EnvLogDB, PaperProfileDB, ProgressDB
from research_town.engines import LifecycleResearchEngine


Role = Literal['reviewer', 'proj_leader', 'proj_participant', 'chair'] | None


def run_sync_experiment(
    exp_settings_path: str,
    config_file_path: str,
    save_file_path: str,
) -> None:
    exp_settings = json.load(open(exp_settings_path, 'r'))
    print('Experiment settings:')
    print(exp_settings)
    
    agent_names = exp_settings['agent_names']
    # if save path exists, then load
    config = Config(config_file_path)
    agent_db = AgentProfileDB()
    paper_db = PaperProfileDB()
    if os.path.exists(save_file_path):
        agent_db.load_from_json(save_file_path, with_embed=True)
        paper_db.load_from_json(save_file_path, with_embed=True)
    else:
        agent_db.pull_agents(agent_names=agent_names, config=config)
        paper_db.pull_papers(num=10, domain=exp_settings['domain'])

    env_db = EnvLogDB()
    progress_db = ProgressDB()
    engine = LifecycleResearchEngine(
        project_name='research_town_demo',
        agent_db=agent_db,
        paper_db=paper_db,
        progress_db=progress_db,
        env_db=env_db,
        config=config,
    )
    engine.run(task=exp_settings['task'])
    engine.save(save_file_path=save_file_path, with_embed=True)
    return


def main() -> None:
    formatted_time = str(datetime.datetime.now().strftime('%Y%m%d_%H%M%S'))
    run_sync_experiment(
        exp_settings_path='./exp_settings/exp.json',
        config_file_path='../configs/default_config.yaml',
        save_file_path='./research_town_demo_log_' + formatted_time, # 当前时间命名
    )


if __name__ == '__main__':
    main()
