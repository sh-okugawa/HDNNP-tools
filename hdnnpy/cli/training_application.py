# coding=utf-8

import fnmatch
import pathlib
import shutil

import chainer
import chainer.training.extensions as ext
from chainer.training.triggers import EarlyStoppingTrigger
import chainermn
from traitlets import (Bool, Dict, List, Unicode)
from traitlets.config import Application
import yaml

from hdnnpy.cli.configurables import (
    DatasetConfig, ModelConfig, Path, TrainingConfig,
    )
from hdnnpy.dataset import (AtomicStructure, DatasetGenerator, HDNNPDataset)
from hdnnpy.dataset.descriptor import DESCRIPTOR_DATASET
from hdnnpy.dataset.property import PROPERTY_DATASET
from hdnnpy.format import parse_xyz
from hdnnpy.model import (HighDimensionalNNP, MasterNNP)
from hdnnpy.preprocess import PREPROCESS
from hdnnpy.training import (
    Manager, Updater, ScatterPlot, set_log_scale,
    )
from hdnnpy.training.loss_function import LOSS_FUNCTION
from hdnnpy.utils import (MPI, pprint, pyyaml_path_representer)
import ase.io
## Additional import for saving dataset and exit before train
import numpy as np
import sys
import random



class TrainingApplication(Application):
    name = Unicode(u'hdnnpy train')
    description = 'Train a HDNNP to optimize given properties.'

    is_resume = Bool(
        False,
        help='Resume flag used internally.')
    resume_dir = Path(
        None,
        allow_none=True,
        help='This option can be set only by command line.')
    verbose = Bool(
        False,
        help='Set verbose mode'
        ).tag(config=True)

    classes = List([DatasetConfig, ModelConfig, TrainingConfig])

    config_file = Path(
        'training_config.py',
        help='Load this config file')

    aliases = Dict({
        'resume': 'TrainingApplication.resume_dir',
        'log_level': 'Application.log_level',
        })

    flags = Dict({
        'verbose': ({
            'TrainingApplication': {
                'verbose': True,
                },
            }, 'Set verbose mode'),
        'v': ({
            'TrainingApplication': {
                'verbose': True,
                },
            }, 'Set verbose mode'),
        'debug': ({
            'Application': {
                'log_level': 10,
                },
            }, 'Set log level to DEBUG'),
        })

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.dataset_config = None
        self.model_config = None
        self.training_config = None
        self.loss_function = None

    def initialize(self, argv=None):
        # temporarily set `resume_dir` configurable
        self.__class__.resume_dir.tag(config=True)
        self.parse_command_line(argv)

        if self.resume_dir is not None:
            self.is_resume = True
            self.config_file = self.resume_dir.with_name(self.config_file.name)
        self.load_config_file(self.config_file)

        self.dataset_config = DatasetConfig(config=self.config)
        self.model_config = ModelConfig(config=self.config)
        self.training_config = TrainingConfig(config=self.config)
        if self.is_resume:
            self.training_config.out_dir = self.resume_dir.parent
        name, _ = self.training_config.loss_function
        self.loss_function = LOSS_FUNCTION[name]

    def start(self):

        tc = self.training_config
        tc.out_dir.mkdir(parents=True, exist_ok=True)
        if not self.is_resume:
            shutil.copy(self.config_file,
                        tc.out_dir / self.config_file.name)
        tag_xyz_map, tc.elements = parse_xyz(
            tc.data_file, verbose=self.verbose)

        #2020/3/26 making hold out before PCA
        #split xyz data to train and test
        #then, construct dataset
        #the procedure is as follows:
        #1. temporaly save to train.xyz and test.xyz for each tag and
        #   map the tag to each file
        #2. construct the symmetry function data and PCA fit for training data
        #3. construct the symmetry function and apply PCA preprocess obtained by step 2

        #print(tag_xyz_map)


        #hold out procedure
        tag_training_xyz_map = {}
        tag_test_xyz_map = {}
        train_descriptor_npz =[]
        test_descriptor_npz = []

        for pattern in tc.tags:
            for tag in fnmatch.filter(tag_xyz_map, pattern):
                if self.verbose:
                    pprint(f'holdout xyz data tagged as "{tag}"')
                tagged_xyz = tag_xyz_map.get(tag)

                train_descriptor_npz.append(
                    tagged_xyz.with_name(f'{self.dataset_config.descriptor}.npz').exists())
                test_descriptor_npz.append(
                    tagged_xyz.with_name(f'{self.dataset_config.descriptor}-test.npz').exists())
                #print(tagged_xyz)
                xyz_data=ase.io.read(str(tagged_xyz), index=':', format='xyz')

                random.shuffle(xyz_data)
                s = int(len(xyz_data) * tc.train_test_ratio)
                train = xyz_data[:s]
                test = xyz_data[s:]
                assert len(train) > 0
                assert len(test) > 0

                ase.io.write(str(tc.data_file.with_name(tag))+"/train.xyz",train,format='xyz')
                ase.io.write(str(tc.data_file.with_name(tag)) + "/test.xyz", test, format='xyz')
                #print(tc.data_file.__class__)

                tag_training_xyz_map[tag] = (tc.data_file.with_name(tag)
                                    / 'train.xyz')
                tag_test_xyz_map[tag] = (tc.data_file.with_name(tag)
                                    / 'test.xyz')




        #decide load the npz for descriptor or not
        #if descriptor npz found in all tag, then load
        load_descriptor = False
        if(all(train_descriptor_npz) and all(test_descriptor_npz) ):
            load_descriptor = True
            pprint(f'reuse the preserved descriptor data. train.xyz and test.xyz data is not used.')

        train_datasets = self.construct_training_datasets(tag_training_xyz_map,load_descriptor)
        test_datasets = self.construct_test_datasets(tag_test_xyz_map,load_descriptor)
        '''
        for t in train_datasets:
            print(t.tag)
            print(t.property.properties)
        '''

        #reshapse the form of dataset
        dataset=[]
        for train in train_datasets:
            test_dataset = None
            for test in test_datasets:
                if(test.tag == train.tag):
                    test_dataset=test
            dataset.append((train,test))

        #test print
        '''
        for training, test in dataset:
            print(training.tag)
            print(test.tag)
            print(training.property.properties)
            print(test.property.properties)
        '''


        #original detaset generation
        #In this case, PCA use all data to constract transform matrix
        '''
        datasets = self.construct_datasets(tag_xyz_map)
        dataset = DatasetGenerator(*datasets).holdout(tc.train_test_ratio)
        '''


        ## Stop process here if no_train flag is set
        #print(tc.no_train)
        if tc.no_train:
            print('Process is stopped by no_train flag')
            sys.exit()
        ## End of stopping process



        result = self.train(dataset)
        if MPI.rank == 0:
            self.dump_result(result)

    #original one
    def construct_datasets(self, tag_xyz_map):
        dc = self.dataset_config
        mc = self.model_config
        tc = self.training_config

        preprocess_dir = tc.out_dir / 'preprocess'
        preprocess_dir.mkdir(parents=True, exist_ok=True)
        preprocesses = []
        for (name, args, kwargs) in dc.preprocesses:
            preprocess = PREPROCESS[name](*args, **kwargs)
            if self.is_resume:
                preprocess.load(
                    preprocess_dir / f'{name}.npz', verbose=self.verbose)
            preprocesses.append(preprocess)

        datasets = []
        for pattern in tc.tags:
            for tag in fnmatch.filter(tag_xyz_map, pattern):
                if self.verbose:
                    pprint(f'Construct sub dataset tagged as "{tag}"')
                tagged_xyz = tag_xyz_map.pop(tag)
                structures = AtomicStructure.read_xyz(tagged_xyz)

                # prepare descriptor dataset
                descriptor = DESCRIPTOR_DATASET[dc.descriptor](
                    self.loss_function.order['descriptor'],
                    structures, **dc.parameters)
                descriptor_npz = tagged_xyz.with_name(f'{dc.descriptor}.npz')
                if descriptor_npz.exists():
                    descriptor.load(
                        descriptor_npz, verbose=self.verbose, remake=dc.remake)
                else:
                    descriptor.make(verbose=self.verbose)
                    descriptor.save(descriptor_npz, verbose=self.verbose)

                # prepare property dataset
                property_ = PROPERTY_DATASET[dc.property_](
                    self.loss_function.order['property'], structures)
                property_npz = tagged_xyz.with_name(f'{dc.property_}.npz')
                if property_npz.exists():
                    property_.load(
                        property_npz, verbose=self.verbose, remake=dc.remake)
                else:
                    property_.make(verbose=self.verbose)
                    property_.save(property_npz, verbose=self.verbose)

                # construct HDNNP dataset from descriptor & property datasets
                dataset = HDNNPDataset(descriptor, property_)
                dataset.construct(
                    all_elements=tc.elements, preprocesses=preprocesses,
                    shuffle=True, verbose=self.verbose)
                dataset.scatter()
                datasets.append(dataset)
                dc.n_sample += dataset.total_size
                mc.n_input = dataset.n_input
                mc.n_output = dataset.n_label

        for preprocess in preprocesses:
            preprocess.save(
                preprocess_dir / f'{preprocess.name}.npz',
                verbose=self.verbose)

        return datasets

    #for preprocess, only use training dataset
    def construct_training_datasets(self, tag_xyz_map,load_descriptor):
        dc = self.dataset_config
        mc = self.model_config
        tc = self.training_config

        preprocess_dir = tc.out_dir / 'preprocess'
        preprocess_dir.mkdir(parents=True, exist_ok=True)
        preprocesses = []
        for (name, args, kwargs) in dc.preprocesses:
            preprocess = PREPROCESS[name](*args, **kwargs)
            if self.is_resume:
                preprocess.load(
                    preprocess_dir / f'{name}.npz', verbose=self.verbose)
            preprocesses.append(preprocess)

        datasets = []
        for pattern in tc.tags:
            for tag in fnmatch.filter(tag_xyz_map, pattern):
                if self.verbose:
                    pprint(f'Construct sub training dataset tagged as "{tag}"')
                tagged_xyz = tag_xyz_map.pop(tag)
                structures = AtomicStructure.read_xyz(tagged_xyz)

                # prepare descriptor dataset
                descriptor = DESCRIPTOR_DATASET[dc.descriptor](
                    self.loss_function.order['descriptor'],
                    structures, **dc.parameters)
                descriptor_npz = tagged_xyz.with_name(f'{dc.descriptor}.npz')
                if load_descriptor:
                    descriptor.load(
                        descriptor_npz, verbose=self.verbose, remake=dc.remake)
                else:
                    descriptor.make(verbose=self.verbose)
                    descriptor.save(descriptor_npz, verbose=self.verbose)

                # prepare property dataset
                property_ = PROPERTY_DATASET[dc.property_](
                    self.loss_function.order['property'], structures)
                property_npz = tagged_xyz.with_name(f'{dc.property_}.npz')
                if property_npz.exists() and load_descriptor:
                    property_.load(
                        property_npz, verbose=self.verbose, remake=dc.remake)
                else:
                    property_.make(verbose=self.verbose)
                    property_.save(property_npz, verbose=self.verbose)

                # construct HDNNP dataset from descriptor & property datasets
                dataset = HDNNPDataset(descriptor, property_)
                dataset.construct(
                    all_elements=tc.elements, preprocesses=preprocesses,
                    shuffle=True, verbose=self.verbose)

    ##Save preprocessed dataset
                dtset_npz = tagged_xyz.with_name(f'preprocd_dataset.npz')
                np.savez(dtset_npz, dataset=dataset)
    ##End of saving preprocessed dataset

                dataset.scatter()
                datasets.append(dataset)
                dc.n_sample += dataset.total_size
                mc.n_input = dataset.n_input
                mc.n_output = dataset.n_label

        for preprocess in preprocesses:
            preprocess.save(
                preprocess_dir / f'{preprocess.name}.npz',
                verbose=self.verbose)

        return datasets

    #use preprocess defined by training dataset
    #same procedure as prediction case
    def construct_test_datasets(self, tag_xyz_map,load_descriptor):
        dc = self.dataset_config
        mc = self.model_config
        tc = self.training_config
        preprocess_dir = tc.out_dir / 'preprocess'
        preprocesses = []
        for (name, args, kwargs) in dc.preprocesses:
            preprocess = PREPROCESS[name](*args, **kwargs)
            preprocess.load(
                preprocess_dir / f'{preprocess.name}.npz',
                verbose=self.verbose)
            preprocesses.append(preprocess)

        datasets = []
        for pattern in tc.tags:
            for tag in fnmatch.filter(tag_xyz_map, pattern):
                if self.verbose:
                    pprint(f'Construct sub test dataset tagged as "{tag}"')
                tagged_xyz = tag_xyz_map.pop(tag)
                structures = AtomicStructure.read_xyz(tagged_xyz)

                # prepare descriptor dataset
                descriptor = DESCRIPTOR_DATASET[dc.descriptor](
                    self.loss_function.order['descriptor'], structures, **dc.parameters)
                descriptor_npz = tagged_xyz.with_name(f'{dc.descriptor}-test.npz')
                if load_descriptor:
                    descriptor.load(
                        descriptor_npz, verbose=self.verbose, remake=dc.remake)
                else:
                    descriptor.make(verbose=self.verbose)
                    descriptor.save(descriptor_npz, verbose=self.verbose)

                # prepare property dataset
                property_ = PROPERTY_DATASET[dc.property_](
                    self.loss_function.order['property'], structures)
                property_npz = tagged_xyz.with_name(f'{dc.property_}-test.npz')
                if property_npz.exists() and load_descriptor:
                    property_.load(
                        property_npz, verbose=self.verbose, remake=dc.remake)
                else:
                    property_.make(verbose=self.verbose)
                    property_.save(property_npz, verbose=self.verbose)

                # construct test dataset from descriptor & property datasets
                dataset = HDNNPDataset(descriptor, property_)
                dataset.construct(
                    all_elements=tc.elements, preprocesses=preprocesses,
                    shuffle=False, verbose=self.verbose)
                dataset.scatter()
                datasets.append(dataset)
                dc.n_sample += dataset.total_size
                mc.n_input = dataset.n_input
                mc.n_output = dataset.n_label

        return datasets

    def train(self, dataset, comm=None):
        mc = self.model_config
        tc = self.training_config
        if comm is None:
            comm = chainermn.create_communicator('naive', MPI.comm)
        result = {'training_time': 0.0, 'observation': []}

        # model and optimizer
        master_nnp = MasterNNP(
            tc.elements, mc.n_input, mc.hidden_layers, mc.n_output, mc.initializer)
        master_opt = chainer.optimizers.Adam(tc.init_lr)
        master_opt = chainermn.create_multi_node_optimizer(master_opt, comm)
        master_opt.setup(master_nnp)
        master_opt.add_hook(chainer.optimizer_hooks.Lasso(tc.l1_norm))
        master_opt.add_hook(chainer.optimizer_hooks.WeightDecay(tc.l2_norm))

        for training, test in dataset:
            tag = training.tag
            properties = training.property.properties

            # iterators
            train_iter = chainer.iterators.SerialIterator(
                training, tc.batch_size // MPI.size, repeat=True, shuffle=True)
            test_iter = chainer.iterators.SerialIterator(
                test, tc.batch_size // MPI.size, repeat=False, shuffle=False)

            # model
            hdnnp = HighDimensionalNNP(
                training.elemental_composition,
                mc.n_input, mc.hidden_layers, mc.n_output, mc.initializer)
            hdnnp.sync_param_with(master_nnp)
            main_opt = chainer.Optimizer()
            main_opt = chainermn.create_multi_node_optimizer(main_opt, comm)
            main_opt.setup(hdnnp)

            # loss function
            _, kwargs = tc.loss_function
            loss_function = self.loss_function(hdnnp, properties, **kwargs)
            observation_keys = loss_function.observation_keys

            # triggers
            interval = (tc.interval, 'epoch')
            stop_trigger = EarlyStoppingTrigger(
                check_trigger=interval,
                monitor=f'val/main/{observation_keys[-1]}',
                patients=tc.patients, mode='min',
                verbose=self.verbose, max_trigger=(tc.epoch, 'epoch'))

            # updater and trainer
            updater = Updater(train_iter,
                              {'main': main_opt, 'master': master_opt},
                              loss_func=loss_function.eval)
            out_dir = tc.out_dir / tag
            trainer = chainer.training.Trainer(updater, stop_trigger, out_dir)

            # extensions
            trainer.extend(ext.ExponentialShift('alpha', 1 - tc.lr_decay,
                                                target=tc.final_lr,
                                                optimizer=master_opt))
            evaluator = chainermn.create_multi_node_evaluator(
                ext.Evaluator(test_iter, hdnnp, eval_func=loss_function.eval),
                comm)
            trainer.extend(evaluator, name='val')
            if tc.scatter_plot:
                trainer.extend(ScatterPlot(test, hdnnp, comm),
                               trigger=interval)
            if MPI.rank == 0:
                if tc.log_report:
                    trainer.extend(ext.LogReport(log_name='training.log'))
                if tc.print_report:
                    trainer.extend(ext.PrintReport(
                        ['epoch', 'iteration']
                        + [f'main/{key}' for key in observation_keys]
                        + [f'val/main/{key}' for key in observation_keys]))
                if tc.plot_report:
                    trainer.extend(ext.PlotReport(
                        [f'main/{key}' for key in observation_keys],
                        x_key='epoch', postprocess=set_log_scale,
                        file_name='training_set.png', marker=None))
                    trainer.extend(ext.PlotReport(
                        [f'val/main/{key}' for key in observation_keys],
                        x_key='epoch', postprocess=set_log_scale,
                        file_name='validation_set.png', marker=None))

            manager = Manager(tag, trainer, result, is_snapshot=True)
            if self.is_resume:
                manager.check_to_resume(self.resume_dir.name)
            if manager.allow_to_run:
                with manager:
                    trainer.run()

        if MPI.rank == 0:
            chainer.serializers.save_npz(
                tc.out_dir / 'master_nnp.npz', master_nnp)

        return result

    def dump_result(self, result):
        yaml.add_representer(pathlib.PosixPath, pyyaml_path_representer)
        result_file = self.training_config.out_dir / 'training_result.yaml'
        with result_file.open('w') as f:
            yaml.dump({
                'dataset': self.dataset_config.dump(),
                'model': self.model_config.dump(),
                'training': self.training_config.dump(),
                }, f, default_flow_style=False)
            yaml.dump({
                'result': result,
                }, f, default_flow_style=False)


def generate_config_file():
    training_app = TrainingApplication()
    training_app.config_file.write_text(training_app.generate_config_file())
