from pathlib import Path


def get_project_path() -> Path:
    return Path(__file__).parent.parent


def get_data_folder_path() -> Path:
    return Path(get_project_path(), 'data')


def get_tmp_folder_path() -> Path:
    """
    Return path to the temporary folder where different files can be stored
    """
    tmp_folder = Path(get_data_folder_path(), 'temp_storage')
    tmp_folder = tmp_folder.resolve()

    if tmp_folder.exists() is False:
        tmp_folder.mkdir(exist_ok=True, parents=True)

    return tmp_folder


def get_arbonaut_raster_path() -> Path:
    return Path(get_data_folder_path(), 'arbonaUT', 'Raster_data')


def get_arbonaut_vector_path() -> Path:
    return Path(get_data_folder_path(), 'arbonaUT', 'Vector_data')


def prepared_folder() -> Path:
    folder = Path(get_data_folder_path(), 'prepared')
    folder = folder.resolve()

    if folder.exists() is False:
        folder.mkdir(exist_ok=True, parents=True)

    return folder
