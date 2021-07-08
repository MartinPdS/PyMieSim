"""
New Material BK7
================
"""

# sphinx_gallery_thumbnail_path = '../images/Extra:New-Material-BK7.png'

def run(Plot, Save):
    from PyMieSim.Data._Material.utils import LoadOnlineSave
    from PyMieSim                      import Material

    LoadOnlineSave(filename='BK7', url='https://refractiveindex.info/data_csv.php?datafile=data/glass/schott/N-BK7.yml')

    Mat = Material('BK7')

    if Plot:
        Mat.Plot()

    if Save:
        from pathlib import Path
        Mat.SaveFig(Path(__file__).stem)


if __name__ == '__main__':
    run(Plot=True, Save=False)
