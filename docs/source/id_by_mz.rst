Identification by Accurate Mass
===============================
Example workflow for the processing of a set of mzML files (defined in the ``files`` variable) including centroiding,
feature detection, feature linking and accurate mass search.
The resulting data gets processed in a pandas data frame with feature filtering (missing values, quality) and imputation
of remaining missing values.
Compounds detected during accurate mass search will be annoted in the resulting dataframe.

User Input
**********
Important: 
``files`` directory containing your mzML files
``accurate_mass_search_params`` for your compounds create custom `db:mapping` and `db:struct` files as well as adduct lists

.. code-block:: python

    files = os.path.join(os.getcwd(), 'IdByMz_Example')
    already_centroided = False

    feature_finder_params = { # defaults in comments
        b'debug': b'false', # b'false'
        b'intensity:bins': 10, # 10
        b'mass_trace:mz_tolerance': 0.03, # 0.03
        b'mass_trace:min_spectra': 10, # 10
        b'mass_trace:max_missing': 1, # 1
        b'mass_trace:slope_bound': 0.1, # 0.1
        b'isotopic_pattern:charge_low': 1, # 1
        b'isotopic_pattern:charge_high': 4, # 4
        b'isotopic_pattern:mz_tolerance': 0.03, # 0.03
        b'isotopic_pattern:intensity_percentage': 10.0, # 10
        b'isotopic_pattern:intensity_percentage_optional': 0.1, # 0.1
        b'isotopic_pattern:mass_window_width': 25.0, # 25.0
        b'isotopic_pattern:abundance_12C': 98.93, # 98.93
        b'isotopic_pattern:abundance_14N': 99.632, # 99.632
        b'seed:min_score': 0.8, # 0.8
        b'fit:max_iterations': 500, # 500
        b'feature:min_score': 0.7, # 0.7
        b'feature:min_isotope_fit': 0.8, # 0.8
        b'feature:min_trace_score': 0.5, # 0.5
        b'feature:min_rt_span': 0.333, # 0.333
        b'feature:max_rt_span': 2.5, # 2.5
        b'feature:rt_shape': b'symmetric', # b'symmetric
        b'feature:max_intersection': 0.35, # 0.35
        b'feature:reported_mz': b'monoisotopic', # b'monoisotopic'
        b'user-seed:rt_tolerance': 5.0, # 5.0
        b'user-seed:mz_tolerance': 1.1, # 1.1
        b'user-seed:min_score': 0.5, # 0.5
        b'debug:pseudo_rt_shift': 500.0 # 500.0
    }

    accurate_mass_search_params = { # defaults in comments
        b'mass_error_value': 5.0, # 5.0
        b'mass_error_unit': b'ppm', # b'ppm'
        b'ionization_mode': b'negative', # b'positive'
        b'isotopic_similarity': b'false', # b'false'
        b'positive_adducts': str.encode(os.path.join(files, 'PositiveAdducts.tsv')), # b'CHEMISTRY/PositiveAdducts.tsv'
        b'negative_adducts': str.encode(os.path.join(files, 'NegativeAdducts.tsv')), # b'CHEMISTRY/NegativeAdducts.tsv'
        b'use_feature_adducts': b'false', # b'false'
        b'keep_unidentified_masses': b'false', # b'false'
        b'db:mapping': [str.encode(os.path.join(files, 'HMDBMappingFile.tsv'))], # b'CHEMISTRY/HMDBMappingFile.tsv'
        b'db:struct': [str.encode(os.path.join(files, 'HMDB2StructMapping.tsv'))], # b'CHEMISTRY/HMDB2StructMapping.tsv'
        b'mzTab:exportIsotopeIntensities': b'false' # b'false'
    }

    allowed_missing_values = 1
    min_feature_quality = 0.8
    n_nearest_neighbours = 2 # default: 2; for KNN imputation of missing values

Imports
*******

.. code-block:: python

    import os
    import shutil
    import requests

    import pandas as pd
    from pyopenms import *

    import numpy as np

    from sklearn.impute import KNNImputer
    from sklearn.preprocessing import FunctionTransformer
    from sklearn.pipeline import Pipeline

Download Example Data
*********************
This cell is important only for the example workflow.

.. code-block:: python

    if not os.path.isdir(os.path.join(os.getcwd(), 'IdByMz_Example')):
        os.mkdir(os.path.join(os.getcwd(), 'IdByMz_Example'))

    urls = ['https://abibuilder.informatik.uni-tuebingen.de/archive/openms/Tutorials/Data/latest/Example_Data/Metabolomics/datasets/2012_02_03_PStd_050_1.mzML',
            'https://abibuilder.informatik.uni-tuebingen.de/archive/openms/Tutorials/Data/latest/Example_Data/Metabolomics/datasets/2012_02_03_PStd_050_2.mzML',
            'https://abibuilder.informatik.uni-tuebingen.de/archive/openms/Tutorials/Data/latest/Example_Data/Metabolomics/datasets/2012_02_03_PStd_050_3.mzML',
            'https://abibuilder.informatik.uni-tuebingen.de/archive/openms/Tutorials/Data/latest/Example_Data/Metabolomics/databases/PositiveAdducts.tsv',
            'https://abibuilder.informatik.uni-tuebingen.de/archive/openms/Tutorials/Data/latest/Example_Data/Metabolomics/databases/NegativeAdducts.tsv',
            'https://abibuilder.informatik.uni-tuebingen.de/archive/openms/Tutorials/Data/latest/Example_Data/Metabolomics/databases/HMDBMappingFile.tsv',
            'https://abibuilder.informatik.uni-tuebingen.de/archive/openms/Tutorials/Data/latest/Example_Data/Metabolomics/databases/HMDB2StructMapping.tsv']

    for url in urls:
        request = requests.get(url, allow_redirects=True)
        open(os.path.join(files, os.path.basename(url)), 'wb').write(request.content)

Reading mzML files and Centroiding
**********************************
in: MS data (files); information if already centroided (already_centroided)
out: centroided mzML files in a subfolder 'centroid' (files)

.. code-block:: python

    if not already_centroided:
        if os.path.exists(os.path.join(files, 'centroid')):
            shutil.rmtree(os.path.join(files, 'centroid'))
        os.mkdir(os.path.join(files, 'centroid'))

        for file in os.listdir(files):

            if file.endswith('.mzML'):
                exp_raw = MSExperiment()
                MzMLFile().load(os.path.join(files, file), exp_raw)
                exp_centroid = MSExperiment()
                
                PeakPickerHiRes().pickExperiment(exp_raw, exp_centroid)
                
                MzMLFile().store(os.path.join(files, 'centroid', file), exp_centroid)

        files = os.path.join(files, 'centroid')

Feature Detection
*****************
in: centroided mzML files (files)
out: list with FeatureMaps (feature_maps)

.. code-block:: python

    feature_maps = []

    for file in os.listdir(files):
        
        if file.endswith('.mzML'):
            exp = MSExperiment()
            MzMLFile().load(os.path.join(files, file), exp)
            exp.updateRanges()

            feature_finder = FeatureFinder()
            feature_map = FeatureMap()

            params = Param()
            for key, value in feature_finder_params.items():
                params.setValue(key, value)

            feature_finder.run('centroided', exp, feature_map, params, FeatureMap())

            # fm.setUniqueIds()
            feature_map.setPrimaryMSRunPath([str.encode(file[:-5])])

            feature_maps.append(feature_map)

ConsensusMap with ability to export pandas DataFrames with intensity and meta values
************************************************************************************
will be obsolete when implemented in pyopenms directly

.. code-block:: python

    class ConsensusMapDF(ConsensusMap):
        def __init__(self):
            super().__init__()

        def get_intensity_df(self):
            labelfree = self.getExperimentType() == "label-free"
            filemeta = self.getColumnHeaders()  # type: dict[int, ColumnHeader]
            labels = list(set([header.label for header in
                            filemeta.values()]))  # TODO could be more efficient. Do we require same channels in all files?
            files = list(set([header.filename for header in filemeta.values()]))
            label_to_idx = {k: v for v, k in enumerate(labels)}
            file_to_idx = {k: v for v, k in enumerate(files)}

            def gen(cmap: ConsensusMap, fun):
                for f in cmap:
                    yield from fun(f)

            if not labelfree:
                # TODO write two functions for LF and labelled. One has only one channel, the other has only one file per CF
                def extractRowBlocksChannelWideFileLong(f: ConsensusFeature):
                    subfeatures = f.getFeatureList()  # type: list[FeatureHandle]
                    filerows = defaultdict(lambda: [0] * len(labels))  # TODO use numpy array?
                    for fh in subfeatures:
                        header = filemeta[fh.getMapIndex()]
                        row = filerows[header.filename]
                        row[label_to_idx[header.label]] = fh.getIntensity()
                    return (f.getUniqueId(), filerows)

                def extractRowsChannelWideFileLong(f: ConsensusFeature):
                    uniqueid, rowdict = extractRowBlocksChannelWideFileLong(f)
                    for file, row in rowdict.items():
                        row.append(file)
                        yield tuple([uniqueid] + row)

                if len(labels) == 1:
                    labels[0] = "intensity"
                dtypes = [('id', np.dtype('uint64'))] + list(zip(labels, ['f'] * len(labels)))
                dtypes.append(('file', 'U300'))
                # For TMT we know that every feature can only be from one file, since feature = PSM
                #cnt = 0
                #for f in self:
                #    cnt += f.size()

                intyarr = np.fromiter(iter=gen(self, extractRowsChannelWideFileLong), dtype=dtypes, count=self.size())
                return pd.DataFrame(intyarr).set_index('id')
            else:
                # Specialized for LabelFree which has to have only one channel
                def extractRowBlocksChannelLongFileWideLF(f: ConsensusFeature):
                    subfeatures = f.getFeatureList()  # type: list[FeatureHandle]
                    row = [0.] * len(files)  # TODO use numpy array?
                    for fh in subfeatures:
                        header = filemeta[fh.getMapIndex()]
                        row[file_to_idx[header.filename]] = fh.getIntensity()
                    yield tuple([f.getUniqueId()] + row)

                dtypes = [('id', np.dtype('uint64'))] + list(zip(files, ['f'] * len(files)))
                # cnt = self.size()*len(files) # TODO for this to work, we would need to fill with NAs for CFs that do not go over all files
                cnt = self.size()

                intyarr = np.fromiter(iter=gen(self, extractRowBlocksChannelLongFileWideLF), dtype=dtypes, count=cnt)
                return pd.DataFrame(intyarr).set_index('id')

        def get_metadata_df(self):
            def gen(cmap: ConsensusMap, fun):
                for f in cmap:
                    yield from fun(f)

            def extractMetaData(f: ConsensusFeature):
                # subfeatures = f.getFeatureList()  # type: list[FeatureHandle]
                pep = f.getPeptideIdentifications()  # type: list[PeptideIdentification]
                if len(pep) != 0:
                    hits = pep[0].getHits()
                    if len(hits) != 0:
                        besthit = hits[0]  # type: PeptideHit
                        # TODO what else
                        yield f.getUniqueId(), besthit.getSequence().toString(), f.getCharge(), f.getRT(), f.getMZ(), f.getQuality()
                    else:
                        yield f.getUniqueId(), None, f.getCharge(), f.getRT(), f.getMZ(), f.getQuality()
                else:
                    yield f.getUniqueId(), None, f.getCharge(), f.getRT(), f.getMZ(), f.getQuality()

            cnt = self.size()

            mddtypes = [('id', np.dtype('uint64')), ('sequence', 'U200'), ('charge', 'i4'), ('RT', np.dtype('double')), ('mz', np.dtype('double')),
                        ('quality', 'f')]
            mdarr = np.fromiter(iter=gen(self, extractMetaData), dtype=mddtypes, count=cnt)
            return pd.DataFrame(mdarr).set_index('id')

Feature Linking
***************
in: list with FeatureMaps (feature_maps)
out: ConsensusMap (consensus_map)

.. code-block:: python

    feature_grouper = FeatureGroupingAlgorithmQT()

    consensus_map = ConsensusMapDF()
    file_descriptions = consensus_map.getColumnHeaders()

    for i, feature_map in enumerate(feature_maps):
        file_description = file_descriptions.get(i, ColumnHeader())
        file_description.filename = feature_map.getMetaValue('spectra_data')[0].decode()
        file_description.size = feature_map.size()
        file_description.unique_id = feature_map.getUniqueId()
        file_descriptions[i] = file_description

    consensus_map.setColumnHeaders(file_descriptions)
    feature_grouper.group(feature_maps, consensus_map)

ConsensusMap to pandas DataFrame
********************************
in: ConsensusMap (consensus_map)
out: DataFrame with RT, mz and quality (result_df)

.. code-block:: python

    intensities = consensus_map.get_intensity_df()

    meta_data = consensus_map.get_metadata_df()[['RT', 'mz', 'quality']]

    result_df = pd.concat([meta_data, intensities], axis=1)
    result_df.reset_index(drop=True, inplace=True)

Accurate Mass Search
********************
in: ConsensusMap (consensus_map)
out: DataFrame with identifications (id_df)

.. code-block:: python

    accurate_mass_search = AccurateMassSearchEngine()

    params = Param()
    for key, value in accurate_mass_search_params.items():
        params.setValue(key, value)

    accurate_mass_search.setParameters(params)

    mztab = MzTab()

    accurate_mass_search.init()

    accurate_mass_search.run(consensus_map, mztab)

    MzTabFile().store(os.path.join(files, 'ids.tsv'), mztab)

    df = pd.read_csv(os.path.join(files, 'ids.tsv'), header=None, sep='\n')
    df = df[0].str.split('\t', expand=True)
    column_names = df.loc[df[0] == 'SMH']
    id_df = df.loc[df[0] == 'SML']
    id_df.columns = df.loc[df[0] == 'SMH'].iloc[0]
    id_df.reset_index(drop=True, inplace=True)

    os.remove(os.path.join(files, 'ids.tsv'))

Data Filtering and Imputation
*****************************
in: unfiltered result DataFrame (result_df)
out: features below minimum quality and with too many missing values removed, remaining missing values imputated with KNN algorithm (result_df)

.. code-block:: python

    # drop features that have more then the allowed number of missing values or are below minimum feature quality
    to_drop = []

    for i, row in result_df.iterrows():
        if row.isna().sum() > allowed_missing_values or row['quality'] < min_feature_quality:
            to_drop.append(i)

    result_df.drop(index=result_df.index[to_drop], inplace=True)

    # Data imputation with KNN
    imputer = Pipeline([("imputer", KNNImputer(n_neighbors=2)),
                        ("pandarizer",FunctionTransformer(lambda x: pd.DataFrame(x, columns = result_df.columns)))])

    result_df = imputer.fit_transform(result_df)

Annotate features with identified compounds
*******************************************
in: result DataFrame without identifications (result_df) and Identifications DataFrame (id_df)
out: result DataFrame with new identifications column, where compound names and adduct are stored [name : adduct]

.. code-block:: python
    result_df['identifications'] = pd.Series(['' for x in range(len(result_df.index))])

    for rt, mz, description, adduct in zip(id_df['retention_time'],
                                        id_df['exp_mass_to_charge'],
                                        id_df['description'],
                                        id_df['opt_global_adduct_ion']):

        indices = result_df.loc[(round(result_df['mz'], 6) == round(float(mz), 6)) & (round(result_df['RT'], 6) == round(float(rt), 6))].index.tolist()
        for index in indices:
            result_df.loc[index,'identifications'] += '[' + description + ' : ' + adduct + ']'
        
    result_df.to_csv(os.path.join(files, 'result.tsv'), sep = '\t', index = False)