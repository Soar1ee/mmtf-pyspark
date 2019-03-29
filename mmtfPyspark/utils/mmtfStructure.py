#!/usr/bin/env python
'''mmtfStructure.py

Decode msgpack unpacked data to mmtf structure

'''
__author__ = "Mars (Shih-Cheng) Huang"
__maintainer__ = "Mars (Shih-Cheng) Huang"
__email__ = "marshuang80@gmail.com"
__version__ = "0.2.0"
__status__ = "Done"

import numpy as np
from mmtf.utils import decoder_utils
from mmtfPyspark.utils import mmtfDecoder


class MmtfStructure(object):
    model_counter = 0
    chain_counter = 0
    group_counter = 0
    atom_counter = 0

    def __init__(self, input_data):
        """Decodes a msgpack unpacked data to mmtf structure"""

        # Variables that are not in all mmtf files
        if "bFactorList" in input_data:
            #int_array = np.frombuffer(input_data["bFactorList"][12:], '>i2')
            #decode_num = np.frombuffer(input_data["bFactorList"][8:12], '>i')
            #self.b_factor_list = mmtfDecoder.recursive_index_decode(
            #    int_array, decode_num)
            self.b_factor_list = mmtfDecoder.decode_type_10(input_data, "bFactorList")
        #else:
        #    self.b_factor_list = []
        if 'resolution' in input_data:
            self.resolution = input_data['resolution']
        else:
            self.resolution = None
        if "rFree" in input_data:
            self.r_free = input_data["rFree"]
        else:
            self.r_free = None
        if "rWork" in input_data:
            self.r_work = input_data["rWork"]
        else:
            self.r_work = None
        if "bioAssemblyList" in input_data:
            self.bio_assembly = input_data["bioAssemblyList"]
        else:
            self.bio_assembly = []
        if "unitCell" in input_data:
            self.unit_cell = input_data["unitCell"]
        else:
            self.unit_cell = None
        if "releaseDate" in input_data:
            self.release_date = input_data["releaseDate"]
        else:
            self.release_date = None
        if "depositionDate" in input_data:
            self.deposition_date = input_data["depositionDate"]
        else:
            self.deposition_date = None
        if "title" in input_data:
            self.title = input_data["title"]
        else:
            self.title = None
        if "mmtfVersion" in input_data:
            self.mmtf_version = input_data["mmtfVersion"]
        else:
            self.mmtf_version = None
        if "mmtfProducer" in input_data:
            self.mmtf_producer = input_data["mmtfProducer"]
        else:
            self.mmtf_producer = None
        if "structureId" in input_data:
            self.structure_id = input_data["structureId"]
        else:
            self.structure_id = None
        if "spaceGroup" in input_data:
            self.space_group = input_data["spaceGroup"]
        else:
            self.space_group = None
        # TODO bond info needs to be decoded
        # if "bondAtomList" in input_data:
        #     self.bond_atom_list = np.frombuffer(
        #         input_data["bondAtomList"][12:], '>i4')
        # else:
        #     self.bond_atom_list = None
        # if "bondOrderList" in input_data:
        #     self.bond_order_list = np.frombuffer(
        #         input_data["bondOrderList"][12:], '>i1')
        # else:
        #     self.bond_order_list = None
        if "secStructList" in input_data:
            #self.sec_struct_list = np.frombuffer(input_data["secStructList"][12:], '>i1')
            self.sec_struct_list = mmtfDecoder.decode_type_2(input_data, "secStructList")
        #else:
        #    self.sec_struct_list = []
        if "atomIdList" in input_data:
            #self.atom_id_list = np.cumsum(mmtfDecoder.run_length_decoder(
            #    np.frombuffer(input_data['atomIdList'][12:], '>i4')).astype(np.int16))
            self.atom_id_list = mmtfDecoder.decode_type_8(input_data, "atomIdList", input_data["numAtoms"])
        #else:
        #    self.atom_id_list = []
        if "sequenceIndexList" in input_data:
            #self.sequence_index_list = np.cumsum(mmtfDecoder.run_length_decoder(
            #   np.frombuffer(input_data['sequenceIndexList'][12:], '>i4')).astype(np.int16))
            self.sequence_index_list = mmtfDecoder.decode_type_8(input_data, "sequenceIndexList", input_data["numAtoms"])
        #else:
        #    self.sequence_index_list = []
        if "occupancyList" in input_data:
            #decode_num = np.frombuffer(input_data["occupancyList"][8:12], '>i')
            #self.occupancy_list = mmtfDecoder.run_length_decoder(
            #    np.frombuffer(input_data["occupancyList"][12:], ">i4")) / decode_num
            self.occupancy_list = mmtfDecoder.decode_type_9(input_data, "occupancyList", input_data["numAtoms"])
        #else:
        #    self.occupancy_list = []
        if "experimentalMethods" in input_data:
            self.experimental_methods = input_data["experimentalMethods"]
        else:
            self.experimental_methods = None
        if "insCodeList" in input_data:
            # TODO needs more efficient decoding method
            #ic = [chr(a) for a in mmtfDecoder.run_length_decoder(np.frombuffer(
            #    input_data["insCodeList"][12:], ">i4")).astype(np.int16)]
            #self.ins_code_list = np.array(ic, dtype=np.chararray)
            # new more efficient method
            #ic = mmtfDecoder.run_length_decoder(np.frombuffer(input_data["insCodeList"][12:], ">i4")) \
            #   .astype(np.uint8).tostring().decode("ascii")
            #self.ins_code_list = np.array(list(ic))
            self.ins_code_list = mmtfDecoder.decode_type_6(input_data, "insCodeList", input_data["numGroups"])
        #else:
        #    self.ins_code_list = []
        if "entityList" in input_data:
            self.entity_list = input_data["entityList"]
        else:
            self.entity_list = []

        if "chainNameList" in input_data:
            #self.chain_name_list = np.frombuffer(
            #    input_data["chainNameList"][12:], 'S4').astype(str)
            self.chain_name_list = mmtfDecoder.decode_type_5(input_data, "chainNameList")
        #else:
        #    self.chain_name_list = []

        # Variables guaranteed in mmtf files
        self.num_bonds = input_data["numBonds"]
        self.num_chains = input_data["numChains"]
        self.num_models = input_data["numModels"]
        self.num_atoms = input_data["numAtoms"]
        self.num_groups = input_data["numGroups"]
        self.chains_per_model = input_data["chainsPerModel"]
        self.groups_per_chain = input_data["groupsPerChain"]
        #self.group_id_list = np.cumsum(mmtfDecoder.run_length_decoder(
        #    np.frombuffer(input_data['groupIdList'][12:], '>i4'))).astype(np.int32)
        self.group_id_list = mmtfDecoder.decode_type_8(input_data, "groupIdList", self.num_groups)
        #self.group_type_list = np.frombuffer(
        #    input_data['groupTypeList'][12:], '>i4')
        self.group_type_list = mmtfDecoder.decode_type_4(input_data, "groupTypeList")
        #self.x_coord_list = mmtfDecoder.recursive_index_decode(np.frombuffer(
        #    input_data['xCoordList'][12:], '>i2'), np.frombuffer(input_data['xCoordList'][8:12], '>i'))
        #self.y_coord_list = mmtfDecoder.recursive_index_decode(np.frombuffer(
        #    input_data['yCoordList'][12:], '>i2'), np.frombuffer(input_data['yCoordList'][8:12], '>i'))
        #self.z_coord_list = mmtfDecoder.recursive_index_decode(np.frombuffer(
        #    input_data['zCoordList'][12:], '>i2'), np.frombuffer(input_data['zCoordList'][8:12], '>i'))
        self.x_coord_list = mmtfDecoder.decode_type_10(input_data, "xCoordList")
        self.y_coord_list = mmtfDecoder.decode_type_10(input_data, "yCoordList")
        self.z_coord_list = mmtfDecoder.decode_type_10(input_data, "zCoordList")
        self.group_list = input_data['groupList']
        #self.chain_id_list = np.frombuffer(
        #    input_data["chainIdList"][12:], 'S4').astype(str)
        self.chain_id_list = mmtfDecoder.decode_type_5(input_data, "chainIdList")
        #self.alt_loc_list = input_data['altLocList'][12:]
        self.alt_loc_list = mmtfDecoder.decode_type_6(input_data, "altLocList", self.num_atoms)
        self.alt_loc_set = True

    def pass_data_on(self, data_setters):
        """Write the data from the getters to the setters.

        Parameters
        ----------
        data_setters : DataTransferInterface
            a series of functions that can fill a chemical
        """
        self.set_alt_loc_list()
        data_setters.init_structure(self.num_bonds, len(self.x_coord_list), len(self.group_type_list),
                                    len(self.chain_id_list), len(self.chains_per_model), self.structure_id)
        decoder_utils.add_entity_info(self, data_setters)
        decoder_utils.add_atomic_information(self, data_setters)
        decoder_utils.add_header_info(self, data_setters)
        decoder_utils.add_xtalographic_info(self, data_setters)
        decoder_utils.generate_bio_assembly(self, data_setters)
        decoder_utils.add_inter_group_bonds(self, data_setters)
        data_setters.finalize_structure()

    def set_alt_loc_list(self):
        """Set the alternative location list for structure"""
        #self.alt_loc_list = [chr(x) for x in mmtfDecoder.run_length_decoder(
        #    np.frombuffer(self.alt_loc_list, ">i4")).astype(np.int16)]
        #self.alt_loc_set = True
        #self.alt_loc_list = mmtfDecoder.decode_type_6(self.alt_loc_list, "altLocList", self.num_atoms)
        return self
