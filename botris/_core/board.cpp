#include <nanobind/nanobind.h>
#include <nanobind/stl/array.h>
#include "engine/Board.hpp"

namespace nb = nanobind;

void bind_board(nb::module_ &m) {
    nb::class_<Board>(m, "Board")
        .def_ro_static("width", &Board::width)
        .def_ro_static("visual_height", &Board::visual_height)
        .def_ro_static("height", &Board::height)

        .def(nb::init<>())
        .def("get", &Board::get)
        .def("get_column", &Board::get_column)
        .def("set", nb::overload_cast<size_t, size_t>(&Board::set))
        .def("set_piece", nb::overload_cast<const Piece&>(&Board::set))
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
        .def_rw("board", &Board::board);
}
