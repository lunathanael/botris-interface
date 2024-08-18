#include <nanobind/nanobind.h>
#include <nanobind/stl/array.h>
#include "engine/modes/Botris.hpp"
#include "engine/ShaktrisConstants.hpp"

namespace nb = nanobind;
using namespace nb::literals;

void bind_modes(nb::module_ &m) {
    nb::class_<Botris>(m, "Botris")
        .def(nb::init<>())
        .def_ro_static("combo_table", &Botris::combo_table)
        .def_ro_static("attack_table", &Botris::attack_table)
        .def_ro_static("all_spin_bonus", &Botris::all_spin_bonus)
        .def_ro_static("pc_bonus", &Botris::pc_bonus)
        .def_ro_static("b2b_bonus", &Botris::b2b_bonus)
        .def("points", [](Botris &self, int linesCleared, spinType spin, bool pc, u16 &combo, u16 &b2b) {
            return self.points(linesCleared, spin, pc, combo, b2b);
        }, "linesCleared"_a, "spin"_a, "pc"_a, "combo"_a, "b2b"_a);
}
