#include <nanobind/nanobind.h>
#include <nanobind/stl/bind_vector.h>
#include <nanobind/stl/array.h>

#include "engine/MoveGen.hpp"

namespace nb = nanobind;
using namespace nb::literals;

void bind_movegen(nb::module_ &m) {
    auto tm = m.def_submodule("traditional_movegen", "Shaktris Traditional Movegen Module");
    auto sm = m.def_submodule("smeared_movegen", "Shaktris Smeared Movegen Module");

    tm.def("sky_piece_movegen", &Shaktris::MoveGen::Traditional::sky_piece_movegen, "board"_a, "piece_type"_a)
    .def("convex_movegen", &Shaktris::MoveGen::Traditional::convex_movegen, "board"_a, "piece_type"_a);

    sm.def("movegen", &Shaktris::MoveGen::Smeared::movegen, "board"_a, "type"_a)
    .def("god_movegen", &Shaktris::MoveGen::Smeared::god_movegen, "board"_a, "type"_a);
}
