#include <nanobind/nanobind.h>
#include "engine/Board.hpp"

namespace nb = nanobind;

void bind_board(nb::module_ &m) {
    nb::class_<Board>(m, "Board")
        .def(nb::init<>())  // Default constructor
        .def("get", &Board::get)
        .def("get_column", &Board::get_column)
        .def("set", nb::overload_cast<size_t, size_t>(&Board::set))  // Overload for set with coordinates
        .def("set_piece", nb::overload_cast<const Piece&>(&Board::set))  // Overload for set with Piece
        .def("unset", &Board::unset)
        .def("clearLines", &Board::clearLines)
        .def("filledRows", &Board::filledRows)
        .def("is_empty", &Board::is_empty)
        .def("bounded", &Board::bounded)
        .def("not_empty", &Board::not_empty)
        .def("full", &Board::full)
        .def("has_imbalanced_split", &Board::has_imbalanced_split)
        .def("empty_cells", &Board::empty_cells)
        .def("is_convex", &Board::is_convex)
        .def("get_garbage_height", &Board::get_garbage_height)
        .def_rw("board", &Board::board);  // Exposing the board array
}
