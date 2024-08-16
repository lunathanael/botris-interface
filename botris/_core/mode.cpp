#include <nanobind/nanobind.h>
#include "engine/modes/Botris.hpp"
#include "engine/ShaktrisConstants.hpp"

namespace nb = nanobind;

void bind_modes(nb::module_ &m) {
    nb::class_<Botris>(m, "Botris")
        .def(nb::init<>())  // Default constructor
        .def_static("combo_table", []() { return Botris::combo_table; })
        .def_static("attack_table", []() { return Botris::attack_table; })
        .def_static("all_spin_bonus", []() { return Botris::all_spin_bonus; })
        .def_static("pc_bonus", []() { return Botris::pc_bonus; })
        .def_static("b2b_bonus", []() { return Botris::b2b_bonus; })
        .def("points", [](Botris &self, int linesCleared, spinType spin, bool pc, u16 &combo, u16 &b2b) {
            return self.points(linesCleared, spin, pc, combo, b2b);
        });
}
