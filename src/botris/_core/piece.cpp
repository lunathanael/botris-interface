#include <nanobind/nanobind.h>
#include <nanobind/stl/bind_vector.h>
#include <nanobind/stl/array.h>

#include "engine/Piece.hpp"

namespace nb = nanobind;
using namespace nb::literals;

void bind_piece(nb::module_ &m) {
    nb::class_<Piece>(m, "Piece")
        .def(nb::init<PieceType>(), "type"_a)
        .def(nb::init<PieceType, RotationDirection>(), "type"_a, "dir"_a)
        .def(nb::init<PieceType, RotationDirection, Coord>(), "type"_a, "dir"_a, "pos"_a)
        .def(nb::init<PieceType, RotationDirection, Coord, spinType>(), "type"_a, "dir"_a, "pos"_a, "spn"_a)

        .def("rotate", &Piece::rotate, "direction"_a)
        .def("calculate_rotate", &Piece::calculate_rotate, "direction"_a)
        .def("hash", &Piece::hash)
        .def("compact_hash", &Piece::compact_hash)
        .def_rw("minos", &Piece::minos)
        .def_rw("position", &Piece::position)
        .def_rw("rotation", &Piece::rotation)
        .def_rw("type", &Piece::type)
        .def_rw("spin", &Piece::spin)

        .def("copy", [](const Piece &self) {
            Piece copy = self;
            return copy;
        });

    nb::bind_vector<std::vector<Piece>>(m, "VectorPiece");
}
