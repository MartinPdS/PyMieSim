"""
New Material Silver
===================
"""

# sphinx_gallery_thumbnail_path = '../images/Extra:New-Material-Silver.png'

def run(Plot, Save):
    from PyMieSim.Data._Material.utils import LoadOnlineSave
    from PyMieSim                      import Material

    LoadOnlineSave(filename='Silver', url='https://refractiveindex.info/data_csv.php?datafile=data/main/Ag/Johnson.yml')

    Mat = Material('Silver')

    if Plot:
        Mat.Plot()

    if Save:
        from pathlib import Path
        Mat.SaveFig(Path(__file__).stem)


if __name__ == '__main__':
    run(Plot=True, Save=False)
