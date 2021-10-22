Feature Linking
===============

The pyOpenMS feature grouping algorithms group corresponding features from multiple ``FeatureMap`` objects into a ``ConsensusMap``.
Before feature linking, a map alignment is advisable.

Different feature grouping algorithms are available in pyOpenMS:

- FeatureGroupingAlgorithmQT
- FeatureGroupingAlgorithmKD
- FeatureGroupingAlgorithm
- FeatureGroupingAlgorithmLabeled
- FeatureGroupingAlgorithmUnlabeled

To perform feature linking we can employ the algorithm FeatureGroupingAlgorithmQT.

Download Example Data
*********************

.. code-block:: python

    from pyopenms import *
    from urllib.request import urlretrieve

    base_url = 'https://raw.githubusercontent.com/OpenMS/pyopenms-extra/master/src/data/'

    feature_files = ['BSA1_F1.featureXML', 'BSA2_F1.featureXML', 'BSA3_F1.featureXML']

    feature_maps = []

    # download the feature files and store feature maps in list (feature_maps)
    for feature_file in feature_files:
        urlretrieve (base_url + feature_file, feature_file)
        feature_map = FeatureMap()
        FeatureXMLFile().load(feature_file, feature_map)
        feature_maps.append(feature_map)

Feature Linking Algorithm
*************************

All ``FeatureMap`` objects will be combined in a ``ConsensusMap``.

.. code-block:: python

    feature_grouper = FeatureGroupingAlgorithmQT()

    consensus_map = ConsensusMap()

    file_descriptions = consensus_map.getColumnHeaders()

    for i, feature_map in enumerate(feature_maps):
        file_description = file_descriptions.get(i, ColumnHeader())
        file_description.filename = feature_map.getMetaValue('spectra_data')[0].decode()
        file_description.size = feature_map.size()
        file_description.unique_id = feature_map.getUniqueId()
        file_descriptions[i] = file_description

    consensus_map.setColumnHeaders(file_descriptions)
    feature_grouper.group(feature_maps, consensus_map)