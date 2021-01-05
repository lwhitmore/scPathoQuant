from setuptools import setup, find_packages

setup(name="scViralQuant",
      version="1.0.0",
      description="The goal of this package is to accurately align and quantify viral reads for 10x single cell data. \
                   This software integrates viral counts and viral gene counts into 10x files (features.tsv.gz and matrix.mtx.gz \
                  in the filtered_feature_bc_matrix folder) so that softwares such as seurat can be used to analyze data",
      author=["Leanne Whitmore"],
      author_email=["leanne382@gmail.com"],
      platforms=["linux"],
      license="BSD 3 clause",
      url="https://github.com/sandialabs/RetSynth",
      keywords='single-cell, viral, quantification',
      test_suite="tests",
      packages=find_packages(),
      install_requires=[
          'argparse',
          'htseq', 
          'pandas'
      ],
      include_package_data=True,
      zip_safe=False,
      scripts=[
          'scviralquant.py',
      ]
)