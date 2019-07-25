# -------------------------------------------------------------------------------------------------
# <copyright file="precondition.pxd" company="Nautech Systems Pty Ltd">
#  Copyright (C) 2015-2019 Nautech Systems Pty Ltd. All rights reserved.
#  The use of this source code is governed by the license as found in the LICENSE.md file.
#  http://www.nautechsystems.io
# </copyright>
# -------------------------------------------------------------------------------------------------

cdef class Precondition:
    @staticmethod
    cdef true(bint predicate, str description)
    @staticmethod
    cdef type(object argument, object is_type, str param_name)
    @staticmethod
    cdef type_or_none(object argument, object is_type, str param_name)
    @staticmethod
    cdef is_in(object key, dict dictionary, str param_name, str dict_name)
    @staticmethod
    cdef not_in(object key, dict dictionary, str param_name, str dict_name)
    @staticmethod
    cdef list_type(list argument, type type_to_contain, str param_name)
    @staticmethod
    cdef dict_types(dict argument, type key_type, type value_type, str param_name)
    @staticmethod
    cdef none(object argument, str param_name: str)
    @staticmethod
    cdef not_none(object argument, str param_name)
    @staticmethod
    cdef valid_string(unicode argument, str param_name)
    @staticmethod
    cdef equal(object argument1, object argument2)
    @staticmethod
    cdef equal_lengths(
            list collection1,
            list collection2,
            str collection1_name,
            str collection2_name)
    @staticmethod
    cdef positive(double value, str param_name)
    @staticmethod
    cdef not_negative(double value, str param_name)
    @staticmethod
    cdef in_range(
            double value,
            str param_name,
            double start,
            double end)
    @staticmethod
    cdef not_empty(object argument, str param_name)
    @staticmethod
    cdef empty(object argument, str param_name)