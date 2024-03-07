from pathlib import Path


def get_project_path() -> Path:
    return Path(__file__).parent.parent


def get_tmp_folder_path() -> Path:
    """
    Return path to the temporary folder where different files can be stored
    """
    tmp_folder = Path(get_project_path(), 'data', 'temp_storage')
    tmp_folder = tmp_folder.resolve()

    if tmp_folder.exists() is False:
        tmp_folder.mkdir(exist_ok=True, parents=True)

    return tmp_folder
