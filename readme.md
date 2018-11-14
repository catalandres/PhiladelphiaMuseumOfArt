# Philadelphia Museum of Art Permanent Collection
## A comprehensive inventory of the art vaults of the PMA

[[https://github.com/username/repository/blob/master/img/PhiladelphiaMuseumOfArt.jpg | alt=Philadelphia Museum of Art]]

### Context

This dataset compiles all the data available through the Philadelphia Museum of Art's (PMA) [website](https://www.philamuseum.org) about the contents of its permanent collection.

### Contents

| Field | Description |
| --- | --- |
| `id` | Website identifier for the piece |
| `url` | URL for the piece's page in PMA's website |
| `title` | Name of the piece |
| `subtitle` | Further explanation, provides context for the piece |
| `author` | Name of the artist |
| `geography` | Geographic location of the creation of the piece |
| `date` | Time of the creation of the piece |
| `medium` | Material medium that expresses the piece |
| `dimensions` | Approximate dimensions of the piece |
| `copyright` | Current copyright conditions of the piece |
| `curatorial_department` | PMA department in charge of the piece |
| `location` | Whether and where the piece is on view at the museum |
| `accession_number` | Internal PMA identifier |
| `credit_line` | Description of how the piece joined PMA's permanent collection |

### Acknowledgements

Thanks to the Philadelphia Museum of Art for inspiring their visitors to discover the spirit of imagination that lies in everyone, and for connecting all Philadelphians from near and far with an outstanding art collection.

### Inspiration

Here are some questions you may want to answer:

* An analysis of all the works by geography
* A time series tracking how donations have evolved over time (`geography`, `medium`, etc.)
* An analysis of the content in the `credit_line` field:
    * Analyze the more frequent forms of donation
    * Carry out a social network analysis to determine the most influential donors
* A study of the different support media in the collection (`medium`)


### Copyright

The Philadelphia Museum of Art's copyright policy at the time of collecting this data states that (emphasis added):

> WEBSITE CONTENT IS PROTECTED BY LAW. The data, images, software, documentation, text, video, audio, and other information on the Websites (the "Materials") are proprietary to the Museum or its licensors or other third parties. The Museum retains all its rights, including copyright, in the Materials. Copyright and other proprietary rights may be held by individuals or entities other than, or in addition to, the Museum. Any unauthorized use of the Materials or the Trademarks (defined below), except as permitted by these terms and conditions, is strictly prohibited.
> 
> PERMITTED USE. **The Materials are made available for non-commercial, educational and personal use only or for "fair use" under the United States copyright laws. Users may download files for personal use, subject to any additional terms or restrictions applicable to the individual Materials. Users must properly cite the source of the Materials and the citations should include a link to www.philamuseum.org.** By downloading, printing, or using Materials from the Websites, whether accessed directly or indirectly, users agree that they will limit their use to the uses permitted by these terms and conditions or by fair use, and will not violate the Museum’s or any other party's proprietary rights. Users may not remove any copyright, trademark, or other proprietary notices and may not modify the Materials. Downloading, copying, distributing, or otherwise using Materials for any commercial purpose is strictly prohibited.

This dataset has been collected for the purposes of demonstrating the usage of web scraping techniques in Python and therefore falls under the case of non-commercial, educational and/or personal use.

Before you use this dataset, make sure you read carefully and understand the full text of PMA's [current copyright policy](https://www.philamuseum.org/copyright.html).

### Code

We have decoupled data collection (`PMA-download.py`) from dataset synthesizing (`PMA-synthesize.py`) to allow for separate testing. The download process can take several hours to complete. The code uses files on disk for backup purposes, so that the PMA's webserver will not be hit with redundant requests: once information about an artist or a work is collected, it should never be collected again, unless the corresponding local file is deleted.

Once the dataset is collected, is up to the user to delete any intermediate local files.

### Dataset

* The folder `results` contains the dataset in CSV format, broken down in chunks of 10K records for manageability.
* The folders `artists` and `works` contain the intermediate files corresponding to artists and works, respectively.