package snippet

import (
	"fmt"
	"sort"
)

func hexStr(num int) string {
	return fmt.Sprintf("%#04x", num)
}

func hexFmt(port int, mask ...int) string {
	_mask := 0
	if len(mask) > 0 && mask[0] > 0 {
		_mask = mask[0]
	}
	if _mask <= 0 {
		return hexStr(port)
	}
	return fmt.Sprintf("%s/%s", hexStr(port), hexStr(0xffff & ^_mask))
}

// getRulesPortMin encodes a port range
// range(minPort, (minPort | (topBit - 1)) + 1) into a set of bit value/masks.
func genRulesPortMin(minPort, topBit int) []string {
	// Processing starts with setting up mask and topBit variables to their
	// maximum. TopBit has the form (1000000) with '1' pointing to the register
	// being processed, while mask has the form (0111111) with '1' showing
	// possible range to be covered.
	//
	// With each rule generation cycle, mask and topBit are bit shifted to the
	// right. When topBit reaches 0 it means that last register was processed.
	//
	// Let minPort be n bits long, topBit = 1 << k, 0<=k<=n-1.
	//
	// Each cycle step checks the following conditions:
	//
	//     1). port & mask == 0
	//     This means that remaining bits k..1 are equal to '0' and can be
	//     covered by a single port/mask rule.
	//
	//     If condition 1 doesn't fit, then both topBit and mask are bit
	//     shifted to the right and condition 2 is checked:
	//
	//     2). port & topVit == 0
	//     This means that kth port bit is equal to '0'. By setting it to '1'
	//     and masking other (k-1) bits all ports in range
	//     [P, P + 2^(k-1)-1] are guaranteed to be covered.
	//     Let p_k be equal to port first (n-k) bits with rest set to 0.
	//     Then P = p_k | top_bit.
	//
	// Correctness proof:
	// The remaining range to be encoded in a cycle is calculated as follows:
	// R = [minPOrt, minPort | mask].
	// If condition 1 holds, then a rule that covers R is generated and the job
	// is done.
	// If condition 2 holds, then the rule emitted will cover 2^(k-1) values
	// from the range. Remaining range R will shrink by 2^(k-1).
	// If condition 2 doesn't hold, then even after topVit/mask shift in next
	// iteration the value of R won't change.
	//
	// Full cycle example for range [40, 64):
	// port=0101000, topBit=1000000, k=6
	// * step 1, k=6, R=[40, 63]
	//   topBit=1000000, mask=0111111 -> condition 1 doesn't hold, shifting
	//                                   mask/top_bit
	//   topBit=0100000, mask=0011111 -> condition 2 doesn't hold
	//
	// * step 2, k=5, R=[40, 63]
	//   topBit=0100000, mask=0011111 -> condition 1 doesn't hold, shifting
	//                                   mask/top_bit
	//   topBit=0010000, mask=0001111 -> condition 2 holds -> 011xxxx or
	//                                                        0x0030/fff0
	// * step 3, k=4, R=[40, 47]
	//   topBit=0010000, mask=0001111 -> condition 1 doesn't hold, shifting
	//                                   mask/topBit
	//   topBit=0001000, mask=0000111 -> condition 2 doesn't hold
	//
	// * step 4, k=3, R=[40, 47]
	//   topBit=0001000, mask=0000111 -> condition 1 holds -> 0101xxx or
	//                                                        0x0028/fff8
	//
	//   rules=[0x0030/fff0, 0x0028/fff8]

	rules := []string{}
	mask := topBit - 1
	for {
		if (minPort & mask) == 0 {
			// greedy matched a streak of '0' in port_min
			rules = append(rules, hexFmt(minPort, mask))
			break
		}
		topBit >>= 1
		mask >>= 1
		if (minPort & topBit) == 0 {
			// matched next '0' in port_min to substitute for '1' in resulting
			rules = append(rules, hexFmt(minPort & ^mask | topBit, mask))
		}
	}
	return rules
}

// getRulesPortMax encodes a port range
// range(maxPort & ~(topBit - 1), maxPort + 1) into a set of bit value/masks.
func genRulesPortMax(maxPort, topBit int) []string {
	// Processing starts with setting up mask and topBit variables to their
	// maximum. TopBit has the form (1000000) with '1' pointing to the register
	// being processed, while mask has the form (0111111) with '1' showing
	// possible range to be covered.
	//
	// With each rule generation cycle, mask and topBit are bit shifted to the
	// right. When topBit reaches 0 it means that last register was processed.
	//
	// Let maxPort be n bits long, topBit = 1 << k, 0<=k<=n-1.
	//
	// Each cycle step checks the following conditions:
	//
	//     1). port & mask == mask
	//     This means that remaining bits k..1 are equal to '1' and can be
	//     covered by a single port/mask rule.
	//
	//     If condition 1 doesn't fit, then both topBit and mask are bit
	//     shifted to the right and condition 2 is checked:
	//
	//     2). port & topBit == topBit
	//     This means that kth port bit is equal to '1'. By setting it to '0'
	//     and masking other (k-1) bits all ports in range
	//     [P, P + 2^(k-1)-1] are guaranteed to be covered.
	//     Let p_k be equal to port first (n-k) bits with rest set to 0.
	//     Then P = p_k | ~top_bit.
	//
	// Correctness proof:
	// The remaining range to be encoded in a cycle is calculated as follows:
	// R = [maxPort & ~mask, maxPort].
	// If condition 1 holds, then a rule that covers R is generated and the job
	// is done.
	// If condition 2 holds, then the rule emitted will cover 2^(k-1) values
	// from the range. Remaining range R will shrink by 2^(k-1).
	// If condition 2 doesn't hold, then even after topBit/mask shift in next
	// iteration the value of R won't change.
	//
	// Full cycle example for range [64, 105]:
	// port=1101001, topBit=1000000, k=6
	// * step 1, k=6, R=[64, 105]
	//   topBit=1000000, mask=0111111 -> condition 1 doesn't hold, shifting
	//                                   mask/topBit
	//   topBit=0100000, mask=0011111 -> condition 2 holds -> 10xxxxx or
	//                                                        0x0040/ffe0
	// * step 2, k=5, R=[96, 105]
	//   topBit=0100000, mask=0011111 -> condition 1 doesn't hold, shifting
	//                                   mask/topBit
	//   topBit=0010000, mask=0001111 -> condition 2 doesn't hold
	//
	// * step 3, k=4, R=[96, 105]
	//   topBit=0010000, mask=0001111 -> condition 1 doesn't hold, shifting
	//                                   mask/topBit
	//   topBit=0001000, mask=0000111 -> condition 2 holds -> 1100xxx or
	//                                                        0x0060/fff8
	// * step 4, k=3, R=[104, 105]
	//   topVit=0001000, mask=0000111 -> condition 1 doesn't hold, shifting
	//                                   mask/topBit
	//   topVit=0000100, mask=0000011 -> condition 2 doesn't hold
	//
	// * step 5, k=2, R=[104, 105]
	//   topVit=0000100, mask=0000011 -> condition 1 doesn't hold, shifting
	//                                   mask/topBit
	//   topVit=0000010, mask=0000001 -> condition 2 doesn't hold
	//
	// * step 6, k=1, R=[104, 105]
	//   topVit=0000010, mask=0000001 -> condition 1 holds -> 1101001 or
	//                                                        0x0068
	//
	//   rules=[0x0040/ffe0, 0x0060/fff8, 0x0068]

	rules := []string{}
	mask := topBit - 1
	for {
		if (maxPort & mask) == mask {
			// greedy matched a streak of '1' in maxPort
			rules = append(rules, hexFmt(maxPort & ^mask, mask))
			break
		}
		topBit >>= 1
		mask >>= 1
		if (maxPort & topBit) == topBit {
			// matched next '1' in maxPort to substitute for '0' in resulting
			rules = append(rules, hexFmt(maxPort & ^mask & ^topBit, mask))
		}
	}
	return rules
}

// PortRuleMasking translates a range [port_min, port_max] into a set of
// bitwise matches.
//
// Each match has the form 'port/mask'. The port and mask are 16-bit numbers
// written in hexadecimal prefixed by 0x. Each 1-bit in mask requires that
// the corresponding bit in port must match. Each 0-bit in mask causes the
// corresponding bit to be ignored.
func PortRuleMasking(minPort, maxPort int) []string {
	// Let binary representation of minPort and maxPort be n bits long and
	// have first m bits in common, 0 <= m <= n.
	//
	// If remaining (n - m) bits of given ports define 2^(n-m) values, then
	// [minPort, maxPort] range is covered by a single rule.
	// For example:
	// n = 6
	// minPort = 16 (binary 010000)
	// maxPort = 23 (binary 010111)
	// Ports have m=3 bits in common with the remaining (n-m)=3 bits
	// covering range [0, 2^3), which equals to a single 010xxx rule. The algo
	// will return [0x0010/fff8].
	//
	// Else [minPort, maxPort] range will be split into 2: range [minPort, T)
	// and [T, maxPort]. Let p_m be the common part of minPort and maxPort
	// with other (n-m) bits set to 0. Then T = p_m | 1 << (n-m-1).
	// For example:
	// n = 7
	// minPort = 40  (binary 0101000)
	// maxPort = 105 (binary 1101001)
	// Ports have m=0 bits in common, p_m=000000. Then T=1000000 and the
	// initial range [40, 105] is divided into [40, 64) and [64, 105].
	// Each of the ranges will be processed separately, then the generated rules
	// will be merged.

	if maxPort < minPort {
		panic(fmt.Errorf("maxPort is smaller than minPort"))
	}
	bitdiff := minPort ^ maxPort
	if bitdiff == 0 { // minPort == maxPort
		return []string{hexFmt(minPort)}
	}

	topBit := 1
	for topBit <= bitdiff {
		topBit <<= 1
	}
	if minPort&(topBit-1) == 0 && maxPort&(topBit-1) == topBit-1 {
		// special case, range of 2^k ports is covered
		return []string{hexFmt(minPort, topBit-1)}
	}

	topBit >>= 1
	minRules := genRulesPortMin(minPort, topBit)
	maxRules := genRulesPortMax(maxPort, topBit)
	rules := make([]string, len(minRules)+len(maxRules))
	copy(rules, minRules)
	copy(rules[len(minRules):], maxRules)
	sort.Strings(rules)
	return rules
}
