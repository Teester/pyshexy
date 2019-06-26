# Copyright (c) 2017, Mayo Clinic
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification,
# are permitted provided that the following conditions are met:
#
# Redistributions of source code must retain the above copyright notice, this
#     list of conditions and the following disclaimer.
#
#     Redistributions in binary form must reproduce the above copyright notice,
#     this list of conditions and the following disclaimer in the documentation
#     and/or other materials provided with the distribution.
#
#     Neither the name of the Mayo Clinic nor the names of its contributors
#     may be used to endorse or promote products derived from this software
#     without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
# IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT,
# INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, 
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
# LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE
# OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED
# OF THE POSSIBILITY OF SUCH DAMAGE.
from typing import Tuple, Any


def compare_values(string_val: str, json_val: Any) -> bool:
    if isinstance(json_val, bool):
        # Note - this is probably too liberal but should be good enough
        if (string_val in ("1", "T", "t", "True", "true", "TRUE") and json_val) or \
           (string_val in ("0", "F", "f", "False", "false", "FALSE") and not json_val):
            return True
    # Try to match the numeric portion with the corresponding string
    elif isinstance(json_val, (int, float)):
        try:
            return float(string_val) == json_val
        except ValueError:
            pass

    return False


def json_filtr(kv1: Tuple[Any, Any], kv2: Tuple[Any, Any]) -> bool:
    # To qualify:
    #   1) The keys must be strings
    #   2) The keys must match
    #   3) Exactly one of the values must be a string
    if kv1 is None or kv2 is None or \
            (kv1[0] is not None and not isinstance(kv1[0], str)) or kv1[0] != kv2[0]:
        return False
    v1_is_string = isinstance(kv1[1], str)
    if v1_is_string == isinstance(kv2[1], str):
        return False

    # Try to match the numeric portion with the corresponding string
    numeric_val = kv2[1] if v1_is_string else kv1[1]
    string_val = kv1[1] if v1_is_string else kv2[1]
    return compare_values(string_val, numeric_val)



