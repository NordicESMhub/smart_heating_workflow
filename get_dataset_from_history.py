"""Python program to download tabular filename from galaxy history
"""

from bioblend import galaxy
import click
import sys

@click.command()
@click.option("--galaxy-server", required=True, help="Galaxy url")
@click.option("--galaxy-user-key", required=True, help="Galaxy User API KEY")
@click.option("--tags", required=True, help="tags to search history.")
@click.option("--dataset-name", required=True, help="name of the dataset to find")
def main(galaxy_server, galaxy_user_key, tags, dataset_name):
    gi = galaxy.GalaxyInstance(url=galaxy_server, key=galaxy_user_key)
    print(tags)
    tag_carrying_histories = gi.histories._get(params={'q': ['tag'], 'qv': tags.split(',')})
    if tag_carrying_histories:
        sys.stdout.write(tag_carrying_histories[0]['id'])

        history_datasets_info = gi.histories.show_history(
            history_id=tag_carrying_histories[0]['id'], contents=True
        )

        for ds in history_datasets_info:
            if ds['name'] == dataset_name:
                # download dataset
                print(ds['id'], ds['name'])
                datasets = gi.datasets.download_dataset(ds['id'],
                                                    file_path='./'+ ds['name'].replace(' ', '_'),
                                                    use_default_filename=False,
                                                    maxwait=5)



if __name__ == "__main__":
    print("jhe")
    main()
