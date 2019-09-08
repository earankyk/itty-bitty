#
# pieces - An experimental BitTorrent client
#
# Copyright 2016 markus.eliasson@gmail.com
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from collections import OrderedDict
from itty_bitty.bencoding import Decoder, Encoder
import pytest

def assertEqual(a, b):
    assert a == b

def test_peek_iis_idempotent():
    decoder = Decoder(b'12')

    assertEqual(b'1', decoder._peek())
    assertEqual(b'1', decoder._peek())

def test_peek_should_handle_end():
    decoder = Decoder(b'1')
    decoder._index = 1

    assertEqual(None, decoder._peek())

def test_read_until_found():
    decoder = Decoder(b'123456')

    assertEqual(b'123', decoder._read_until(b'4'))

def test_read_until_not_found():
    decoder = Decoder(b'123456')

    with pytest.raises(RuntimeError):
        decoder._read_until(b'7')

def test_empty_string():
    with pytest.raises(EOFError):
        Decoder(b'').decode()

def test_not_a_string():
    with pytest.raises(TypeError):
        Decoder(123).decode()
    with pytest.raises(TypeError):
        Decoder({'a': 1}).decode()

def test_integer():
    res = Decoder(b'i123e').decode()

    assertEqual(int(res), 123)

def test_string():
    res = Decoder(b'4:name').decode()

    assertEqual(res, b'name')

def test_min_string():
    res = Decoder(b'1:a').decode()

    assertEqual(res, b'a')

def test_string_with_space():
    res = Decoder(b'12:Middle Earth').decode()

    assertEqual(res, b'Middle Earth')

def test_list():
    res = Decoder(b'l4:spam4:eggsi123ee').decode()

    assertEqual(len(res), 3)
    assertEqual(res[0], b'spam')
    assertEqual(res[1], b'eggs')
    assertEqual(res[2], 123)

def test_dict():
    res = Decoder(b'd3:cow3:moo4:spam4:eggse').decode()

    assertTrue(isinstance(res, dict))
    assertEqual(res[b'cow'], b'moo')
    assertEqual(res[b'spam'], b'eggs')

def test_malformed_key_in_dict_should_failed():
    with pytest.raises(EOFError):
        Decoder(b'd3:moo4:spam4:eggse').decode()

def test_empty_encoding():
    res = Encoder(None).encode()

    assertEqual(res, None)

def test_integer():
    res = Encoder(123).encode()

    assertEqual(b'i123e', res)

def test_string():
    res = Encoder('Middle Earth').encode()

    assertEqual(b'12:Middle Earth', res)

def test_list():
    res = Encoder(['spam', 'eggs', 123]).encode()

    assertEqual(b'l4:spam4:eggsi123ee', res)

def test_dict():

    d = OrderedDict()
    d['cow'] = 'moo'
    d['spam'] = 'eggs'
    res = Encoder(d).encode()

    assertEqual(b'd3:cow3:moo4:spam4:eggse', res)

def test_nested_structure():
    outer = OrderedDict()
    b = OrderedDict()
    b['ba'] = 'foo'
    b['bb'] = 'bar'
    outer['a'] = 123
    outer['b'] = b
    outer['c'] = [['a', 'b'], 'z']
    res = Encoder(outer).encode()

    assertEqual(res,
                     b'd1:ai123e1:bd2:ba3:foo2:bb3:bare1:cll1:a1:be1:zee')
