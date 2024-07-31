This work replicates the geometry of the structure analysed in the paper ![Background Information of Deep Learning for Structural Engineering](https://www.researchgate.net/publication/318190131_Background_Information_of_Deep_Learning_for_Structural_Engineering).

The figure below shows a beam like 2D truss with 10 bars. The length of the bars are fixed, however the cross sectional areas are obtained through a random uniform sampling between $0.6$ $cm^2$ and $225.8$ $cm^2$. In total, 500 different structures were generated.

 ![](https://drive.google.com/uc?export=view&id=1xOuJYBWiWGkq5l_Z_hcAjYak_hjG26l5)

Then, the structure is loaded and analysed in the commercial FE software Abaqus. Since the dimensions in the structure are fixed, the input is the set of areas, while all nodal displacements and also bar stresses are computed as output.


## Data Loading and Manipulation

Upload the following files:
1. the dataset containing the areas, `areas.csv`;
2. displacements and reaction force along the time, `FinalResult.csv`;

To generate the data, we suggest to use the "student version" of the software [Abaqus](https://edu.3ds.com/en/software/abaqus-student-edition). The following files are available in the same [link](https://drive.google.com/drive/folders/1HYyx7BTRARnFPjQOHDklCtuB6la89mUM?usp=drive_link):
 1. To generate random areas `AreaGeneration.ipynb`. The output is `areas.csv`;
 2. Script to run in Abaqus to generate data `10_BarStructure.py`;
 3. Basic geometry to be called by the script mentioned in item 2 `Job-10-bar.inp`;
 4. Copy the file `extracted_data_DATA_HOUR.csv` as `FinalResult.csv` .

 **Important**

The script in item 02 automatically generates the bar geometry in Abaqus. If you want to assemble a geometry - at least once - in Abaqus, Prof Marcilio Alves has kindly prepared a tutorial for us, available at the [link](https://www.youtube.com/channel/UCEDn-UheEHKLfOKJKmSKzJw).


### Linear material model

The material characteristics are generic values for Aluminum alloy 6061, as listed below.

Property  | Value &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;    | Unity&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
---   | --- | ---
Mass density $\rho$ | $2.768\times  10^{-9}$ | $ton/mm^2$
Poisson $\nu$ | $0.35$ | -
Young's Modulus $E$| $68950$ | $MPa$
Yield stress $\sigma_{y0}$| $200$ | $MPa$

The material undergoes elastic deformation until it reaches the elastic limit defined by the yield stress. After the elastic limit, the material exhibits plastic behavior,that is, the material deforms irreversibly and does not return to its original shape and size, even when the load is removed. Initially, only elastic behaviour is considered.


