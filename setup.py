import os
from setuptools import setup, find_packages

requirements = open(os.path.join(os.path.dirname(__file__), 'requirements.txt')).readlines()
setup(name="scPathoQuant",
      version="1.2.0",
      description="The goal of this package is to accurately align and quantify viral reads for 10x single cell data. \
                   This software integrates viral counts and viral gene counts into 10x files (features.tsv.gz and matrix.mtx.gz \
                  in the filtered_feature_bc_matrix folder) so that softwares such as seurat can be used to analyze data",
      author=["Leanne Whitmore"],
      author_email=["leanne382@gmail.com"],
      platforms=["linux"],
      keywords='single-cell, viral/pathogen, quantification',
      packages=find_packages(),
      install_requires=requirements,
      include_package_data=True,
      zip_safe=False,
      scripts=[
          'scpathoquant',
      ]
)
