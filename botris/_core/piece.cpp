#include <nanobind/nanobind.h>
#include "engine/Piece.hpp"
#include <nanobind/stl/bind_vector.h>

namespace nb = nanobind;

void bind_piece(nb::module_ &m) {
    nb::class_<Piece>(m, "Piece")
        .def(nb::init<PieceType>())
        .def(nb::init<PieceType, RotationDirection>())
        .def(nb::init<PieceType, RotationDirection, Coord>())
        .def(nb::init<PieceType, RotationDirection, Coord, spinType>())
        .def("rotate", &Piece::rotate)
        .def("calculate_rotate", &Piece::calculate_rotate)
        .def("hash", &Piece::hash)
        .def("compact_hash", &Piece::compact_hash)
        .def_rw("minos", &Piece::minos)
        .def_rw("position", &Piece::position)
        .def_rw("rotation", &Piece::rotation)
        .def_rw("type", &Piece::type)
        .def_rw("spin", &Piece::spin);

    nb::bind_vector<std::vector<Piece>>(m, "Piece");
}
