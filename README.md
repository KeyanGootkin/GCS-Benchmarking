# GCS-Benchmarking
> Creating a benchmark set of CME measurements for CME progation model validation

Coronal Mass Ejections (CMEs) are immense clouds of charged particles emitted from the sun. When a CME reaches Earth or a spacecraft, it can negatively affect power grids, electronics, radio communications and GPS.

Predicting where a CME will arrive and the severity of its impact can help offset these effects. Several models exist to simulate CME propagation thoughout the solar system, but there is currently no common set of simulation input parameters. This makes it challenging to determine whether a given model’s performance is due to its CME input parameters or its model settings.

To aid in solving this problem we have created eUCLID: the Universal CME modeL Input Dataset. This catalogue of historical CME parameter measurements is intended to be used as inputs to CME propagation models in validation efforts.


## Contents

#### eUCLID.txt

A text file containing a pandas DataFrame containing average time, longitude, latitude, tilt angle, velocity, ascpect ratio, half angle, and time at 21.5 solar radii for historical CMEs. These parameters can be used as inputs into CME propagation models for validation purposes.

#### croissant.py

A python module which contains all of the functions used in the repository. Import croissant as such for style consistency: ```import croissant as cr```

#### gcs_analysis.py

A python script which creates/updates eUCLID. In addition, gcs_analysis.py will calculate the spread in measurements of the same CME and saves these results as histograms and scatterplots in a path named "figdir" which must be specified. This is useful in understanding the errors in the CME measurement process, and getting a sense of how accurate the measurements used are.

#### carrots.txt

List of Carrington rotation start times, in seconds since the beginning of the unix epoch. Used for conversion from Carrington coordinates to Stonyhurst coordinates.

#### data 

A series of folders containing GCS output files. gcs_analysis.py draws from these folders to create eUCLID. 


## Usage

### Model Validation

For model validation purposes the most important file is eUCLID.txt. The contents of that table will serve as the inputs for CME propogation models. _Note_: Half angle in eUCLID is not the same as half width. Half angle is a quality as described in this [paper by A. Thernisien](http://iopscience.iop.org/article/10.1088/0067-0049/194/2/33/meta). Half width can be calculated using half angle and ratio.

### CME Measurement

This repository could also be used to analyze other GCS measurements of CMEs. To do this download croissant.py and recreate the file structure in the data folder. Use make_eUCLID() from croissant to create a pandas DataFrame containing the averaged measurements of each CME.

## Authors

Please send any questions or comments regarding the code in this repository to Keyan Gootkin.

* Keyan Gootkin – Keyan.Gootkin@NASA.gov or goot1024@uw.edu – Twitter: [@KeyanGootkin](https://twitter.com/KeyanGootkin) 

* M. Crawford - m.crawford.velez@gmail.com

* Rachel Broemmelsiek - rbroemme@terpmail.umd.edu

* Austin Skipper - skippera22@mail.wlu.edu

* Jinkoo Yim - jinkooyim@gmail.com



Distributed under the MIT license. See ``LICENSE.txt`` for more information.


<!-- Markdown link & img dfn's -->
[npm-image]: https://img.shields.io/npm/v/datadog-metrics.svg?style=flat-square
[npm-url]: https://npmjs.org/package/datadog-metrics
[npm-downloads]: https://img.shields.io/npm/dm/datadog-metrics.svg?style=flat-square
[travis-image]: https://img.shields.io/travis/dbader/node-datadog-metrics/master.svg?style=flat-square
[travis-url]: https://travis-ci.org/dbader/node-datadog-metrics
[wiki]: https://github.com/yourname/yourproject/wiki
