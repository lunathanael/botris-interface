#include <nanobind/nanobind.h>
#include <nanobind/stl/array.h>

#include "engine/Board.hpp"

namespace nb = nanobind;
using namespace nb::literals;

void bind_board(nb::module_ &m) {
    nb::class_<Board>(m, "Board")
        .def_ro_static("width", &Board::width)
        .def_ro_static("visual_height", &Board::visual_height)
        .def_ro_static("height", &Board::height)

        .def(nb::init<>())
        .def("get", &Board::get, "x"_a, "y"_a)
        .def("get_column", &Board::get_column, "x"_a)
        .def("set", nb::overload_cast<size_t, size_t>(&Board::set), "x"_a, "y"_a)
        .def("set", nb::overload_cast<const Piece&>(&Board::set), "piece"_a)
        .def("unset", &Board::unset, "x"_a, "y"_a)
        .def("clearLines", &Board::clearLines)
        .def("filledRows", &Board::filledRows)
        .def("is_empty", &Board::is_empty)
        .def("bounded", &Board::bounded, "height"_a)
        .def("not_empty", &Board::not_empty, "height"_a)
        .def("full", &Board::full, "height"_a)
        .def("has_imbalanced_split", &Board::has_imbalanced_split, "height"_a)
        .def("empty_cells", &Board::empty_cells, "height"_a)
        .def("is_convex", &Board::is_convex)
        .def("get_garbage_height", &Board::get_garbage_height)
        .def("is_low", &Board::is_low)

        .def_rw("board", &Board::board)
        .def("copy", [](const Board &other) {
            Board board_copy = other;
            return board_copy;
        });
}
