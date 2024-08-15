#include <nanobind/nanobind.h>
#include <cstdint>
#include <climits>
#include "multiply.hpp"
#include "engine/Game.hpp"

template <typename T>
T pext_impl(const T src, const T mask) {
    T dest = 0;
    int m = 0, k = 0;
    while (m < sizeof(T) * CHAR_BIT) {
        if ((mask >> m) & 1) {
            dest |= (src & (1 << m)) >> (m - k);
            k++;
        }
        m++;
    }
    return dest;
}

#if defined(__BMI2__)
#include <immintrin.h>

uint32_t pext_u32(uint32_t src, uint32_t mask) {
    return _pext_u32(src, mask);
}

uint64_t pext_u64(uint64_t src, uint64_t mask) {
    return _pext_u64(src, mask);
}
#else
uint32_t pext_u32(uint32_t src, uint32_t mask) {
    return pext_impl(src, mask);
}

uint64_t pext_u64(uint64_t src, uint64_t mask) {
    return pext_impl(src, mask);
}
#endif

NB_MODULE(_core, m) {
    m.doc() = R"pbdoc(
        Pext extension module
        -----------------------
        .. currentmodule:: pext
        .. autosummary::
           :toctree: _generate
    )pbdoc";

    m.def("pext_u32", &pext_u32, "Extract bits from a 32-bit integer");
    m.def("pext_u64", &pext_u64, "Extract bits from a 64-bit integer");
    m.def("multiply", &multiply, "Multiply two integers");
}
