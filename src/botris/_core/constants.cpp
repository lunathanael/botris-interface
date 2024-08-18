#include <nanobind/nanobind.h>
#include <nanobind/stl/array.h>

#include "engine/ShaktrisConstants.hpp"

namespace nb = nanobind;
using namespace nb::literals;

void bind_constants(nb::module_ &m) {
    nb::module_ constants = m.def_submodule("constants", "Group of constants and enums");

    nb::enum_<spinType>(constants, "spinType")
        .value("null", spinType::null)
        .value("mini", spinType::mini)
        .value("normal", spinType::normal);

    nb::enum_<RotationDirection>(constants, "RotationDirection")
        .value("North", RotationDirection::North)
        .value("East", RotationDirection::East)
        .value("South", RotationDirection::South)
        .value("West", RotationDirection::West)
        .value("RotationDirections_N", RotationDirection::RotationDirections_N);

    nb::enum_<ColorType>(constants, "ColorType")
        .value("S", ColorType::S)
        .value("Z", ColorType::Z)
        .value("J", ColorType::J)
        .value("L", ColorType::L)
        .value("T", ColorType::T)
        .value("O", ColorType::O)
        .value("I", ColorType::I)
        .value("Empty", ColorType::Empty)
        .value("LineClear", ColorType::LineClear)
        .value("Garbage", ColorType::Garbage)
        .value("ColorTypes_N", ColorType::ColorTypes_N);

    nb::enum_<PieceType>(constants, "PieceType")
        .value("S", PieceType::S)
        .value("Z", PieceType::Z)
        .value("J", PieceType::J)
        .value("L", PieceType::L)
        .value("T", PieceType::T)
        .value("O", PieceType::O)
        .value("I", PieceType::I)
        .value("Empty", PieceType::Empty)
        .value("PieceTypes_N", PieceType::PieceTypes_N);

    nb::enum_<TurnDirection>(constants, "TurnDirection")
        .value("Left", TurnDirection::Left)
        .value("Right", TurnDirection::Right);

    nb::enum_<Movement>(constants, "Movement")
        .value("Left", Movement::Left)
        .value("Right", Movement::Right)
        .value("RotateClockwise", Movement::RotateClockwise)
        .value("RotateCounterClockwise", Movement::RotateCounterClockwise)
        .value("SonicDrop", Movement::SonicDrop);

    nb::class_<Coord>(constants, "Coord")
        .def(nb::init<>())
        .def(nb::init<i8, i8>(), "x"_a, "y"_a)
        .def_rw("x", &Coord::x)
        .def_rw("y", &Coord::y);

    constants.attr("n_minos") = n_minos;

    constants.attr("piece_definitions") = piece_definitions;

    constants.attr("rot_piece_def") = rot_piece_def;

    constants.attr("piece_spawn_height") = piece_spawn_height;
}
