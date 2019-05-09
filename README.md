# Collect SEGY files from National Geoscience Data Centre

https://www.bgs.ac.uk/services/ngdc/accessions/ - NGDC Accessions service contains some amount of SEGY format seismic data available under the UK Open Government License.

This repository contains a hardcoded list of dataset IDs which contain .sgy files as of writing (this information isn't searchable via the existing API), a script to create downloadable URLs for those files via the Accessions API hosted by the British Geological Survey.

  1. https://en.wikipedia.org/wiki/Open_Government_Licence - The OGL permits anyone to copy, publish, distribute, transmit and adapt the licensed work
  2. https://www.bgs.ac.uk/services/ngdc/accessions/ - National Geoscience Data Centre is recognised as the NERC Environmental Data Centre for geoscience data.
  3. https://github.com/equinor/segyio - Segyio is a small LGPL licensed C library for easy interaction with SEG-Y and Seismic Unix formatted seismic data, with language bindings for Python and Matlab 
