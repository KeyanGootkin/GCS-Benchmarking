# GCS-Benchmarking
> Creating a benchmark set of CME measurements for CME progation model validation

Coronal Mass Ejections (CMEs) are immense clouds of charged particles emitted from the sun. When a CME reaches Earth or a spacecraft, it can negatively affect power grids, electronics, radio communications and GPS.

Predicting where a CME will arrive and the severity of its impact can help offset these effects. Several models exist to simulate CME propagation thoughout the solar system, but there is currently no common set of simulation input parameters. This makes it challenging to determine whether a given model’s performance is due to its CME input parameters or its model settings.

To aid in solving this problem we have created eUCLID: the Universal CME modeL Input Dataset. This catalogue of historical CME parameter measurements is intended to be used as inputs to CME propagation models in validation efforts.


## Contents

### eUCLID.txt

A text file containing a pandas DataFrame containing average time, longitude, latitude, tilt angle, velocity, ascpect ratio, half angle, and time at 21.5 solar radii for historical CMEs. These parameters can be used as inputs into CME propagation models for validation purposes.

### gcs_analysis.py

A python script which creates/updates eUCLID. In addition, gcs_analysis.py will calculate the spread in measurements of the same CME and saves these results as histograms and scatterplots in a path named "figdir" which must be specified. This is useful in understanding the errors in the CME measurement process, and getting a sense of how accurate the measurements used are.

### carrots.txt

List of Carrington rotation start times, in seconds since the beginning of the unix epoch. Used for conversion from Carrington coordinates to Stonyhurst coordinates.


## Usage example

A few motivating and useful examples of how your product can be used. Spice this up with code blocks and potentially more screenshots.

_For more examples and usage, please refer to the [Wiki][wiki]._


## Authors

* Keyan Gootkin – Keyan.Gootkin@NASA.gov or goot1024@uw.edu – [@KeyanGootkin](https://twitter.com/KeyanGootkin) 

* M. Crawford - M.Crawford.Velez@gmail.com

* Rachel Broemmelsiek - rbroemme@terpmail.umd.edu

Distributed under the XYZ license. See ``LICENSE`` for more information.


<!-- Markdown link & img dfn's -->
[npm-image]: https://img.shields.io/npm/v/datadog-metrics.svg?style=flat-square
[npm-url]: https://npmjs.org/package/datadog-metrics
[npm-downloads]: https://img.shields.io/npm/dm/datadog-metrics.svg?style=flat-square
[travis-image]: https://img.shields.io/travis/dbader/node-datadog-metrics/master.svg?style=flat-square
[travis-url]: https://travis-ci.org/dbader/node-datadog-metrics
[wiki]: https://github.com/yourname/yourproject/wiki
