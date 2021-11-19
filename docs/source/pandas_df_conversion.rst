Export to pandas DataFrame
==========================

In pyOpenMS some data structures can be converted to a tabular format as a ``pandas.DataFrame``. This allows convenient access to data and meta values of spectra, features and identifications.

Required imports for the examples:

.. code-block:: python

    from pyopenms import *
    from urllib.request import urlretrieve
    url = 'https://raw.githubusercontent.com/OpenMS/pyopenms-extra/master/src/data/'

MSExperiment
************

**pyopenms.MSExperiment.get_df(** *long=False* **)**
        Generates a pandas DataFrame with all peaks in the MSExperiment

        **Parameters:**

        **long :** default False
        
        set to True if you want to have a long/expanded/melted dataframe with one row per peak. Faster but
        replicated RT information. If False, returns rows in the style: rt, np.array(mz), np.array(int)
        
        **Returns:**

        **pandas.DataFrame** 
        
        peak map information stored in a DataFrame

**Examples:**

.. code-block:: python

    urlretrieve(url+'BSA1.mzML', 'BSA1.mzML')
    exp = MSExperiment()
    MzMLFile().load('BSA1.mzML', exp)

    df = exp.get_df() # default: long = False
    df.head(2)
    
.. csv-table:: exp.get_df()
   :widths: 2 10 50 50
   :header: ,"RT", "mzarray", "intarray"

   "0",	"1501.41394", "[300.0897645621494, 300.18132740129533, 300.20...",	"[3431.0261, 1181.809, 1516.1746, 1719.8547, 11..."
   "1", "1503.03125", "[300.06577092599525, 300.08932376441896, 300.2...",	"[914.79034, 1842.2311, 2395.1025, 851.4738, 16..." 


.. code-block:: python

    df = exp.get_df(long=True)
    df.head(2)

.. csv-table:: exp.get_df(long=True)
   :widths: 2 20 20 20
   :header: , "RT",	"mz", "inty"

   "0", "1501.41394", "300.089752",	"3431.026123"
   "1",	"1501.41394",	"300.181335",	"1181.808960"

FeatureMap
**********

**pyopenms.FeatureMap.get_df(** *meta_values = None* **)**
        Generates a pandas DataFrame with information contained in the FeatureMap.

        **Parameters:**

        **meta_values :** default None
        
        meta values to include (None, [custom list of meta value names] or 'all')
        
        **Returns:**

        **pandas.DataFrame** 
        
        feature information stored in a DataFrame

**Examples:**

.. code-block:: python

    urlretrieve(url+'BSA1_F1.featureXML', 'BSA1_F1.featureXML')
    feature_map = FeatureMap()
    FeatureXMLFile().load('BSA1_F1.featureXML', feature_map)

    df = feature_map.get_df() # default: meta_values = None
    df.head(2)
    
.. csv-table:: feature_map.get_df()
   :widths: 2 20 5 20 20 20 20 20 20 20 20
   :header: 	, "sequence",	"charge",	"RT",	"mz",	"RTstart",	"RTend",	"mzstart",	"mzend",	"quality",	"intensity"
            "id"

   "9650885788371886430",	"None",	"2",	"1942.600083",	"395.239277",	"1932.484009",	"1950.834351",	"395.239199",	"397.245758",	"0.808494",	"157572000.0"
   "18416216708636999474",	"None",	"2",	"1749.138335",	"443.711224",	"1735.693115",	"1763.343506",	"443.71112",	"445.717531",	"0.893553",	"54069300.0"


.. code-block:: python

    df = feature_map.get_df(meta_values = 'all')
    df.head(2)

.. csv-table:: feature_map.get_df(meta_values = 'all')
   :widths: 2 20 5 20 20 20 20 20 20 20 20 20 20 20 20 20 20
   :header: 	, "sequence",	"charge",	"RT",	"mz",	"RTstart",	"RTend",	"mzstart",	"mzend",	"quality",	"intensity", "FWHM", "spectrum_index", "spectrum_native_id", "label", "score_correlation",	"score_fit"
            "id"

   "9650885788371886430",	"None",	"2",	"1942.600083",	"395.239277",	"1932.484009",	"1950.834351",	"395.239199",	"397.245758",	"0.808494",	"157572000.0", "10.061090",	"259",	"spectrum=1270",	"168",	"0.989969",	"0.660286"
   "18416216708636999474",	"None",	"2",	"1749.138335",	"443.711224",	"1735.693115",	"1763.343506",	"443.71112",	"445.717531",	"0.893553",	"54069300.0", "14.156094",	"156",	"spectrum=1167",	"169",	"0.999002",	"0.799234"

.. code-block:: python

    df = feature_map.get_df(meta_values = [b'FWHM', b'label'])
    df.head(2)

.. csv-table:: feature_map.get_df(meta_values = [b'FWHM', b'label'])
   :widths: 2 20 5 20 20 20 20 20 20 20 20 20 20
   :header: 	, "sequence",	"charge",	"RT",	"mz",	"RTstart",	"RTend",	"mzstart",	"mzend",	"quality",	"intensity", "FWHM", "label"
            "id"

   "9650885788371886430",	"None",	"2",	"1942.600083",	"395.239277",	"1932.484009",	"1950.834351",	"395.239199",	"397.245758",	"0.808494",	"157572000.0", "10.061090", "168"
   "18416216708636999474",	"None",	"2",	"1749.138335",	"443.711224",	"1735.693115",	"1763.343506",	"443.71112",	"445.717531",	"0.893553",	"54069300.0", "14.156094",	"169"

ConsensusMap
************

**pyopenms.ConsensusMap.get_df()**
        Generates a pandas DataFrame with both consensus feature meta data and intensities from each sample.

        **Returns:**

        **pandas.DataFrame** 
        
        consensus map meta data and intensity stored in pandas DataFrame

**pyopenms.ConsensusMap.get_intensity_df()**
        Generates a pandas DataFrame with feature intensities from each sample in long format (over files).
        For labelled analyses channel intensities will be in one row, therefore resulting in a semi-long/block format.
        Resulting DataFrame can be joined with result from get_metadata_df by their index 'id'.

        **Returns:**

        **pandas.DataFrame** 
        
        intensity DataFrame

**pyopenms.ConsensusMap.get_metadata_df()**
        Generates a pandas DataFrame with feature meta data (sequence, charge, mz, RT, quality).
        Resulting DataFrame can be joined with result from get_intensity_df by their index 'id'.

        **Returns:**

        **pandas.DataFrame** 
        
        DataFrame with metadata for each feature (such as: best identified sequence, charge, centroid RT/mz, fitting quality)

**Examples:**

.. code-block:: python

    urlretrieve(url+'ConsensusXMLFile_1.consensusXML', 'ConsensusXMLFile_1.consensusXML')
    consensus_map = ConsensusMap()
    ConsensusXMLFile().load('ConsensusXMLFile_1.consensusXML', consensus_map)

    df = consensus_map.get_df()
    df.head(2)
    
.. csv-table:: consensus_map.get_df()
   :widths: 2 10 20 20 20 20 30 30
   :header:     , "sequence",	"charge",	"RT",	"mz",	"quality",	"data/MapAlignmentFeatureMap1.xml",	"data/MapAlignmentFeatureMap2.xml"
            "id"

   "0",	"A",	"0",	"1273.27",	"904.470",	"1.1",	"31253900.0",	"0.0"
   "1",	"E",	"0",	"1248.33",	"897.449",	"1.2",	"25917900.0",	"25917900.0"

.. code-block:: python

    df = consensus_map.get_intensity_df()
    df.head(2)

.. csv-table:: consensus_map.get_intensity_df()
   :widths: 2 30 30
   :header:     , "data/MapAlignmentFeatureMap1.xml",	"data/MapAlignmentFeatureMap2.xml"
            "id"

   "0",	"31253900.0",	"0.0"
   "1",	"25917900.0",	"25917900.0"

.. code-block:: python

    df = consensus_map.get_metadata_df()
    df.head(2)

.. csv-table:: consensus_map.get_metadata_df()
   :widths: 2 10 20 20 20 20
   :header:     , "sequence",	"charge",	"RT",	"mz",	"quality"
            "id"

   "0",	"A",	"0",	"1273.27",	"904.470",	"1.1"
   "1",	"E",	"0",	"1248.33",	"897.449",	"1.2"

PeptideIdentifications
**********************

**pyopenms.peptide_identifications_to_df( peps**, *decode_ontology=True*, *default_missing_values={bool: False, int: -9999, float: np.nan, str: ''}*, *export_unidentified=True* **)**
        Generates a pandas DataFrame with all peaks in the MSExperiment

        **Parameters:**

        **peps :** 
        
        list of PeptideIdentification objects

        **decode_ontology :** default True
        
        if meta values contain CV identifer (e.g., from PSI-MS) they will be automatically decoded into the human readable CV term name.

        **default_missing_values :** default {bool: False, int: -9999, float: np.nan, str: ''}
        
        default value for missing values for each data type

        **export_unidentified :** default True
        
        export PeptideIdentifications without PeptideHit
        
        **Returns:**

        **pandas.DataFrame** 
        
        peptide identifications in a DataFrame

**Examples:**

.. code-block:: python

    urlretrieve(url+'small.idXML', 'small.idXML')
    prot_ids = []
    pep_ids = []
    IdXMLFile().load('small.idXML', prot_ids, pep_ids)

    df = peptide_identifications_to_df(pep_ids)
    df.head(2)
    
.. csv-table:: peptide_identifications_to_df(pep_ids)
   :widths: 2 20 10 20 20 10 20 20 20 20 20 20 20 20 20 20
   :header: , "id",	"RT",	"mz",	"q-value",	"charge",	"protein_accession",	"start",	"end",	"NuXL:z2 mass",	"NuXL:z3 mass",	"...", "isotope_error",	"NuXL:peptide_mass_z0",	"NuXL:XL_U",	"NuXL:sequence_score"

    "0",	"OpenNuXL_2019-12-04T16:39:43_1021782429466859437",	"900.425415",	"414.730865",	"0.368649",	"4",	"DECOY_sp|Q86UQ0|ZN589_HUMAN",	"255",	"267",	"828.458069",	"552.641113",	"...", "0",	"1654.901611",	"0",	"0.173912"
    "1",	"OpenNuXL_2019-12-04T16:39:43_7293634134684008928",	"903.565186",	"506.259521",	"0.422779",	"2",	"sp|P61313|RL15_HUMAN",	"179",	"187",	"0.0",	"0.0",	"...", "0",	"1010.504639",	"0",	"0.290786"
