# Copyright 2011, VMware, Inc.
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.
#
# Borrowed from the module 'neutron.common.utils' in OpenStack project.


def _hex_format(port, mask=0):

    def hex_str(num):
        return format(num, '#06x')
    if mask > 0:
        return "%s/%s" % (hex_str(port), hex_str(0xffff & ~mask))
    return hex_str(port)


def _gen_rules_port_min(port_min, top_bit):
    """
    Encode a port range range(port_min, (port_min | (top_bit - 1)) + 1) into
    a set of bit value/masks.
    """
    # Processing starts with setting up mask and top_bit variables to their
    # maximum. Top_bit has the form (1000000) with '1' pointing to the register
    # being processed, while mask has the form (0111111) with '1' showing
    # possible range to be covered.
    #
    # With each rule generation cycle, mask and top_bit are bit shifted to the
    # right. When top_bit reaches 0 it means that last register was processed.
    #
    # Let port_min be n bits long, top_bit = 1 << k, 0<=k<=n-1.
    #
    # Each cycle step checks the following conditions:
    #
    #     1). port & mask == 0
    #     This means that remaining bits k..1 are equal to '0' and can be
    #     covered by a single port/mask rule.
    #
    #     If condition 1 doesn't fit, then both top_bit and mask are bit
    #     shifted to the right and condition 2 is checked:
    #
    #     2). port & top_bit == 0
    #     This means that kth port bit is equal to '0'. By setting it to '1'
    #     and masking other (k-1) bits all ports in range
    #     [P, P + 2^(k-1)-1] are guaranteed to be covered.
    #     Let p_k be equal to port first (n-k) bits with rest set to 0.
    #     Then P = p_k | top_bit.
    #
    # Correctness proof:
    # The remaining range to be encoded in a cycle is calculated as follows:
    # R = [port_min, port_min | mask].
    # If condition 1 holds, then a rule that covers R is generated and the job
    # is done.
    # If condition 2 holds, then the rule emitted will cover 2^(k-1) values
    # from the range. Remaining range R will shrink by 2^(k-1).
    # If condition 2 doesn't hold, then even after top_bit/mask shift in next
    # iteration the value of R won't change.
    #
    # Full cycle example for range [40, 64):
    # port=0101000, top_bit=1000000, k=6
    # * step 1, k=6, R=[40, 63]
    #   top_bit=1000000, mask=0111111 -> condition 1 doesn't hold, shifting
    #                                    mask/top_bit
    #   top_bit=0100000, mask=0011111 -> condition 2 doesn't hold
    #
    # * step 2, k=5, R=[40, 63]
    #   top_bit=0100000, mask=0011111 -> condition 1 doesn't hold, shifting
    #                                    mask/top_bit
    #   top_bit=0010000, mask=0001111 -> condition 2 holds -> 011xxxx or
    #                                                         0x0030/fff0
    # * step 3, k=4, R=[40, 47]
    #   top_bit=0010000, mask=0001111 -> condition 1 doesn't hold, shifting
    #                                    mask/top_bit
    #   top_bit=0001000, mask=0000111 -> condition 2 doesn't hold
    #
    # * step 4, k=3, R=[40, 47]
    #   top_bit=0001000, mask=0000111 -> condition 1 holds -> 0101xxx or
    #                                                         0x0028/fff8
    #
    #   rules=[0x0030/fff0, 0x0028/fff8]

    rules = []
    mask = top_bit - 1

    while True:
        if (port_min & mask) == 0:
            # greedy matched a streak of '0' in port_min
            rules.append(_hex_format(port_min, mask))
            break
        top_bit >>= 1
        mask >>= 1
        if (port_min & top_bit) == 0:
            # matched next '0' in port_min to substitute for '1' in resulting
            # rule
            rules.append(_hex_format(port_min & ~mask | top_bit, mask))
    return rules


def _gen_rules_port_max(port_max, top_bit):
    """
    Encode a port range range(port_max & ~(top_bit - 1), port_max + 1) into
    a set of bit value/masks.
    """
    # Processing starts with setting up mask and top_bit variables to their
    # maximum. Top_bit has the form (1000000) with '1' pointing to the register
    # being processed, while mask has the form (0111111) with '1' showing
    # possible range to be covered.
    #
    # With each rule generation cycle, mask and top_bit are bit shifted to the
    # right. When top_bit reaches 0 it means that last register was processed.
    #
    # Let port_max be n bits long, top_bit = 1 << k, 0<=k<=n-1.
    #
    # Each cycle step checks the following conditions:
    #
    #     1). port & mask == mask
    #     This means that remaining bits k..1 are equal to '1' and can be
    #     covered by a single port/mask rule.
    #
    #     If condition 1 doesn't fit, then both top_bit and mask are bit
    #     shifted to the right and condition 2 is checked:
    #
    #     2). port & top_bit == top_bit
    #     This means that kth port bit is equal to '1'. By setting it to '0'
    #     and masking other (k-1) bits all ports in range
    #     [P, P + 2^(k-1)-1] are guaranteed to be covered.
    #     Let p_k be equal to port first (n-k) bits with rest set to 0.
    #     Then P = p_k | ~top_bit.
    #
    # Correctness proof:
    # The remaining range to be encoded in a cycle is calculated as follows:
    # R = [port_max & ~mask, port_max].
    # If condition 1 holds, then a rule that covers R is generated and the job
    # is done.
    # If condition 2 holds, then the rule emitted will cover 2^(k-1) values
    # from the range. Remaining range R will shrink by 2^(k-1).
    # If condition 2 doesn't hold, then even after top_bit/mask shift in next
    # iteration the value of R won't change.
    #
    # Full cycle example for range [64, 105]:
    # port=1101001, top_bit=1000000, k=6
    # * step 1, k=6, R=[64, 105]
    #   top_bit=1000000, mask=0111111 -> condition 1 doesn't hold, shifting
    #                                    mask/top_bit
    #   top_bit=0100000, mask=0011111 -> condition 2 holds -> 10xxxxx or
    #                                                         0x0040/ffe0
    # * step 2, k=5, R=[96, 105]
    #   top_bit=0100000, mask=0011111 -> condition 1 doesn't hold, shifting
    #                                    mask/top_bit
    #   top_bit=0010000, mask=0001111 -> condition 2 doesn't hold
    #
    # * step 3, k=4, R=[96, 105]
    #   top_bit=0010000, mask=0001111 -> condition 1 doesn't hold, shifting
    #                                    mask/top_bit
    #   top_bit=0001000, mask=0000111 -> condition 2 holds -> 1100xxx or
    #                                                         0x0060/fff8
    # * step 4, k=3, R=[104, 105]
    #   top_bit=0001000, mask=0000111 -> condition 1 doesn't hold, shifting
    #                                    mask/top_bit
    #   top_bit=0000100, mask=0000011 -> condition 2 doesn't hold
    #
    # * step 5, k=2, R=[104, 105]
    #   top_bit=0000100, mask=0000011 -> condition 1 doesn't hold, shifting
    #                                    mask/top_bit
    #   top_bit=0000010, mask=0000001 -> condition 2 doesn't hold
    #
    # * step 6, k=1, R=[104, 105]
    #   top_bit=0000010, mask=0000001 -> condition 1 holds -> 1101001 or
    #                                                         0x0068
    #
    #   rules=[0x0040/ffe0, 0x0060/fff8, 0x0068]

    rules = []
    mask = top_bit - 1

    while True:
        if (port_max & mask) == mask:
            # greedy matched a streak of '1' in port_max
            rules.append(_hex_format(port_max & ~mask, mask))
            break
        top_bit >>= 1
        mask >>= 1
        if (port_max & top_bit) == top_bit:
            # matched next '1' in port_max to substitute for '0' in resulting
            # rule
            rules.append(_hex_format(port_max & ~mask & ~top_bit, mask))
    return rules


def port_rule_masking(port_min, port_max):
    """Translate a range [port_min, port_max] into a set of bitwise matches.

    Each match has the form 'port/mask'. The port and mask are 16-bit numbers
    written in hexadecimal prefixed by 0x. Each 1-bit in mask requires that
    the corresponding bit in port must match. Each 0-bit in mask causes the
    corresponding bit to be ignored.
    """

    # Let binary representation of port_min and port_max be n bits long and
    # have first m bits in common, 0 <= m <= n.
    #
    # If remaining (n - m) bits of given ports define 2^(n-m) values, then
    # [port_min, port_max] range is covered by a single rule.
    # For example:
    # n = 6
    # port_min = 16 (binary 010000)
    # port_max = 23 (binary 010111)
    # Ports have m=3 bits in common with the remaining (n-m)=3 bits
    # covering range [0, 2^3), which equals to a single 010xxx rule. The algo
    # will return [0x0010/fff8].
    #
    # Else [port_min, port_max] range will be split into 2: range [port_min, T)
    # and [T, port_max]. Let p_m be the common part of port_min and port_max
    # with other (n-m) bits set to 0. Then T = p_m | 1 << (n-m-1).
    # For example:
    # n = 7
    # port_min = 40  (binary 0101000)
    # port_max = 105 (binary 1101001)
    # Ports have m=0 bits in common, p_m=000000. Then T=1000000 and the
    # initial range [40, 105] is divided into [40, 64) and [64, 105].
    # Each of the ranges will be processed separately, then the generated rules
    # will be merged.
    #
    # Check port_max >= port_min.
    if port_max < port_min:
        raise ValueError(_("'port_max' is smaller than 'port_min'"))

    bitdiff = port_min ^ port_max
    if bitdiff == 0:
        # port_min == port_max
        return [_hex_format(port_min)]
    # for python3.x, bit_length could be used here
    top_bit = 1
    while top_bit <= bitdiff:
        top_bit <<= 1
    if (port_min & (top_bit - 1) == 0 and
            port_max & (top_bit - 1) == top_bit - 1):
        # special case, range of 2^k ports is covered
        return [_hex_format(port_min, top_bit - 1)]

    top_bit >>= 1
    rules = []
    rules.extend(_gen_rules_port_min(port_min, top_bit))
    rules.extend(_gen_rules_port_max(port_max, top_bit))
    return rules


if __name__ == "__main__":
    expect = ['0x03e8/0xfff8', '0x03f0/0xfff0', '0x0400/0xfe00',
              '0x0600/0xff00', '0x0700/0xff80', '0x0780/0xffc0',
              '0x07c0/0xfff0']
    output = port_rule_masking(1000, 1999)

    ok1 = ok2 = True
    for i in expect:
        if i not in output:
            ok1 = False
            break
    for i in output:
        if i not in expect:
            ok2 = False
            break
    print("Expect:", expect)
    print("Output:", output)
    print("Result:", "Right" if ok1 and ok2 else "Error")
